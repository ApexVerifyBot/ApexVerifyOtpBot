import importlib.util
import json
import os
import tempfile
import unittest


MODULE_PATH = "/workspaces/ApexVerifyOtpBot/apexverifybot.py"


spec = importlib.util.spec_from_file_location("apexverifybot", MODULE_PATH)
apexverifybot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(apexverifybot)


class BotSettingsTests(unittest.TestCase):
    def test_membership_status_is_checked_correctly(self):
        self.assertTrue(apexverifybot.membership_allows_access("member"))
        self.assertTrue(apexverifybot.membership_allows_access("creator"))
        self.assertFalse(apexverifybot.membership_allows_access("left"))
        self.assertFalse(apexverifybot.membership_allows_access("kicked"))

    def test_load_and_save_settings(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_path = os.path.join(tmpdir, "bot_settings.json")
            with open(settings_path, "w", encoding="utf-8") as fh:
                json.dump(
                    {
                        "otp_rate": 1.5,
                        "referral_price": 5,
                        "min_withdraw": 75,
                        "max_withdraw": 5000,
                    },
                    fh,
                )

            apexverifybot.SETTINGS_FILE = settings_path
            apexverifybot.BOT_SETTINGS = {}
            apexverifybot.load_settings()

            self.assertEqual(apexverifybot.get_setting("otp_rate"), 1.5)
            self.assertEqual(apexverifybot.get_setting("referral_price"), 5)
            self.assertEqual(apexverifybot.get_setting("min_withdraw"), 75)
            self.assertEqual(apexverifybot.get_setting("max_withdraw"), 5000)

            apexverifybot.save_settings({"otp_rate": 2.25, "referral_price": 6})
            apexverifybot.load_settings()
            self.assertEqual(apexverifybot.get_setting("otp_rate"), 2.25)
            self.assertEqual(apexverifybot.get_setting("referral_price"), 6)

    def test_menu_action_matches_stylized_button_text(self):
        self.assertEqual(
            apexverifybot.get_menu_action("📞 𝗚𝗘𝗧 𝗡𝗨𝗠𝗕𝗘𝗥"),
            "GET NUMBER",
        )
        self.assertEqual(
            apexverifybot.get_menu_action("⚙️ 𝗔𝗗𝗠𝗜𝗡 𝗣𝗔𝗡𝗘𝗟 ⚙️"),
            "ADMIN PANEL",
        )


if __name__ == "__main__":
    unittest.main()
