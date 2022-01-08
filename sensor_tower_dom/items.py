import typing

import pydantic

from . import constants
from . import utils


class Review(pydantic.BaseModel):
    date: str
    negative: int
    positive: int

    @pydantic.validator("date", pre=True)
    def parse_date(cls, value):
        value = utils.get_date_in_proper_format(value)
        if not constants.RE_DATE.match(value):
            error_msg = f"Can not parse 'Date' value. Raw value: {value}"
            raise ValueError(error_msg)

        return value

    @pydantic.validator("negative", pre=True)
    def parse_negative(cls, value):
        return utils.get_review_number(value)

    @pydantic.validator("positive", pre=True)
    def parse_positive(cls, value):
        return utils.get_review_number(value)

    @pydantic.root_validator()
    def rename_fields(cls, values):
        for old_name, new_name in constants.MAPPING_REVIEW_FIELDS:
            if old_name in values:
                values[new_name] = values.pop(old_name)
        return values


class GameInfo(pydantic.BaseModel):
    game_name: str
    platform: str
    date_scrapped: str
    sensor_score: int
    visibility_score: int
    internationalization_score: int
    downloads: int
    revenue: float
    keywords: typing.List[str]
    reviews: typing.List[Review]

    @pydantic.validator("revenue", pre=True)
    def parse_revenue(cls, value):
        """Convert $100k into 100000."""

        numb = utils.get_regex_value(value, constants.RE_NUMB)
        if numb:
            large_numb = utils.get_regex_value(value, constants.RE_LARGE_NUMB)
            return float(numb) * constants.LARGE_NUMBERS.get(large_numb, 1)

        error_msg = f"Can not parse 'Revenue' value. Raw value: {value}"
        raise ValueError(error_msg)

    @pydantic.validator("downloads", pre=True)
    def parse_downloads(cls, value):
        """Convert 7k into 7000."""

        numb = utils.get_regex_value(value, constants.RE_NUMB)
        if numb:
            large_numb = utils.get_regex_value(value, constants.RE_LARGE_NUMB)
            return int(numb) * constants.LARGE_NUMBERS.get(large_numb, 1)

        error_msg = f"Can not parse 'Downloads' value. Raw value: {value}"
        raise ValueError(error_msg)

    @pydantic.root_validator()
    def rename_fields(cls, values):
        for old_name, new_name in constants.MAPPING_GAME_INFO_FIELDS:
            if old_name in values:
                values[new_name] = values.pop(old_name)
        return values
