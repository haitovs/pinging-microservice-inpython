# Pinging Microservice

## Overview

The Pinging Microservice monitors network endpoints by checking both ping response times and port availability. It performs two main tasks:

1. **Ping Monitoring**: Measures round-trip time (RTT) for specified IP addresses or URLs.
2. **Port Monitoring**: Checks if a specified port (default: 443) is accessible.

## Features

- Real-time RTT and port availability monitoring
- Multithreaded checks for improved performance
- Dynamic configuration via environment variables
- Error logging for results and issues
- Automatic updates of monitoring results to JSON files

## Usage

1. **Configuration**: List target IPs or URLs in the `target.txt` file.
2. **Execution**: Run the script to start monitoring and save results in JSON files.
3. **Review**: Check the `output` directory for the results.

## Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/haitovs/pinging-microservice-inpython.git
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Set environment variables (e.g., `URL`, `URL2`).
4. Run the script:

   ```sh
   python index.py
   ```

## GitHub Actions

The project uses GitHub Actions for automatic execution on push events and scheduled runs every 5 minutes.

## Contributing

Contributions are welcome! Open an issue or submit a pull request for improvements.

## License

Licensed under the MIT License.

---