import os
import requests
import logging
from requests.adapters import HTTPAdapter, Retry
from .writeHostsToFiles import write_hosts_to_files
from .parseVpnData import parse_vpn_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_url():
    """Retrieve the URL from environment variables or use the default."""
    return os.getenv(
        "URL2",
        "https://giamping.com/repository/vpnrequestmobile.php?message=MBVRvEzBAVRWJST8NhVTRCAKbh2gO2ztsF5pwbdVfjd1UaqvsdTg9K122p1JxkuXgILF5npSo48jFf9ZAPnSe2rIRxq3QCGClEu21YSWLU6F3Nvf0XMJ2LU34sHuKa8go0DN0vHaf2OEFYNrhcXcGpozFezCj8OlN8cPzPrnIsLLMzBeTcglmF0jFS9gZZQipqU/3pbsftSRlUY1j5/BMpGPVPNhWMxE4m71qx7Ryfy5j967hXwjrP7dhrH63izHZyhbQIGPVPNXQXB1nf70ftqAgVEQNw=="
    )


def create_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504)):
    """Create a requests Session with retry strategy."""
    session = requests.Session()
    retry = Retry(total=retries, read=retries, connect=retries, backoff_factor=backoff_factor, status_forcelist=status_forcelist, allowed_methods=["GET"])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def fetch_data():
    """
    Fetch data from a specified URL, parse it, and write the results to files.
    """
    logging.info("Step 1: Starting fetch_data...")

    url = get_url()

    if not url:
        logging.error("URL is not defined.")
        return

    logging.info(f"Using URL: {url}")

    session = create_session()

    try:
        logging.info("Step 2: Fetching data from URL...")
        response = session.get(url, timeout=15)
        response.raise_for_status()
        logging.info(f"Step 3: Successfully fetched data from URL. Data snippet: {response.text[:100]}")

        # Extract the file data
        file_data = response.text

        logging.debug(f"Type of file_data: {type(file_data)}")  # Expecting a string

        logging.info("Step 4: Parsing data from URL...")
        hosts = parse_vpn_data(file_data)

        logging.debug(f"Type of hosts: {type(hosts)}")  # Expecting a list or dict
        if hosts:
            logging.debug(f"Sample host: {hosts[0]}")
        else:
            logging.warning("No hosts parsed from the fetched data.")

        # Write to files
        logging.info("Step 5: Writing data to files...")
        write_hosts_to_files(hosts)
        logging.info("Step 7: Completed fetching and processing data successfully.")

    except requests.exceptions.RequestException as error:
        logging.error(f"Step Error: Fetching data failed with error: {error}", exc_info=True)
        # Optionally, handle retries or fallback mechanisms here
