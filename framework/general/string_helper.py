import random
import string
from datetime import datetime


def convert_data_created_audit_to_timestamp(date_str):
    """
    Convert a date string in ISO 8601 format to a timestamp.

    :param date_str: Date string in ISO 8601 format (e.g., '2024-06-02T08:53:13Z')
    :return: Timestamp in milliseconds since the epoch
    """
    if date_str is None:
        return 0

    try:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        timestamp_ms = int(dt.timestamp())
        return timestamp_ms
    except ValueError as e:
        raise ValueError(f"Invalid date string format: {e}")


def convert_data_string_to_timestamp(data_string):
    """
    Converts the string representation of a date and time to a timestamp.
    Args:data_string (str): The string representation of the date and time (Example: "14-05-23 14:34:41 +0300").
    Returns:int: The timestamp representing the date and time.
    """
    try:
        date_parts, time_part, timezone = data_string.split(" ")
        day, month, year = date_parts.split("-")
        hour, minute, second = time_part.split(":")

        formatted_date_string = f"{year}-{month}-{day}T{hour}:{minute}:{second}"
        formatted_datetime = datetime.strptime(formatted_date_string, "%y-%m-%dT%H:%M:%S")

        timestamp = formatted_datetime.timestamp()

        return int(timestamp)
    except Exception as error:
        print("Error occurred while converting data string to timestamp:", error)
        return None


def generate_random_string(length: int = 6):
    """
    Generates a random string of digits.
    Args:length (int): The length of the random string to generate.
    Returns:str: A random string consisting of digits.
    """
    letters = string.ascii_lowercase
    return ''.join(random.choices(letters, k=length))
