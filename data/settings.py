# data/settings.py

from util.log import logger
from data.json_io import load_from_json, save_to_json
from config import Config
from typing import ClassVar, List

class Settings:
    # How browser tabs should open
    # options: "new_window" — each tab in a new window
    #          "single_row" — all tabs in one window/row
    #          "links_only" — show only links
    TAB_OPEN_STYLE_OPTIONS: str = ["new_window", "single_row", "links_only"]
    tab_open_style_value: int

    # Language preference for search
    # Examples:
    # "auto" — use the language the user types in
    # "en"   — search in English
    # "ru"   — search in Russian, etc.
    language_preference: str

    # The maximum number of pages to search for
    limit_count: int

    # Minimum page rating
    min_page_rating: int
    # Maximum page rating
    max_page_rating: int

    # Clear the input field after a search (True/False)
    clear_input_after_search: bool

    # Current selected language
    LANGUAGE_PREFERENCE_OPTIONS: str = ["auto", "en", "ru"]
    language_preference_value: int

    # Show the program’s “opinion” about each site (True/False)
    program_opinion: bool

    def __init__(self) -> None:
        logger.info("Enter")

        self.by_default()
        load_from_json(self, Config.SETTINGS_PATH)
        if not self.check_parameters():
            logger.warning("Invalid or missing parameters in JSON, reverting to defaults")
            self.by_default()
            save_to_json(self, Config.SETTINGS_PATH)

    def by_default(self) -> None:
        logger.info("Enter")
        # Set default values for all settings
        self.tab_open_style_value = 0  # "new_window"
        self.limit_count = 10
        self.min_page_rating = 0
        self.max_page_rating = 100
        self.clear_input_after_search = True
        self.language_preference_value = 0 # "auto"
        self.program_opinion = False

    def check_parameters(self) -> bool:
        logger.info("Enter")
        return (
            self.check_tab_open_style() and
            self.check_limit_count() and
            self.check_min_page_rating() and
            self.check_max_page_rating() and
            self.check_clear_input_after_search() and
            self.check_language_preference() and
            self.check_program_opinion()
        )

    # Individual checks
    def check_tab_open_style(self) -> bool:
        if self.tab_open_style_value < 0 or self.tab_open_style_value >= len(self.TAB_OPEN_STYLE_OPTIONS):
            logger.info("Invalid tab_open_style!")
            return False
        return True


    def check_limit_count(self) -> bool:
        if not (1 <= self.limit_count <= 100):
            logger.info("limit_count must be between 1 and 100")
            return False
        return True


    def check_min_page_rating(self) -> bool:
        if self.min_page_rating < 0:
            logger.info("min_page_rating must be >= 0")
            return False
        return True


    def check_max_page_rating(self) -> bool:
        if self.max_page_rating < self.min_page_rating or self.max_page_rating > 100:
            logger.info("max_page_rating must be >= min_page_rating and <= 100")
            return False
        return True


    def check_clear_input_after_search(self) -> bool:
        if not isinstance(self.clear_input_after_search, bool):
            logger.info("clear_input_after_search must be True/False")
            return False
        return True


    def check_language_preference(self) -> bool:
        if self.language_preference_value < 0 or self.language_preference_value >= len(self.LANGUAGE_PREFERENCE_OPTIONS):
            logger.info("Invalid language_preference!")
            return False
        return True


    def check_program_opinion(self) -> bool:
        if not isinstance(self.program_opinion, bool):
            logger.info("program_opinion must be True/False")
            return False
        return True

