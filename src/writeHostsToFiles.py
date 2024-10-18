import json
import logging
import os
from .limitLogMessage import limit_log_message
from .config import *

logging.basicConfig(level=logging.INFO)


def read_file(file_path):
    """Read JSON data from a file and handle potential errors."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)  # Attempt to load the file as JSON
    except json.JSONDecodeError:
        logging.error(f"Failed to decode JSON from {file_path}. File may be empty or corrupted.")
        return []  # Return an empty list if the file is empty or invalid
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}. Returning an empty list.")
        return []  # Return an empty list if the file is not found
    except Exception as e:
        logging.error(f"Unexpected error reading {file_path}: {str(e)}")
        return []


def update_db_json(new_hosts):
    """Update the db.json file with new hosts formatted as strings."""

    db_hosts = read_file(host_list_file)  # Read the existing hosts from db.json
    print(f"Sample db_host: {db_hosts[0] if db_hosts else 'No hosts in db'}")

    # Create a set to hold the unique host strings
    unique_hosts = set(db_hosts)  # Start with existing hosts

    # Process new_hosts
    for host in new_hosts:
        if isinstance(host, dict):
            try:
                # Format the host as "IP:Port"
                host_string = f"{host['ip']}:{host['port']}"
                unique_hosts.add(host_string)  # Add the formatted string to the set
            except KeyError as e:
                print(f"Error: Missing key in host dictionary - {str(e)}")
        else:
            print(f"Error: host {host} is not a dictionary. Skipping...")

    # Convert the set back to a list
    db_hosts = list(unique_hosts)

    # Write the updated host list back to db.json
    with open(host_list_file, 'w', encoding='utf-8') as f:
        json.dump(db_hosts, f)
    print("db.json successfully updated")


def update_today_json(new_hosts):
    """Update today's JSON file with new hosts."""
    all_data = read_file(today_json_file)  # Read the existing data from today's JSON file
    all_data += new_hosts  # Add the new hosts to the data

    # Write the updated data back to today's JSON file
    with open(today_json_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f)


def update_file_summaries():
    """Generate and write file summaries to files.json."""
    try:
        # Specify the directory where the JSON files are stored (adjust this path if necessary)
        json_files_directory = os.path.dirname(file_list_path)

        # Generate the file summaries
        files = generate_file_summaries(json_files_directory)

        # Write the summaries to files.json
        files_json_path = os.path.join(json_files_directory, 'files.json')
        with open(files_json_path, 'w', encoding='utf-8') as f:
            json.dump(files, f, indent=4)
        logging.info("File summaries successfully written to files.json.")
    except Exception as e:
        logging.error(f"Failed to update file summaries. Error: {limit_log_message(str(e))}")


def generate_file_summaries(dir_path):
    """Generate a summary of JSON files in the data directory."""
    summaries = []

    # Check if dir_path is a valid directory
    if not os.path.isdir(dir_path):
        logging.error(f"The directory {dir_path} is invalid.")
        return summaries  # Return an empty list if the directory is invalid

    try:
        # Loop through all .json files in the directory
        for name in os.listdir(dir_path):
            # Check if the file name matches the expected format
            if name.endswith(".json") and all(part.isdigit() for part in name.replace('.json', '').split('-')):
                file_path = os.path.join(dir_path, name)

                # Get summary data: count of entries and file size
                summary = {"name": name, "sstpCount": len(read_file(file_path)), "byteSize": os.path.getsize(file_path)}
                summaries.append(summary)
    except Exception as e:
        logging.error(f"Failed to generate file summaries. Error: {limit_log_message(str(e))}")
    return summaries


def handle_fetch_error(error):
    """Handles different types of errors during the fetch process."""
    try:
        if hasattr(error, 'response') and error.response is not None:
            logging.error(f"Error: Received status {error.response.status_code} from the server. Response: {limit_log_message(str(error.response.text))}")
        elif hasattr(error, 'request') and error.request is not None:
            logging.error(f"Error: No response received from the server. Request: {limit_log_message(str(error.request))}")
        else:
            logging.error(f"Error: {limit_log_message(str(error))}")
    except Exception as e:
        logging.error(f"Failed to handle fetch error. Error: {limit_log_message(str(e))}")


def write_hosts_to_files(hosts):
    """Write hosts to db.json, today's JSON file, and update file summaries."""
    if not hosts:
        logging.warning("No hosts found to write.")
        return

    logging.info(f"Writing {len(hosts)} hosts to files...")

    try:
        logging.info("Updating db.json...")
        update_db_json(hosts)
        logging.info("db.json successfully updated.")
    except Exception as e:
        logging.error(f"Failed to update db.json. Error: {limit_log_message(str(e))}")

    try:
        logging.info("Updating today's JSON file...")
        update_today_json(hosts)
        logging.info("Today's JSON file successfully updated.")
    except Exception as e:
        logging.error(f"Failed to update today's JSON file. Error: {limit_log_message(str(e))}")

    try:
        logging.info("Updating file summaries...")
        update_file_summaries()
        logging.info("File summaries successfully updated.")
    except Exception as e:
        logging.error(f"Failed to update file summaries. Error: {limit_log_message(str(e))}")
