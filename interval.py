from datetime import datetime

def calculate_interval(start_time_str):
  # Consistent time format for parsing
  desired_format = "%Y-%m-%d %H:%M:%S"

  # Parse strings to datetime objects
  start_time = datetime.strptime(start_time_str, desired_format)
  # Get current time
  current_time = datetime.now()

  # Format the current time (end time)
  end_time = current_time.strftime(desired_format)

  # Validate that start time is not later than end time
  if start_time > datetime.strptime(end_time, desired_format):
      raise ValueError("Start time cannot be later than end time.")
  else:
      return ((datetime.strptime(end_time, desired_format) - start_time).total_seconds() / float(60)) # convert from seconds to mins
     
  



