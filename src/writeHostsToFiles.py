import json
import logging
from pathlib import Path
import re
from typing import List, Dict
from .limitLogMessage import limit_log_message
from .config import data_dir, today_json_file, host_list_file, file_list_path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def read_file(file_path: Path) -> List:
    """
    Read JSON data from a file and handle potential errors.

    Args:
        file_path (Path): Path to the JSON file.

    Returns:
        list: Data loaded from the JSON file or an empty list on failure.
    """
    try:
        with file_path.open('r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        logging.error(f"Failed to decode JSON from {file_path}. File may be empty or corrupted.")
        return []
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}. Returning an empty list.")
        return []
    except Exception as e:
        logging.error(f"Unexpected error reading {file_path}: {e}")
        return []


def update_db_json(new_hosts: List[Dict]) -> None:
    """
    Update the db.json file with new hosts formatted as strings.

    Args:
        new_hosts (list of dict): List of new host entries.
    """
    db_hosts = read_file(host_list_file)
    logging.debug(f"Sample db_host: {db_hosts[0] if db_hosts else 'No hosts in db'}")

    unique_hosts = set(db_hosts)

    for host in new_hosts:
        if isinstance(host, dict):
            try:
                host_string = f"{host['ip']}:{host['port']}"
                unique_hosts.add(host_string)
            except KeyError as e:
                logging.error(f"Missing key in host dictionary: {e}")
        else:
            logging.error(f"Host {host} is not a dictionary. Skipping...")

    db_hosts = list(unique_hosts)

    try:
        with host_list_file.open('w', encoding='utf-8') as f:
            json.dump(db_hosts, f, indent=4)
        logging.info("db.json successfully updated.")
    except Exception as e:
        logging.error(f"Failed to write to db.json: {e}")


def update_today_json(new_hosts: List[Dict]) -> None:
    """
    Update today's JSON file with new hosts.

    Args:
        new_hosts (list of dict): List of new host entries.
    """
    all_data = read_file(today_json_file)
    all_data.extend(new_hosts)

    try:
        with today_json_file.open('w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=4)
        logging.info("Today's JSON file successfully updated.")
    except Exception as e:
        logging.error(f"Failed to write to today's JSON file: {e}")


def generate_file_summaries(dir_path: Path) -> List[Dict]:
    """
    Generate a summary of JSON files in the data directory.

    Args:
        dir_path (Path): Path to the directory containing JSON files.

    Returns:
        list of dict: List of file summaries.
    """
    summaries = []

    if not dir_path.is_dir():
        logging.error(f"The directory {dir_path} is invalid.")
        return summaries

    try:
        for file_path in dir_path.glob("*.json"):
            name = file_path.name
            # Adjust the filename validation as per your naming conventions
            if re.match(r'^\d{4}-\d{2}-\d{2}\.json$', name):
                data = read_file(file_path)
                summary = {"name": name, "sstpCount": len(data), "byteSize": file_path.stat().st_size}
                summaries.append(summary)
    except Exception as e:
        logging.error(f"Failed to generate file summaries. Error: {limit_log_message(str(e))}")

    return summaries


def update_file_summaries() -> None:
    """
    Generate and write file summaries to files.json.
    """
    try:
        files = generate_file_summaries(data_dir)
        files_json_path = file_list_path

        with files_json_path.open('w', encoding='utf-8') as f:
            json.dump(files, f, indent=4)
        logging.info("File summaries successfully written to files.json.")
    except Exception as e:
        logging.error(f"Failed to update file summaries. Error: {limit_log_message(str(e))}")


def handle_fetch_error(error: Exception) -> None:
    """
    Handles different types of errors during the fetch process.

    Args:
        error (Exception): The exception that was raised.
    """
    try:
        if hasattr(error, 'response') and error.response is not None:
            response_text = limit_log_message(error.response.text)
            logging.error(f"Received status {error.response.status_code} from the server. Response: {response_text}")
        elif hasattr(error, 'request') and error.request is not None:
            request_info = limit_log_message(str(error.request))
            logging.error(f"No response received from the server. Request: {request_info}")
        else:
            logging.error(f"Error: {limit_log_message(str(error))}")
    except Exception as e:
        logging.error(f"Failed to handle fetch error. Error: {limit_log_message(str(e))}")


def generate_file_summaries(dir_path: Path) -> List[Dict]:
    """
    Generate a summary of JSON files in the data directory.

    Args:
        dir_path (Path): Path to the directory containing JSON files.

    Returns:
        list of dict: List of file summaries.
    """
    import re  # Moved inside function to prevent potential circular imports
    summaries = []

    if not dir_path.is_dir():
        logging.error(f"The directory {dir_path} is invalid.")
        return summaries

    try:
        for file_path in dir_path.glob("*.json"):
            name = file_path.name
            # Adjust the regex pattern as per your filename format
            if re.match(r'^\d{4}-\d{2}-\d{2}\.json$', name):
                data = read_file(file_path)
                summary = {"name": name, "sstpCount": len(data), "byteSize": file_path.stat().st_size}
                summaries.append(summary)
    except Exception as e:
        logging.error(f"Failed to generate file summaries. Error: {limit_log_message(str(e))}")

    return summaries


def write_hosts_to_files(hosts: List[Dict]) -> None:
    """
    Write hosts to db.json, today's JSON file, and update file summaries.

    Args:
        hosts (list of dict): List of host entries to write.
    """
    if not hosts:
        logging.warning("No hosts found to write.")
        return

    logging.info(f"Writing {len(hosts)} hosts to files...")

    update_db_json(hosts)
    update_today_json(hosts)
    update_file_summaries()
