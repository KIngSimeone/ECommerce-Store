from django.utils import timezone
from datetime import datetime, timedelta

from dateutil import tz, parser
import pytz


def toUiReadableDateFoormat(value):
    try:
        if value is None:
            return ""

        localizedValue = timezone.localtime(
            value, pytz.timezone('UTC'))
        return datetime.strftime(localizedValue, "%b %d, %Y %I:%M%p")
    except Exception as ex:
        print(ex)
        return str(value)

def toUiReadableDateOnlyFormat(value):
    try:
        localizedValue = timezone.localtime(
            value, pytz.timezone('UTC'))
        return datetime.strftime(localizedValue, "%Y-%m-%d")
    except Exception as ex:
        print("exception was thrown ", ex)
        return ""

def convertStringToDate(value, dayFirst=True):
    try:
        return parser.parse(value, dayfirst=dayFirst)
    except ValueError:
        return None


def convertStringToDateTz(value, dayFirst=True):
    try:

        dateValue = parser.parse(value, dayfirst=dayFirst)

        pst = pytz.timezone('UTC')
        d = pst.localize(dateValue)

        return d
    except ValueError:
        return None


def timezoneAwareDate(date, tzinfo='UTC'):
    try:
        realTzInfo = pytz.timezone(tzinfo)
        return date.astimezone(realTzInfo)
    except ValueError:
        return None
