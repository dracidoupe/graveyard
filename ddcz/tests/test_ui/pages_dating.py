from enum import Enum


class DatingListPage(Enum):
    """Selectors for the dating list page"""

    FIRST_TEXT = "//article[@class='dating'][1]//span[@class='label'][text()='Text:']/following-sibling::span[@class='value']"
    CREATE_DATING_LINK = "//a[contains(@href, 'seznamka/pridat')]"
    NAVIGATION_DATING = "//a[contains(@href, 'seznamka')]"


class DatingCreatePage(Enum):
    """Selectors for the dating creation page"""

    NAME_INPUT = "id_name"
    EMAIL_INPUT = "id_email"
    AREA_INPUT = "id_area"
    TEXT_INPUT = "id_text"
    GROUP_SELECT = "id_group"
    AGE_INPUT = "id_age"
    PHONE_INPUT = "id_phone"
    MOBILE_INPUT = "id_mobil"
    EXPERIENCE_INPUT = "id_experience"
    SUBMIT_BUTTON = "//button[@type='submit']"
