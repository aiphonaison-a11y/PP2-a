from datetime import datetime, timedelta
from zoneinfo import ZoneInfo



# 1. Current Date and Time

now = datetime.now()
print("Current DateTime:", now)



# 2. Formatting Date

formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print("Formatted Date:", formatted)



# 3. Calculating Difference

date1 = datetime(2026, 1, 1)
date2 = datetime(2026, 2, 1)

difference = date2 - date1
print("Days between dates:", difference.days)



# 4. Working with Timezones

utc_time = datetime.now(ZoneInfo("UTC"))
almaty_time = utc_time.astimezone(ZoneInfo("Asia/Almaty"))

print("UTC Time:", utc_time)
print("Almaty Time:", almaty_time)