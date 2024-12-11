import logging
from src.fetchData import fetch_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    try:
        fetch_data()
    except Exception as error:
        logging.error(f"An error occurred during fetch_data: {error}", exc_info=True)
