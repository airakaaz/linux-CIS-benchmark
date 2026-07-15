from dataclasses import dataclass
from pathlib import Path
from glob import glob
import re
import shlex
import grp
import pwd

from utils.command import run


def exists(path: str) -> bool:
    return Path(path).exists()


def read(path: str) -> str:
    return Path(path).read_text()


def read_lines(path: str) -> list[str]:
    return read(path).splitlines()


def resolve_paths(*patterns: str) -> list[str]:
    paths = []

    for pattern in patterns:
        paths.extend(sorted(glob(pattern)))

    return paths


@dataclass(slots=True)
class RegexResult:
    found: bool
    locations: list[str]


def contains_regex(paths: list[str], pattern: str, flags=re.MULTILINE) -> RegexResult:
    regex = re.compile(pattern, flags=flags)
    locations: list[str] = []

    for file in paths:
        path = Path(file)
        if not path.is_file():
            continue

        try:
            content = path.read_text(errors="ignore")
        except OSError:
            continue

        if regex.search(content):
            locations.append(file)

    return RegexResult(
        found=bool(locations),
        locations=locations,
    )


_EXCLUDED_FILESYSTEMS = re.compile(
    r"^(?:nfs|proc|cifs|smb|vfat|iso9660|efivarfs|selinuxfs|ncpfs)"
)
_EXCLUDED_MOUNTS = ("/run", "/tmp", "/var/tmp")
_EXCLUDED_PATHS = (
    "*/containers/storage/*",
    "*/containerd/*",
    "*/kubelet/*",
    "/sys/*",
    "/snap/*",
    "/boot/efi/*",
)


def local_mounts() -> list[str]:
    result = run("findmnt -Dkerno fstype,target")
    if not result.ok and not result.stdout:
        return []

    mounts: list[str] = []
    for line in result.stdout.splitlines():
        fields = line.split(None, 1)
        if len(fields) != 2:
            continue
        fstype, target = fields
        if _EXCLUDED_FILESYSTEMS.match(fstype):
            continue
        if any(target == mount or target.startswith(mount + "/") for mount in _EXCLUDED_MOUNTS):
            continue
        mounts.append(target)
    return mounts


def _find_on_mount(mount: str, expression: str) -> list[str]:
    exclusions = " ".join(
        f"-path {shlex.quote(pattern)} -prune -o" for pattern in _EXCLUDED_PATHS
    )
    command = (
        f"find {shlex.quote(mount)} -mount -xdev {exclusions} "
        f"{expression} -print"
    )
    result = run(command)
    return [path for path in result.stdout.splitlines() if path]


def world_writable_paths() -> tuple[list[str], list[str]]:
    files: list[str] = []
    directories: list[str] = []
    for mount in local_mounts():
        paths = _find_on_mount(mount, "\\( -type f -o -type d \\) -perm -0002")
        for path in paths:
            current = Path(path)
            if current.is_file():
                files.append(path)
            elif current.is_dir():
                try:
                    if current.stat().st_mode & 0o1000 == 0:
                        directories.append(path)
                except OSError:
                    directories.append(path)
    return sorted(set(files)), sorted(set(directories))


def unowned_paths() -> tuple[list[str], list[str]]:
    unowned: list[str] = []
    ungrouped: list[str] = []
    valid_uids = {entry.pw_uid for entry in pwd.getpwall()}
    valid_gids = {entry.gr_gid for entry in grp.getgrall()}
    for mount in local_mounts():
        for path in _find_on_mount(mount, "\\( -type f -o -type d \\) \\( -nouser -o -nogroup \\)"):
            try:
                stat_result = Path(path).stat()
            except OSError:
                continue
            if stat_result.st_uid not in valid_uids:
                unowned.append(path)
            if stat_result.st_gid not in valid_gids:
                ungrouped.append(path)
    return sorted(set(unowned)), sorted(set(ungrouped))
