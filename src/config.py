from pathlib import Path
from datetime import datetime

# Define today's date
today = datetime.now().strftime("%Y-%m-%d")

# Define the base directory (assuming 'config.py' is in 'src/')
base_dir = Path(__file__).resolve().parent.parent  # Adjust as per your project structure

# Define the data directory
data_dir = base_dir / "data"

# Ensure the data directory exists
data_dir.mkdir(parents=True, exist_ok=True)

# Define the JSON file paths
today_json_file = data_dir / f"{today}.json"
host_list_file = data_dir / "db.json"
file_list_path = data_dir / "files.json"
