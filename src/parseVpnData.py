import re
import uuid


def parse_vpn_data(text):
    """Parse VPN data from a complex text structure into structured data."""
    print("Starting VPN data parsing...")

    result = []

    # Dynamic handling of text which can be list or text
    if isinstance(text, str):
        entries = re.split(r'\n+', text)
    elif isinstance(text, list):
        entries = text
    else:
        print("Error: Input must be a string or a list.")
        return []

    print(f"Processed input into {len(entries)} entries.")

    for idx, entry in enumerate(entries):
        # Check if the entry contains the word "OPENGW"
        if "OPENGW" in entry:
            entry_data = {}
            entry_data["id"] = str(uuid.uuid4())  # Create a random UUID

            # Extract sessions info
            sessions_match = re.search(r"(\d+\sSESSIONS.*?)\•", entry)
            if sessions_match:
                entry_data["info"] = sessions_match.group(1)
            else:
                continue  # Skip this entry if sessions info is not found

            # Extract region info
            region_match = re.search(r"(\w+\s\d+\.\d+)\•", entry)
            entry_data["info2"] = region_match.group(1) if region_match else None

            # Extract IP address
            ip_match = re.search(r"([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", entry)
            entry_data["ip"] = ip_match.group(0) if ip_match else None
            if entry_data["ip"] is None:
                continue  # Skip if IP is not found

            # Extract hostname and port
            hostname_port_match = re.search(r"([a-zA-Z0-9.-]+):(\d+)", entry)
            if hostname_port_match:
                entry_data["hostname"] = hostname_port_match.group(1)
                entry_data["port"] = int(hostname_port_match.group(2))
                entry_data["key"] = f"{entry_data['ip']}:{entry_data['port']}"
            else:
                continue  # Skip if hostname and port are not found

            # Extract country and location information
            country_info_match = re.search(r"(\w+)\s-\s([\w\s]+)\s~\s([\w\s]+)", entry)
            if country_info_match:
                entry_data["location"] = {"short": country_info_match.group(1), "country": country_info_match.group(2), "name": country_info_match.group(3) + " ★VPNGATE★"}

            # Add the entry to results only if it contains the required fields
            if "id" in entry_data and "hostname" in entry_data and "ip" in entry_data:
                result.append(entry_data)

    # Log the total number of parsed entries
    print(f"Total entries parsed: {len(result)}")
    print("Succesfully parsed data into Hosts")
    return result


# -----------------------------------------------------

# # Parse the data

# with open('output.txt', 'r', encoding='utf-8') as file:
#     raw_data = file.read()

# parsed_data = parse_vpn_data(response.text)

# print(parsed_data)

# -----------------------------------------------------

# url = os.getenv(
#     "URL2",
#     "https://giamping.com/repository/vpnrequestmobile.php?message=MBVRvEzBAVRWJST8NhVTRCAKbh2gO2ztsF5pwbdVfjd1UaqvsdTg9K122p1JxkuXgILF5npSo48jFf9ZAPnSe2rIRxq3QCGClEu21YSWLU6F3Nvf0XMJ2LU34sHuKa8go0DN0vHaf2OEFYNrhcXcGpozFezCj8OlN8cPzPrnIsLLMzBeTcglmF0jFS9gZZQipqU/3pbsftSRlUY1j5/BMpGPVPNhWMxE4m71qx7Ryfy5j967hXwjrP7dhrH63izHZyhbQIGPVPNXQXB1nf70ftqAgVEQNw=="
# )

# print("Step 2: Fetching data from URL...")
# # Fetch the data from the URL
# response = requests.get(url, timeout=15)  # Timeout after 15 seconds if no response
# response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx, 5xx)
# print("Step 3: Successfully fetched data from URL" + response.text[:100])
# parsed_data = parse_vpn_data(response.text)

# # print(parsed_data)
