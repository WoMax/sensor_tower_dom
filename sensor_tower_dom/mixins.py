from w3lib import url as w3lib_url

from . import constants


class UrlsMixin:
    def search_url(self, game_name, os_type):
        params = {
            **constants.SEARCH_PARAMS,
            "term": game_name,
            "os": os_type
        }
        url = w3lib_url.add_or_replace_parameters(constants.SEARCH_URL, params)
        return url

    def next_search_url(self, url, offset):
        return w3lib_url.add_or_replace_parameter(url, "offset", offset)


class MatchingMixin:
    def is_matched(self, entity_name, search_query):
        """
        Here could be implemented more sophisticated matching with
        included/excluded keywords and threshold, depending on requirements.
        For now, we check just if entity name is equal to search query.
        """
        return entity_name == search_query
