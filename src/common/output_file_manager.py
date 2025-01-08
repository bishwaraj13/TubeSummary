import inspect
from datetime import datetime
import os

from src.config.settings import (
    BASE_DIR,
    MEDIA_DIR
)

def get_date_time():
    # Get current date and time using datetime.now()
    current = datetime.now()
    # Format it as YYYY-MM-DD_HH-MM-SS
    formatted_datetime = current.strftime("%Y-%m-%d_%H-%M-%S")
    return str(formatted_datetime)

def provide_file_path(file_title, extension, media=False):
    # Get the current frame
    current_frame = inspect.currentframe()
    # Get the caller's frame (one level up)
    caller_frame = current_frame.f_back
    # Get the filepath from the caller's frame
    caller_filepath = caller_frame.f_code.co_filename

    caller_filename = caller_filepath.split("/")[-1].split(".")[0]

    base_dir = BASE_DIR
    if media:
        base_dir = MEDIA_DIR

    directory = f"{base_dir}/{caller_filename}"
    os.makedirs(directory, exist_ok=True)

    return os.path.join(directory, f"{file_title}_{get_date_time()}{extension}")

def get_latest_file(directory, extension=".json"):
    files = [f for f in os.listdir(directory) if f.endswith(extension)]
    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(directory, f)))
    return os.path.join(directory, latest_file)

