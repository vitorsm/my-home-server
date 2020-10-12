from datetime import datetime
from dateutil import parser


def from_str_to_date(date_str: str) -> datetime:
    return parser.parse(date_str)
