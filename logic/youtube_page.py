from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from infra.page_base import WebPageBase
from selenium.common.exceptions import TimeoutException


class YouTubeInterface(WebPageBase):
    FULL_SCREEN = (By.CSS_SELECTOR, "button.ytp-fullscreen-button")
    SOUND_TOGGLE = (By.CSS_SELECTOR, "button.ytp-mute-button")
    VIDEO_PLAY = (By.CSS_SELECTOR, "button.ytp-play-button")
    CONFIG_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Settings']")
    DARK_MODE = "Dark theme"
    LIGHT_MODE = "Light theme"
    SYSTEM_MODE = "Use device theme"
    THEME_MENU = (By.XPATH, "//tp-yt-paper-item[@role='menuitem']")

    def start_video(self):
        play_button = self.wait_condition.until(EC.element_to_be_clickable(self.VIDEO_PLAY))
        play_button.click()
        self.wait_condition.until(EC.element_to_be_clickable(self.VIDEO_PLAY))
        return True

    def change_sound_state(self):
        self.wait_condition.until(EC.element_to_be_clickable(self.SOUND_TOGGLE)).click()
        return self.video_is_muted()

    def video_is_muted(self):
        return self.browser_driver.execute_script("return document.querySelector('video').muted;")

    def activate_full_screen(self):
        full_screen_btn = self.wait_condition.until(EC.element_to_be_clickable(self.FULL_SCREEN))
        full_screen_btn.click()
        self.wait_condition.until(
            lambda d: self.browser_driver.execute_script("return document.fullscreenElement != null;"))

    def verify_full_screen(self):
        return self.browser_driver.execute_script("return document.fullscreenElement != null;")

    def deactivate_full_screen(self):
        if self.verify_full_screen():
            self.browser_driver.execute_script("document.exitFullscreen();")
            self.wait_condition.until(
                lambda d: self.browser_driver.execute_script("return document.fullscreenElement == null;"))

    def check_full_screen_exit(self):
        return self.browser_driver.execute_script("return document.fullscreenElement == null;")

    def access_settings(self):
        self.wait_condition.until(EC.element_to_be_clickable(self.CONFIG_BUTTON)).click()

    def select_theme_menu(self, current_theme):
        return self.wait_condition.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//div[@id='label' and contains(text(), 'Appearance: {current_theme}')]")))

    def choose_theme_option(self, theme_choice):
        return self.wait_condition.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//tp-yt-paper-item[@role='link' and contains(., '{theme_choice}')]")))

    def modify_theme(self, new_theme, current_theme="Device theme"):
        theme_choice = ""
        if new_theme == "Dark":
            theme_choice = self.DARK_MODE
        elif new_theme == "Light":
            theme_choice = self.LIGHT_MODE
        elif new_theme == "Device theme":
            theme_choice = self.SYSTEM_MODE
        self.access_settings()
        theme_menu = self.select_theme_menu(current_theme)
        theme_menu.click()
        theme_option = self.choose_theme_option(theme_choice)
        theme_option.click()

    def confirm_theme(self, theme):
        self.access_settings()
        try:
            self.select_theme_menu(theme)
        except TimeoutException:
            return False
        finally:
            self.access_settings()
        return True
