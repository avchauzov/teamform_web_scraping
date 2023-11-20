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
- process_week_data(_browser, _item, _logger): Process data for a specific week.
- main(): Main function for web scraping TeamForm website data.

Example:
```python
if __name__ == "__main__":
    main()
"""

import os.path
import sys
import time

import pandas as pd
from selenium.webdriver.common.by import By
from tqdm import tqdm

from _functions import get_already_processed, get_init, get_sb_week_options, initiate_browser, log_error, PAGES_NUMBER, SIMPLE_URL, URL


def process_week_data(_browser, _item, _logger):
	"""
	Process data for a specific week.
	
	Parameters:
	- _browser (selenium.webdriver.Chrome): An instance of the Chrome browser.
	- _item (Tuple[int, int]): A tuple representing quarter and week number.
	- _logger (logging.Logger): Logger instance for error logging.
	"""
	
	try:
		_browser.get(f'{SIMPLE_URL}{_item[1]}/q{_item[0]}')
		
		for _ in range(PAGES_NUMBER):
			
			try:
				load_more_button = _browser.find_element(By.XPATH, '//*[@id="rankBtn"]')
				_browser.execute_script("arguments[0].click();", load_more_button)
				time.sleep(17)
			
			except Exception as error:
				log_error(error, _logger)
				break
		
		table = _browser.find_element(By.XPATH, '//*[@id="rankTable"]')
		rows_list = table.find_elements(By.TAG_NAME, 'tr')[1:]
		data = []
		
		for row_value in rows_list:
			values_list = row_value.find_elements(By.TAG_NAME, 'td')
			values_list = [value.text.strip() for value in values_list]
			data.append(values_list[3: 6])
		
		df = pd.DataFrame(data, columns=['league', 'country', 'value']).drop_duplicates()
		df.to_parquet('_data/league/' + '_'.join([f'{_item[1]}', f'q{_item[0]}']) + '.gzip')
	
	except Exception as error:
		log_error(error, _logger)
		sys.exit(0)


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
