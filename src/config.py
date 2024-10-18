import os
from datetime import datetime

# Define today's date
today = datetime.now().strftime("%Y-%m-%d")

# Adjust the directory path to be one level above the 'src' directory and normalize it
dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))

# Ensure the data directory exists
if not os.path.exists(dir_path):
    os.makedirs(dir_path)  # Create the directory if it doesn't exist

# Define the JSON file paths
today_json_file = os.path.join(dir_path, f"{today}.json")
host_list_file = os.path.join(dir_path, "db.json")
file_list_path = os.path.join(dir_path, "files.json")
