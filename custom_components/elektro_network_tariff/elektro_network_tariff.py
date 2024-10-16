import datetime

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
    public_holidays.append((easter_saturday.month, easter_saturday.day))
    public_holidays.append((easter_monday.month, easter_monday.day))
    
    # Check if the date matches any public holiday
    if (date.month, date.day) in public_holidays:
        print("hollyday")
        return True

    return False


def calculate_tariff():
    date = datetime.datetime.now()
    month = date.month
    hour = date.hour
    is_high_season = month in [11, 12, 1, 2]
    weekend_or_holiday = is_weekend_or_holiday(date)

    # Define tariff rates in a more structured form
    # (hour_range, high_season_rate, low_season_rate)
    tariffs = [
        ((0, 5), (3, 4), (5, 4)),  # Early morning
        ((6, 6), (2, 3), (4, 3)),  # 6 AM
        ((7, 13), (1, 2), (3, 2)),  # Morning to early afternoon
        ((14, 15), (2, 3), (4, 3)),  # Early afternoon
        ((16, 19), (1, 2), (3, 2)),  # Late afternoon to early evening
        ((20, 21), (2, 3), (4, 3)),  # Evening
        ((22, 23), (3, 4), (5, 4)),  # Late evening
    ]

    # Initialize an array to hold the tariffs for each hour of the day
    blocks = []

    for hour in range(24):  # For each hour from 0 to 23
        for time_range, high_season_tariff, low_season_tariff in tariffs:
            start, end = time_range
            if start <= hour <= end:
                if is_high_season and not weekend_or_holiday:
                    blocks.append(high_season_tariff[0])
                elif not is_high_season and weekend_or_holiday:
                    blocks.append(low_season_tariff[0])
                else:
                    blocks.append(high_season_tariff[1] if is_high_season else low_season_tariff[1])
                break
        else:
            # Default tariff if none of the conditions above are met
            blocks.append(0)

    # Now return the current tariff and the blocks
    current_tariff = blocks[date.hour]  # Get the tariff for the current hour
    return current_tariff, blocks  # Return both the current tariff and the blocks

