from ._Base_1_7 import GsettingsRule, GsettingsCheck, equals


class Rule_1_7_5(GsettingsRule):
    rule_id = "1.7.5"
    title = "Ensure GDM autorun-never is configured"
    _CHECKS = [
        GsettingsCheck(
            schema="org.gnome.desktop.media-handling",
            key="autorun-never",
            require_locked=True,
            validate=equals("true"),
            expected="locked and set to true",
        ),
    ]
