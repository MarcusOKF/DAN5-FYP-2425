import datetime

def convert_microseconds_to_hms(microseconds):
    # Convert microseconds to seconds
    seconds = microseconds / 1000000

    # Create a timedelta object using the total number of seconds
    duration = datetime.timedelta(seconds=seconds)

    # Extract hours, minutes, and seconds from the timedelta object
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    seconds = duration.seconds % 60

    return [hours,minutes,seconds]
