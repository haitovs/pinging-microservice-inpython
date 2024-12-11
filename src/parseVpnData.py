import re
import uuid
import logging
from typing import List, Dict, Union

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Precompile regex patterns for performance
SESSIONS_REGEX = re.compile(r"(\d+\sSESSIONS.*?)\•")
REGION_REGEX = re.compile(r"(\w+\s\d+\.\d+)\•")
IP_REGEX = re.compile(r"(\d+\.\d+\.\d+\.\d+)")
HOSTNAME_PORT_REGEX = re.compile(r"([a-zA-Z0-9.-]+):(\d+)")
COUNTRY_INFO_REGEX = re.compile(r"(\w+)\s-\s([\w\s]+)\s~\s([\w\s]+)")


def parse_entry(entry: str) -> Union[Dict, None]:
    """
    Parse a single entry and extract relevant VPN data.

    Args:
        entry (str): A single line of VPN data.

    Returns:
        dict or None: Parsed data if successful, else None.
    """
    if "OPENGW" not in entry:
        return None

    entry_data = {"id": str(uuid.uuid4())}

    # Extract sessions info
    sessions_match = SESSIONS_REGEX.search(entry)
    if sessions_match:
        entry_data["info"] = sessions_match.group(1)
    else:
        logging.warning("Sessions info not found in entry. Skipping entry.")
        return None

    # Extract region info
    region_match = REGION_REGEX.search(entry)
    entry_data["info2"] = region_match.group(1) if region_match else None

    # Extract IP address
    ip_match = IP_REGEX.search(entry)
    if ip_match:
        entry_data["ip"] = ip_match.group(1)
    else:
        logging.warning("IP address not found in entry. Skipping entry.")
        return None

    # Extract hostname and port
    hostname_port_match = HOSTNAME_PORT_REGEX.search(entry)
    if hostname_port_match:
        entry_data["hostname"] = hostname_port_match.group(1)
        entry_data["port"] = int(hostname_port_match.group(2))
        entry_data["key"] = f"{entry_data['ip']}:{entry_data['port']}"
    else:
        logging.warning("Hostname and port not found in entry. Skipping entry.")
        return None

    # Extract country and location information
    country_info_match = COUNTRY_INFO_REGEX.search(entry)
    if country_info_match:
        entry_data["location"] = {"short": country_info_match.group(1), "country": country_info_match.group(2), "name": f"{country_info_match.group(3)} ★VPNGATE★"}

    # Ensure required fields are present
    required_fields = ["id", "hostname", "ip"]
    if all(field in entry_data for field in required_fields):
        return entry_data
    else:
        logging.warning(f"Entry missing required fields: {entry_data}. Skipping entry.")
        return None


def parse_vpn_data(text: Union[str, List[str]]) -> List[Dict]:
    """
    Parse VPN data from a complex text structure into structured data.

    Args:
        text (str or list): Raw VPN data as a string or list of strings.

    Returns:
        list of dict: Parsed VPN data entries.
    """
    logging.info("Starting VPN data parsing...")

    if isinstance(text, str):
        entries = re.split(r'\n+', text)
    elif isinstance(text, list):
        entries = text
    else:
        logging.error("Input must be a string or a list.")
        return []

    logging.info(f"Processed input into {len(entries)} entries.")

    result = []
    for entry in entries:
        parsed_entry = parse_entry(entry)
        if parsed_entry:
            result.append(parsed_entry)

    logging.info(f"Total entries parsed: {len(result)}")
    logging.info("Successfully parsed data into Hosts.")
    return result
