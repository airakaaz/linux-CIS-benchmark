from dataclasses import dataclass
import shlex
import subprocess


@dataclass(slots=True)
class CommandResult:
    stdout: str
    stderr: str
    returncode: int

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def run(command: str) -> CommandResult:
    try:
        result = subprocess.run(
            shlex.split(command),
            capture_output=True,
            text=True,
        )

        return CommandResult(
            stdout=result.stdout.strip(),
            stderr=result.stderr.strip(),
            returncode=result.returncode,
        )
    except Exception:
        return CommandResult(
            stdout="",
            stderr="",
            returncode=1,
        )
