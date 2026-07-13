from ._Base_1_7 import GsettingsRule, GsettingsCheck, equals


class Rule_1_7_4(GsettingsRule):
    rule_id = "1.7.4"
    title = "Ensure GDM automount is configured"
    _CHECKS = [
        GsettingsCheck(
            schema="org.gnome.desktop.media-handling",
            key="automount",
            require_locked=True,
            validate=equals("false"),
            expected="locked and set to false",
        ),
        GsettingsCheck(
            schema="org.gnome.desktop.media-handling",
            key="automount-open",
            require_locked=True,
            validate=equals("false"),
            expected="locked and set to false",
        ),
    ]
