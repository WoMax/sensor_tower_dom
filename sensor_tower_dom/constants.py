import re

BASE_URL = "https://sensortower.com/"
ITEMS_PER_PAGE = 10000  # max possible value

LARGE_NUMBERS = {
    "k": 10**3,
    "m": 10**6,
    "b": 10**9
}

MAPPING_GAME_INFO_FIELDS = {
    ("game_name", "Game name"),
    ("platform", "Platform"),
    ("date_scrapped", "Date scrapped"),
    ("sensor_score", "Sensor score"),
    ("visibility_score", "Visibility score"),
    ("internationalization_score", "Internationalization score"),
    ("downloads", "Downloads"),
    ("revenue", "Revenue"),
    ("keywords", "List of keywords"),
    ("reviews", "Review breakdown")
}

MAPPING_REVIEW_FIELDS = {
    ("date", "Date"),
    ("positive", "# of positive reviews"),
    ("negative", "# of negative reviews")
}

OS_TYPES = ["android", "ios"]
RE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RE_DOWNLOADS = re.compile(r"downloadsLastMonth\(\)[^>]+?>(.+?)</span>")
RE_INTER_SCORE = re.compile(r"nationalizationScore\(\)[^>]+?>(\d+?)</span>")
RE_KEYWORDS = re.compile(r"class=\"keyword\"[^>]+?>(.+?)</span>")
RE_LARGE_NUMB = re.compile(r"\D*[\d.]+([kmb])")
RE_NUMB = re.compile(r"\D*([\d.]+)\D?")
RE_REVENUE = re.compile(r"revenueLastMonth\(\)[^>]+?>(.+?)</span>")

RE_REVIEW = re.compile(
    r"<b>(?P<date>[^>]+?)</b>\s*<br>\s*<span.+?>Positive</span>:\s*"
    r"(?P<positive>[\d,]+?)<br>\s*<span.+?>Negative</span>:\s*"
    r"(?P<negative>[\d,]+?)</span>"
)

RE_SENSOR_SCORE = re.compile(r"sensorScore\(\)[^>]+?>(\d+?)</span>")
RE_VISIBILITY_SCORE = re.compile(r"visibilityScore\(\)[^>]+?>(\d+?)</span>")

SEARCH_PARAMS = {
    "categories[]": 6014,  # Games
    "entity_type": "app",
    "limit": ITEMS_PER_PAGE,
    "offset": 0,
    "search_fields[]": "name",
}

SEARCH_URL = "https://app.sensortower.com/advanced_search"
