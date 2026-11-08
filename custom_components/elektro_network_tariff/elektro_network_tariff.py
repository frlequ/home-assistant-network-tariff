import datetime

# The block schedule published for 2027 applies from this date onwards.
SCHEDULE_2027_START = datetime.date(2027, 1, 1)

# Block for each hour of the day (one digit per hour, starting at 00:00).
# Keys are (is_high_season, is_non_working_day).
SCHEDULE_UNTIL_2026 = {
    (True, False): "333333211111112211112233",
    (True, True): "444444322222223322223344",
    (False, False): "444444322222223322223344",
    (False, True): "555555433333334433334455",
}

# Source: Agencija za energijo, act of 29 September 2025, Annex 2, chapter 3.
SCHEDULE_FROM_2027 = {
    (True, False): "333333111111222221112233",
    (True, True): "444444333333444443333344",
    (False, False): "555555333333444443333355",
    (False, True): "555555444444555554444455",
}

def calculate_easter(year):
    """Calculate Easter Sunday for a given year."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime.date(year, month, day)

def get_easter_saturday_monday(year):
    """Calculate Easter Saturday and Easter Monday for a given year."""
    easter_sunday = calculate_easter(year)
    easter_saturday = easter_sunday - datetime.timedelta(days=1)
    easter_monday = easter_sunday + datetime.timedelta(days=1)
    return easter_saturday, easter_monday

def is_weekend_or_holiday(date):
    """Check if the date is a weekend or a public holiday in Slovenia."""
    # Check if it's Saturday or Sunday (weekend)
    if date.weekday() in [5, 6]:
        return True
    
    # List of fixed public holidays in Slovenia
    public_holidays = [
        (1, 1),    # New Year's Day
        (1, 2),    # New Year's Day
        (2, 8),    # Preseren Day
        (4, 27),   # Resistance Day
        (5, 1),    # Labour Day
        (5, 2),    # Labour Day
        (6, 25),   # Statehood Day
        (8, 15),   # Assumption Day
        (10, 31),  # National Reformation Day
        (11, 1),   # All Saints' Day
        (12, 25),  # Christmas
        (12, 26),  # Independence and Unity Day
    ]
    
    # Calculate Easter Saturday and Easter Monday for the year of the given date
    easter_saturday, easter_monday = get_easter_saturday_monday(date.year)
    
    # Add Easter Saturday and Easter Monday to the list of public holidays
    public_holidays.extend([(easter_saturday.month, easter_saturday.day), 
                            (easter_monday.month, easter_monday.day)])
    
    # Check if the date matches any public holiday
    return (date.month, date.day) in public_holidays

def is_high_season_month(month):
    """Check if the month is in the high season (November to February)."""
    return month in [11, 12, 1, 2]

def get_blocks_for_day(day):
    """Return the tariff block of each hour for the given calendar day."""
    if isinstance(day, datetime.datetime):
        day = day.date()
    schedule = SCHEDULE_FROM_2027 if day >= SCHEDULE_2027_START else SCHEDULE_UNTIL_2026
    hours = schedule[(is_high_season_month(day.month), is_weekend_or_holiday(day))]
    return [int(block) for block in hours]

def calculate_tariff(now=None):
    """Calculate the current tariff and additional attributes for electricity tariff blocks.

    `now` is the local date and time to calculate for, defaulting to the system clock.
    """
    if now is None:
        now = datetime.datetime.now()

    blocks = get_blocks_for_day(now)

    # Get the tariff for the current hour
    current_tariff = blocks[now.hour]
    # The hour after 23:00 belongs to the next day, which can have different blocks
    if now.hour == 23:
        next_tariff_block = get_blocks_for_day(now.date() + datetime.timedelta(days=1))[0]
    else:
        next_tariff_block = blocks[now.hour + 1]
    # Determine if the next block is higher than the current
    is_next_block_higher = next_tariff_block > current_tariff

    # Return a dictionary with the required attributes
    return {
        "current_tariff": current_tariff,     # Current hour's tariff
        "is_holiday": is_weekend_or_holiday(now),  # Is today a holiday or weekend
        "is_high_season": is_high_season_month(now.month),  # Is high tariff season
        "next_tariff_block": next_tariff_block,  # Tariff for the next hour
        "is_next_block_higher": is_next_block_higher,  # Is the next block higher
        "blocks": blocks                      # Tariff blocks for the entire day
    }
