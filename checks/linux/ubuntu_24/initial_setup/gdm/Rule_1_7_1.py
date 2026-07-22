from ._Base_1_7 import GsettingsRule, GsettingsCheck, equals, non_empty


class Rule_1_7_1(GsettingsRule):
    rule_id = "1.7.1"
    title = "Ensure GDM login banner is configured"
    server_lvl = 1
    workstation_lvl = 1
    _REQUIRED_PACKAGE = "gdm3"
    _CHECKS = [
        GsettingsCheck(
            schema="org.gnome.login-screen",
            key="banner-message-enable",
            require_locked=True,
            validate=equals("true"),
            expected="locked and set to true",
        ),
        GsettingsCheck(
            schema="org.gnome.login-screen",
            key="banner-message-text",
            require_locked=True,
            validate=non_empty(),
            expected="locked and set to site-approved text (verify manually)",
        ),
    ]
