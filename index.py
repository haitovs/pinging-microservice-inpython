# index.py

from src.fetchData import fetch_data

if __name__ == "__main__":
    try:
        fetch_data()
    except Exception as error:
        print("Error occurred during fetch_data:", str(error))
