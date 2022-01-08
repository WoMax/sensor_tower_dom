import asyncio
import datetime
import json

import pyppeteer
import pyppeteer.errors
import scrapy
from w3lib import url as w3lib_url

from .. import constants
from .. import items
from .. import mixins
from .. import utils


class SensorTowerSpider(scrapy.Spider, mixins.UrlsMixin, mixins.MatchingMixin):
    name = "sensor_tower"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_names = json.loads(kwargs.get("game_names"))

    def start_requests(self):
        for game_name in self.game_names:
            for os_type in constants.OS_TYPES:
                yield scrapy.Request(url=self.search_url(game_name, os_type))

    def parse(self, response):
        data = response.json()
        total_items = data["meta"]["total_count"]
        game_name = w3lib_url.url_query_parameter(response.url, "term")
        offset = int(w3lib_url.url_query_parameter(response.url, "offset"))
        is_first_page = offset == 0

        if is_first_page and total_items > constants.ITEMS_PER_PAGE:
            yield from self.parse_next_pages(response.url, total_items)

        for entity in data["data"]["entities"]:
            if self.is_matched(entity["humanized_name"], game_name):
                yield self.parse_game_info(
                    entity["app_id"], game_name, entity["os"]
                )

    def parse_next_pages(self, url, total_items):
        offset_step = constants.ITEMS_PER_PAGE

        for offset in range(offset_step, total_items + 1, offset_step):
            yield scrapy.Request(url=self.next_search_url(url, offset))

    def parse_game_info(self, app_id, game_name, os_type):
        data = {}
        asyncio.get_event_loop().run_until_complete(
            self.run_and_parse(constants.BASE_URL, app_id, data)
        )

        item = items.GameInfo.construct(
            game_name=game_name,
            platform=os_type,
            date_scrapped=datetime.date.today().strftime("%Y-%m-%d"),
            sensor_score=data["sensor_score"],
            visibility_score=data["visibility_score"],
            internationalization_score=data["internationalization_score"],
            downloads=data["downloads"],
            revenue=data["revenue"],
            keywords=data["keywords"],
            reviews=data["reviews"],
        )

        return item.dict()

    async def run_and_parse(self, url, app_id, data):
        """Run product page in browser and parse data."""

        browser = await pyppeteer.launch()
        page = await browser.newPage()
        await page.goto(url)
        await page.waitForXPath("//input[@id=\"app-search-input\"]")
        await page.keyboard.type(str(app_id))
        await page.waitForXPath("//span[@class=\"autocomplete-name\"]")
        await page.click("span[class=\"autocomplete-name\"]")
        await page.waitForXPath(
            "//*[name()=\"g\"]/*[name()=\"rect\" and "
            "contains(@class, \"highcharts-shadow\")]"
        )

        reviews, content = await self.parse_reviews(page)
        await browser.close()

        for key, regex in (
            ("sensor_score", constants.RE_SENSOR_SCORE),
            ("visibility_score", constants.RE_VISIBILITY_SCORE),
            ("internationalization_score", constants.RE_INTER_SCORE),
            ("downloads", constants.RE_DOWNLOADS),
            ("revenue", constants.RE_REVENUE)
        ):
            data[key] = utils.get_regex_value(content, regex)

        data["keywords"] = constants.RE_KEYWORDS.findall(content)
        data["reviews"] = reviews

    async def parse_reviews(self, page):
        """Parse 'Review breakdown' data from histogram chart."""

        rectangles = await page.xpath(
            "//*[name()=\"g\" and contains(@class, \"highcharts-series-0\") "
            "and contains(@class, \"highcharts-tracker\")]/*[name()=\"rect\" "
            "and contains(@class, \"highcharts-shadow\")]"
        )

        content, reviews = "", []
        for rectangle in rectangles:
            await asyncio.wait([rectangle.hover()])
            rect = await rectangle.boundingBox()
            await page.mouse.move(rect["x"] + rect["width"] // 2, rect["y"])

            try:
                await page.waitForXPath(
                    "//span[text()=\"Positive\"]", options={"timeout": 10000}
                )
            except pyppeteer.errors.TimeoutError:
                break  # there is no reviews

            content = await page.content()
            reviews.append(constants.RE_REVIEW.search(content).groupdict())

        return reviews, content
