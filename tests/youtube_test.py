import unittest
from infra.browser_wrapper import WebNavigator
from logic.youtube_page import YouTubeInterface


class TestYouTubeFeatures(unittest.TestCase):
    def setUp(self):
        self.navigator = WebNavigator()
        self.browser_driver = self.navigator.launch_browser("https://www.youtube.com/")
        self.wait_tool = self.navigator.fetch_wait()
        self.youtube_interface = YouTubeInterface(self.browser_driver, self.wait_tool)

    def test_video_playback(self):
        self.navigator.open_website("https://www.youtube.com/watch?v=Qgr4dcsY-60")
        result = self.youtube_interface.start_video()
        self.assertTrue(result)
        result = self.youtube_interface.start_video()
        self.assertTrue(result)

    def test_full_screen_mode(self):
        self.navigator.open_website("https://www.youtube.com/watch?v=Qgr4dcsY-60")
        self.youtube_interface.start_video()
        self.youtube_interface.activate_full_screen()
        self.assertTrue(self.youtube_interface.verify_full_screen(), "Video is not in full screen mode.")
        self.youtube_interface.deactivate_full_screen()
        self.assertTrue(self.youtube_interface.check_full_screen_exit(), "Video did not exit full screen mode.")

    def test_sound_toggle(self):
        self.navigator.open_website("https://www.youtube.com/watch?v=Qgr4dcsY-60")
        self.youtube_interface.start_video()
        is_muted = self.youtube_interface.change_sound_state()
        self.assertTrue(is_muted, "Video is not muted.")
        is_muted = self.youtube_interface.change_sound_state()
        self.assertFalse(is_muted, "Video is not unmuted.")

    def test_theme_change_to_dark(self):
        self.youtube_interface.modify_theme("Dark")
        is_theme_applied = self.youtube_interface.confirm_theme("Dark")
        self.assertTrue(is_theme_applied)

    def test_theme_change_to_light(self):
        self.youtube_interface.modify_theme("Light")
        is_theme_applied = self.youtube_interface.confirm_theme("Light")
        self.assertTrue(is_theme_applied)

    def tearDown(self):
        self.navigator.terminate_browser()


if __name__ == "__main__":
    unittest.main()
