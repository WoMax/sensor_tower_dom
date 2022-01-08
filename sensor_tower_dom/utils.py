from dateutil.parser import parse


def get_regex_value(source, regex, group=1):
    return regex.search(source) and regex.search(source).group(group) or None


def get_date_in_proper_format(date):
    return parse(date).strftime("%Y-%m-%d")


def get_review_number(string):
    return int(string.replace(",", ""))
