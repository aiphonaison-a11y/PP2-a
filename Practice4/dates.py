# dates.py

# Import datetime and timedelta from the datetime module
from datetime import datetime, timedelta


# 1. Subtract five days from current date

# Get the current date and time
current_date = datetime.now()

# Subtract 5 days using timedelta
five_days_ago = current_date - timedelta(days=5)

# Print results
print("1. Current date:", current_date)
print("   Five days ago:", five_days_ago)


# 2. Print yesterday, today, tomorrow

# Get the current date and time again
today = datetime.now()

# Yesterday means today minus 1 day
yesterday = today - timedelta(days=1)

# Tomorrow means today plus 1 day
tomorrow = today + timedelta(days=1)

# Print only the date part
print("\n2. Yesterday, today, tomorrow:")
print("   Yesterday:", yesterday.date())
print("   Today:", today.date())
print("   Tomorrow:", tomorrow.date())


# 3. Drop microseconds from datetime

# Get current datetime with microseconds
now_with_microseconds = datetime.now()

# Replace microseconds with 0
without_microseconds = now_with_microseconds.replace(microsecond=0)

# Print both versions
print("\n3. Datetime without microseconds:")
print("   Before:", now_with_microseconds)
print("   After: ", without_microseconds)


# 4. Calculate difference between two dates in seconds

# Create the first date manually
date1 = datetime(2025, 3, 10, 12, 0, 0)

# Create the second date manually
date2 = datetime(2025, 3, 11, 15, 30, 0)

# Subtract date1 from date2
difference = date2 - date1

# Convert difference to total seconds
seconds = difference.total_seconds()

# Print the result
print("\n4. Difference between two dates in seconds:")
print("   Date 1:", date1)
print("   Date 2:", date2)
print("   Seconds:", int(seconds))