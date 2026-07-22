from ._Base_1_7 import GsettingsRule, GsettingsCheck, numeric_at_most


class Rule_1_7_3(GsettingsRule):
    rule_id = "1.7.3"
    title = "Ensure GDM screen lock is configured"
    server_lvl = 1
    workstation_lvl = 1
    _CHECKS = [
        GsettingsCheck(
            schema="org.gnome.desktop.session",
            key="idle-delay",
            require_locked=True,
            validate=numeric_at_most(900, exclude_zero=True),
            expected="locked and <= 900 (15 min), not 0",
        ),
        GsettingsCheck(
            schema="org.gnome.desktop.screensaver",
            key="lock-delay",
            require_locked=True,
            validate=numeric_at_most(5),
            expected="locked and <= 5",
        ),
    ]
