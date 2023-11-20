# TeamForm Web Scraping Project

## Overview

This project performs web scraping to collect league ranking data from the TeamForm website. It utilizes a headless Chrome browser to navigate through the website, collecting data for each specified quarter/week.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [FAQ](#faq)

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

## Dependencies

- pandas
- selenium
- tqdm (for convenience)
- pyarrow OR fastparquet (for ```gzip``` support)

Install dependencies using:

```bash
pip install -r requirements.txt
```

## File Structure

```plaintext
teamform_web_scraping/
│
├── _data/
│   └── league/
├── _logs/
├── _credentials/
│   └── links.json
├── _functions.py
├── main.py
├── README.md
└── requirements.txt
```

## Contributing

Feel free to contribute to the project. Fork the repository, create a branch, make your changes, and submit a pull request.

## FAQ

### Q: What is the `PAGES_NUMBER` variable in `_functions.py`?

A: The `PAGES_NUMBER` variable in `_functions.py` determines how many times the 'Load More' button is clicked at the bottom of the page. Each click reveals additional rows of data. Adjusting this variable allows you to control the amount of data loaded.

### Q: Does it scrape ALL data?

A: No. Due to a memory issue that arises when attempting to load and process all available data, the scraping script is designed to load a limited number of pages. Specifically, it clicks the 'Load More' button 17 times, fetching a substantial but manageable amount of data. This approach helps avoid memory-related challenges during
the scraping process.

### Q: Does this script support 'Club' or 'National' data?

A: No, at this moment. The current version of the script focuses on retrieving data for leagues. While there are no immediate plans to support 'Club' or 'National' data, the script's structure makes it relatively straightforward to extend functionality for these categories in the future.

### Q: Which Python versions does this script support?

A: The script has been tested on Python 3.8.
