import datetime

NULL = "null"

# code from https://stackoverflow.com/a/30536361/1732223
def deltafmt(td):
    # Get the timedelta’s sign and absolute number of seconds.
    sign = "-" if td.days < 0 else ""
    secs = abs(td).total_seconds()

    # Break the seconds into more readable quantities.
    days, rem = divmod(secs, 86400)  # Seconds per day: 24 * 60 * 60
    hours, rem = divmod(rem, 3600)  # Seconds per hour: 60 * 60
    mins, secs = divmod(rem, 60)

    # Format (as per above answers) and return the result string.
    return f"{sign}{int(hours)}h {int(mins)}m"

def datetime_range(start_date, end_date, inclusive=True):
    """Generate a sequence of datetime.date objects.
    Arguments:
        start_date (datetime.date object): Start date.
        end_date (datetime.date object): End date.
        inclusive (boolean): Whether or not to include `end_date` in the range.
    Yields:
        datetime.date object
    """
    number_of_minutes = int((end_date - start_date).seconds // 60)
    if inclusive:
        number_of_minutes += 1
    if isinstance(start_date, datetime.timedelta) and isinstance(end_date, datetime.timedelta):
        for minutes in range(number_of_minutes):
            yield deltafmt(start_date + datetime.timedelta(minutes=minutes))
    else:
        for minutes in range(number_of_minutes):
            yield start_date + datetime.timedelta(minutes=minutes)


def value_or_null(start_date, end_date, queryset, date_attr, value_attr=None, value=None):
    """Arguments:
        start_date (datetime.date object): Start date.
        end_date: (datetime.date object): End date.
        queryset (QuerySet): Django queryset that we're interested in.
        date_attr (str): Name of date attribute of `queryset`.
        value_attr (str): Name of `queryset` attr to search.
        value (str): Name `queryset` keyword to search in `value_attr`.
    Yields:
        numeric value
    """
    for new_date in datetime_range(start_date, end_date):
        query = {
            date_attr + "__year":   new_date.year,
            date_attr + "__month":  new_date.month,
            date_attr + "__day":    new_date.day,
            date_attr + "__hour":   new_date.hour,
            date_attr + "__minute": new_date.minute,
        }
        if value_attr and value:
            query[value_attr + "__icontains"] = value
        items = queryset.filter(**query)
        yield items.count()
