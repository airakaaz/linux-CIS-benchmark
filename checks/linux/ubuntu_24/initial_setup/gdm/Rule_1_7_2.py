from ._Base_1_7 import GsettingsRule, GsettingsCheck, equals


class Rule_1_7_2(GsettingsRule):
    rule_id = "1.7.2"
    title = "Ensure GDM disable-user-list is configured"
    _REQUIRED_PACKAGE = "gdm3"
    _CHECKS = [
        GsettingsCheck(
            schema="org.gnome.login-screen",
            key="disable-user-list",
            require_locked=True,
            validate=equals("true"),
            expected="locked and set to true",
        ),
    ]
