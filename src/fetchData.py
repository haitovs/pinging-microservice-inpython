import os
import requests
from .writeHostsToFiles import write_hosts_to_files
from .parseVpnData import parse_vpn_data

# Define the URL (can be passed via environment variable or hardcoded)
url = os.getenv(
    "URL2",
    "https://giamping.com/repository/vpnrequestmobile.php?message=MBVRvEzBAVRWJST8NhVTRCAKbh2gO2ztsF5pwbdVfjd1UaqvsdTg9K122p1JxkuXgILF5npSo48jFf9ZAPnSe2rIRxq3QCGClEu21YSWLU6F3Nvf0XMJ2LU34sHuKa8go0DN0vHaf2OEFYNrhcXcGpozFezCj8OlN8cPzPrnIsLLMzBeTcglmF0jFS9gZZQipqU/3pbsftSRlUY1j5/BMpGPVPNhWMxE4m71qx7Ryfy5j967hXwjrP7dhrH63izHZyhbQIGPVPNXQXB1nf70ftqAgVEQNw=="
)


def fetch_data():
    print("Step 1: Starting fetch_data...")

    if not url:
        print("Error: URL is not defined")
        return

    try:
        print("Step 2: Fetching data from URL...")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        print("Step 3: Successfully fetched data from URL" + response.text[:100])

        # Extract the file data
        file_data = response.text

        # Debugging the type of file_data
        print(f"Type of file_data: {type(file_data)}")  # Expecting a string

        print(f"Step 4: Parsing data from URL...")
        hosts = parse_vpn_data(file_data)

        # Debug the type of parsed hosts to check if it's structured correctly
        print(f"Type of hosts: {type(hosts)}")  # Expecting a list or dict
        print(f"Sample host: {hosts[0] if hosts else 'No hosts parsed'}")

        # Write to files
        print("Step 5: Writing data to files...")
        write_hosts_to_files(hosts)
        print("Step 7: Completed fetching and processing data successfully")

    except requests.exceptions.RequestException as error:
        print(f"Step Error: Fetching data failed with error: {error}")
