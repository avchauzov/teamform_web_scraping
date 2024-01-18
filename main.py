"""
TeamForm Web Scraping Script

This script performs web scraping to collect data from the TeamForm website, specifically league rankings.
It initializes logging, retrieves the list of already processed files, and utilizes a headless Chrome browser
to navigate through the website, collecting data for each specified quarter and week.

Dependencies:
- pandas
- selenium
_ tqdm

Usage:
- Run this script to perform web scraping and collect data from the TeamForm website.
- Ensure the necessary dependencies and the Chrome browser are installed.
- Modify URLs and file paths as needed for different scraping tasks.

Functions:
- main(): Main function for web scraping TeamForm website data.

Example:
```python
if __name__ == "__main__":
    main()
"""

import os.path

from tqdm import tqdm

from functions import get_already_processed, get_init, get_sb_week_options, initiate_browser, process_week_data, URL


def main():
	"""
	Main function for web scraping TeamForm website data.
	
	This function initializes logging, retrieves the list of already processed files,
	sets up a headless Chrome browser, and iterates through the specified week options,
	collecting data for each week using the `process_week_data` function.
	
	Usage:
	- Run this function to perform web scraping and collect data from the TeamForm website.
	- Ensure the necessary dependencies and the Chrome browser are installed.
	- Modify URLs and file paths as needed for different scraping tasks.
	"""
	
	file_name, logger, server_type = get_init(__file__)
	
	already_processed_list = get_already_processed('_data/league/')
	
	browser = initiate_browser()
	browser.get(URL)
	sb_week_options = get_sb_week_options(browser)
	
	for item in tqdm(sb_week_options):
		file_path = os.path.join('_data', 'league', f'{item[1]}_q{item[0]}.gzip')
		
		if file_path in already_processed_list:
			continue
		
		process_week_data(browser, item, logger)
	
	browser.close()
	browser.quit()


if __name__ == '__main__':
	main()
