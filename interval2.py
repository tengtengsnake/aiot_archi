from datetime import datetime, timedelta

# Consistent time format for parsing
desired_format = "%Y-%m-%d %H:%M:%S"

# Parse strings to datetime objects
start_time_str = "2024-04-06 13:28:44"
start_time = datetime.strptime(start_time_str, desired_format)

# Get current time
current_time = datetime.now() 

# Convert current time to desired format (same as start_time)
end_time = current_time.strftime(desired_format)

# Validate that start time is not later than end time
if start_time > datetime.strptime(end_time, desired_format):
    raise ValueError("Start time cannot be later than end time.")
else:
    time_delta = (datetime.strptime(end_time, desired_format) - start_time).total_seconds()
    print(time_delta,type(time_delta)) # calculate the time interval between the start time and end time and print the reuslt in seconds