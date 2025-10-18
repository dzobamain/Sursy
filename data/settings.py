# data/settings.py

from util.log import logger

class Settings:
    # How browser tabs should open
    # options: "new_window" — each tab in a new window
    #          "single_row" — all tabs in one window/row
    #          "links_only" — show only links
    tab_open_style: str

    # The maximum number of pages to search for
    limit_count: int

    # Minimum page rating
    min_page_rating: int
    # Maximum page rating
    max_page_rating: int

    # Clear the input field after a search (True/False)
    clear_input_after_search: bool

    # Language preference for search
    #     Examples:
    #       "auto" — use the language the user types in
    #       "en"   — search in English
    #       "es"   — search in Russian, etc.
    #       ...
    language_preference: str

    # Show the program’s “opinion” about each site (True/False)
    program_opinion: bool
    
    def __init__(self):
        logger.info("Enter")
        self.by_default()

    def by_default(self):
        logger.info("Enter")
        # Set default values for all settings.
        self.tab_open_style = "new_window"
        self.limit_count = 10
        self.min_page_rating = 0
        self.max_page_rating = 100
        self.clear_input_after_search = True
        self.language_preference = "auto"
        self.program_opinion = False
    
    def check_parameters(self) -> bool:
        logger.info("Enter check_parameters")
        # Call all individual checks
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
        logger.info("Enter check_tab_open_style")
        if self.tab_open_style not in ["new_window", "single_row", "links_only"]:
            logger.info("Invalid tab_open_style!")
            return False
        return True

    def check_limit_count(self) -> bool:
        logger.info("Enter check_limit_count")
        if self.limit_count < 0 or self.limit_count > 100:
            logger.info("limit_count must be between 0 and 100")
            return False
        return True

    def check_min_page_rating(self) -> bool:
        logger.info("Enter check_min_page_rating")
        if self.min_page_rating < 0:
            logger.info("min_page_rating must be >= 0")
            return False
        return True

    def check_max_page_rating(self) -> bool:
        logger.info("Enter check_max_page_rating")
        if self.max_page_rating < self.min_page_rating or self.max_page_rating > 100:
            logger.info("max_page_rating must be >= min_page_rating and <= 100")
            return False
        return True

    def check_clear_input_after_search(self) -> bool:
        logger.info("Enter check_clear_input_after_search")
        if not isinstance(self.clear_input_after_search, bool):
            logger.info("clear_input_after_search must be True/False")
            return False
        return True

    def check_language_preference(self) -> bool:
        logger.info("Enter check_language_preference")
        if self.language_preference not in ["auto", "en", "es", "ru", "fr", "de", "zh"]:
            logger.info("Invalid language_preference!")
            return False
        return True

    def check_program_opinion(self) -> bool:
        logger.info("Enter check_program_opinion")
        if not isinstance(self.program_opinion, bool):
            logger.info("program_opinion must be True/False")
            return False
        return True
