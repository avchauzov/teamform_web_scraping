# TeamForm Web Scraping Project

## Description

This project performs web scraping to collect league ranking data from the TeamForm website. It utilizes a headless Chrome browser to navigate through the site, collecting data for each specified quarter/week.

## Features

- **Web Scraping for League Ranking Data**: Collects league ranking data from the TeamForm website, providing insights into team performances and standings.
- **Headless Chrome Browser Utilization**: Employs a headless Chrome browser for efficient navigation and data collection from web pages.
- **Configurable Data Load**: The `PAGES_NUMBER` variable in `_functions.py` allows control over how much data is loaded by determining the number of times the 'Load More' button is clicked, each click revealing additional rows of data.
- **Memory Efficiency**: Designed to avoid memory issues by limiting the number of pages loaded. The script clicks the 'Load More' button a predetermined number of times (e.g., 17 times) to fetch a substantial yet manageable amount of data.
- **Focused Data Retrieval**: Currently, the script is specialized in retrieving league data. While it does not support 'Club' or 'National' data at the moment, its structure is conducive to future expansions in this area.

## Python Version Support

This project supports Python 3.8.

![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)

Note: This software has not been tested on earlier or later versions of Python.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/avchauzov/teamform_web_scraping.git
```

2. Navigate to the project directory:

```bash
cd teamform_web_scraping
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Ensure the necessary dependencies, Chrome browser & Chromium are installed.
2. Modify file paths & links.json file as needed.
3. Run the main script to perform web scraping:

```bash
python main.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- **Name:** Andrew Chauzov
- **Email:** [avchauzov@gmail.com](mailto:avchauzov@gmail.com)

For more information or inquiries about the project, feel free to reach out via email.

## Acknowledgements

- [Selenium](https://www.selenium.dev/): A powerful tool for browser automation used in this project for efficient web scraping.
