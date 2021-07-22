from enum import Enum


class TavernTableListPage(Enum):
    URL = "/putyka/"
    TAVERN_TABLE_LIST_NAME = "//table[contains(@class, 'tavern-table-list')]//span[contains(@class, 'tavern-table-name')]"
    NAVIGATION_LIST_STYLE_TEMPLATE = "//a[@data-list-style='{slug}']"

    FIRST_TABLE_LINK = "//table[contains(@class, 'tavern-table-list')]//span[contains(@class, 'tavern-table-name')]:first"

    TAVERN_TABLE_LINK_TEMPLATE = (
        "//table[contains(@class, 'tavern-table-list')]//*[@data-table-id='{table_id}']"
    )


class TavernTablePostPage(Enum):
    URL_TEMPLATE = "/putyka/stul/{table_id}/prispevky/"
    POST_TEXTAREA = '//textarea[@id="id_text"]'
    POST_SUBMIT = '//input[@class="comment__submit"]'
    FIRST_COMMENT = '//p[@class="comment_text"]'
