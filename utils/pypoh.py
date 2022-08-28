# https://github.com/jamesluc007/pypoh/blob/main/pypoh/pypoh.py

import requests
import json

_BASE_URL = "https://api.poh.dev"

def _profiles_api(
    amount: int, order_by: str, order_direction: str, include_unregistered: bool, start_cursor: str
) -> dict:
    """
    Internal method. It simply calls the profiles API. It was created to avoid code repetition.
    Args:
        amount: Amount of registered accounts to fetch. Unused.
        order_by: "registered_time" or "creation_time"
        order_direction: "desc" or "asc"
        include_unregistered: True or False
        start_cursor: Internal use only. This is the cursor returned by the precious _profile_api call if there was some
    Returns:
        A dict of with the key "meta" and the key "profiles"
    """
    include_unregistered_str = "true" if include_unregistered else "false"
    start_cursor_str = "&start_cursor={}".format(start_cursor) if start_cursor is not None else ""
    response_dict = json.loads(
        requests.get(
            "{}/profiles?order_by={}&order_direction={}&include_unregistered={}{}".format(
                _BASE_URL, order_by, order_direction, include_unregistered_str, start_cursor_str
            )
        ).text
    )
    return response_dict

def get_raw_set_of_addresses(
    amount: int = 100,
    order_by: str = "registered_time",
    order_direction: str = "desc",
    include_unregistered: bool = False,
) -> set:
    """
    It returns a set with all the addresses. This might be a bit quicker than calling the get_raw_list_of_humans method.
    The number of returned humans will always be a multiple of 100 for this specific method.
    If you specify an amount of 150, you will get a set of 200 humans instead.
    Args:
        amount: Amount of registered accounts to fetch.
        order_by: "registered_time" or "creation_time"
        order_direction: "desc" or "asc"
        include_unregistered: True or False
    Returns:
        A set with addresses (set of str).
    """

    ultimate_set = set()
    start_cursor = None
    for i in range((amount // 100) + 1):
        response_dict = _profiles_api(amount, order_by, order_direction, include_unregistered, start_cursor)
        start_cursor = response_dict["meta"]["next_cursor"] if response_dict["meta"]["has_more"] else None
        ultimate_set.update([j["eth_address"] for j in response_dict["profiles"]])

    return ultimate_set