"""
This script performs web scraping to retrieve data from the TeamForm website.
It initializes logging, retrieves links and processed files, and uses a headless Chrome browser
to navigate through the website, collecting data for each specified quarter and week.

Functions:
- get_link(link_type): Retrieve a link from 'links.json' based on the specified type.
- get_init(file_name): Initialize logging and retrieve file name, logger, and server type.
- get_already_processed(path): Retrieve a list of files that have already been processed within the specified path.
- initiate_browser(): Initialize and configure a headless Chrome browser with specific options.
- get_sb_week_options(browser): Retrieve and parse options from the "sbWeek" dropdown in a given browser.
- log_error(error, logger): Log errors using the logger.
- process_week_data(browser, item, logger): Process data for a specific week.

Usage:
- Run the script to perform web scraping and collect data from the TeamForm website.
- Ensure the necessary dependencies and the Chrome browser are installed.
- Modify URLs and file paths as needed for different scraping tasks.
"""

import datetime
import json
import logging
import os
import sys
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pandas as pd
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


#

URL = 'https://www.teamform.com/en/league-ranking/world/2023/q3'
SIMPLE_URL = 'https://www.teamform.com/en/league-ranking/world/'
PAGES_NUMBER = 17


#

def get_link(link_type: str) -> str:
	"""
	Retrieve a link from the 'links.json' file based on the specified type.

	Parameters:
	- link_type (str): The type of link to retrieve.

	Returns:
	- str: The corresponding link if found, or an empty string if the type is not present in the 'links.json' file.
	"""
	with open('_credentials/links.json') as file:
		return json.load(file).get(link_type, '')


def get_init(file_name):
	"""
	Initialize logging and retrieve file name, logger, and server type.
	
	Parameters:
	- file_name (str): The name of the file being processed.
	
	Returns:
	- Tuple[str, logging.Logger, str]: A tuple containing the processed file name, logger instance, and server type.
	
	Example:
	file_name, logger, server_type = get_init('example_file.py')
	'example_file', <Logger>, 'development'
	"""
	server_type = None
	try:
		os_name = os.uname()
		if os_name[0] == 'Linux':
			server_type = 'production'
	
	except AttributeError as _:
		server_type = 'development'
	
	if '\\' in file_name:
		file_name = file_name.split('\\')[-1].replace('.py', '').strip()
	
	elif '/' in file_name:
		file_name = file_name.split('/')[-1].replace('.py', '').strip()
	
	else:
		file_name = file_name.replace('.py', '').strip()
	
	#
	
	'''if psutil.Process(os.getpid()).ppid() == 1 and os.path.exists(f'_logs/{file_name}.log'):
		os.unlink(f'_logs/{file_name}.log')'''
	
	if os.path.exists(f'_logs/{file_name}.log'):
		os.unlink(f'_logs/{file_name}.log')
	
	handler = RotatingFileHandler(f'_logs/{file_name}.log', maxBytes=10 * 1024 * 1024, backupCount=3, delay=0, mode='w+')
	logger = logging.getLogger('root')
	logger.setLevel(logging.INFO)
	logger.addHandler(handler)
	
	return file_name, logger, server_type


def get_already_processed(path):
	"""
	Retrieve a list of files that have already been processed within the specified path.
	
	Parameters:
	- path (str): The base path to search for processed files.
	
	Returns:
	- List[str]: A list of file names (without the '.gzip' extension) that have already been processed.
	
	Example:
	get_already_processed('/path/to/files')
	['file1', 'file2', 'file3']
	"""
	already_processed_list = []
	for path in Path(path).glob('**/*.gzip'):
		already_processed_list.append(str(path).split('\\')[-1].replace('.gzip', ''))
	
	return already_processed_list


def initiate_browser():
	"""
	Initialize and configure a headless Chrome browser with specific options.
	
	Returns:
	- selenium.webdriver.Chrome: An instance of a configured Chrome browser.
	
	Example:
	browser = initiate_browser()
	"""
	options = Options()
	
	options.add_argument('--kiosk')
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-gpu')
	options.add_argument('--headless=new')
	options.add_argument('--disk-cache-size=0')
	options.add_argument('window-size=1920,1080')
	options.add_argument('--disable-dev-shm-usage')
	options.add_argument(
			'--proxy-server=' + get_link('scraperapi').replace('url=', 'render=true')
			)
	
	browser = webdriver.Chrome(options=options)
	browser.set_script_timeout(30)
	
	return browser


def get_sb_week_options(browser):
	"""
	Retrieve and parse options from the "sbWeek" dropdown in a given browser.
	
	Parameters:
	- browser (selenium.webdriver.Chrome): An instance of the Chrome browser.
	
	Returns:
	- List[Tuple[int, int]]: A list of tuples representing week options sorted by quarter and week number.
	
	Example:
	browser = initiate_browser()
	options = get_sb_week_options(browser)
	[(1, 1), (1, 2), (2, 1), ...]
	"""
	sb_week_select = Select(browser.find_element(By.XPATH, '//*[@id="sbWeek"]'))
	
	temp_array = sb_week_select.options
	sb_week_options = [value.accessible_name for value in temp_array]
	sb_week_options = [value.split(' - ') for value in sb_week_options]
	sb_week_options = [(int(value[0].replace('Q', '')), int(value[1])) for value in sb_week_options]
	
	return sorted(sb_week_options, key=lambda value: (value[1], value[0]))


def log_error(error, logger):
	"""
	Log errors using the logger.
	
	Parameters:
	- error (Exception): The exception object.
	- logger (logging.Logger): Logger instance for error logging.
	"""
	_type, _obj, _tb = sys.exc_info()
	file_name = os.path.split(_tb.tb_frame.f_code.co_filename)[1]
	
	error_string = '; '.join([str(datetime.datetime.now()), ' <<>> '.join([str(value) for value in [error, _type, file_name, _tb.tb_lineno]]), __name__])
	logger.info(error_string)


def process_week_data(browser, item, logger):
	"""
	Process data for a specific week.

	Parameters:
	- browser (selenium.webdriver.Chrome): An instance of the Chrome browser.
	- item (Tuple[int, int]): A tuple representing quarter and week number.
	- logger (logging.Logger): Logger instance for error logging.
	"""
	try:
		browser.get(f'{SIMPLE_URL}{item[1]}/q{item[0]}')
		
		for _ in range(PAGES_NUMBER):
			
			try:
				load_more_button = browser.find_element(By.XPATH, '//*[@id="rankBtn"]')
				browser.execute_script("arguments[0].click();", load_more_button)
				time.sleep(17)
			
			except Exception as error:
				log_error(error, logger)
				break
		
		table = browser.find_element(By.XPATH, '//*[@id="rankTable"]')
		rows_list = table.find_elements(By.TAG_NAME, 'tr')[1:]
		data = []
		
		for row_value in rows_list:
			values_list = row_value.find_elements(By.TAG_NAME, 'td')
			values_list = [value.text.strip() for value in values_list]
			data.append(values_list[3: 6])
		
		df = pd.DataFrame(data, columns=['league', 'country', 'value']).drop_duplicates()
		df.to_parquet('_data/league/' + '_'.join([f'{item[1]}', f'q{item[0]}']) + '.gzip')
	
	except Exception as error:
		log_error(error, logger)
		sys.exit(0)
