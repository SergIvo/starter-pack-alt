from ..locators import Locator


def test_pydantic_parse_obj():
    Locator.parse_obj({
        'state_class_locator': '/main-menu/',
    })
