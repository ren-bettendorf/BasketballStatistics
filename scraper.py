import json
import requests
from pprint import pprint
from bs4 import BeautifulSoup

def scrapeURL(url):

	# Get HTML and table to scrap from url
	response = requests.get(url)
	html = response.content
	soup = BeautifulSoup(html, "html.parser")
	table = soup.find('table', attrs={'id': 'stat-table'})
	
	# Sets up Header values to be used later
	header = []
	tableData = {}
	for key in table.find_all('tr'):
		header = key.text.split('\n')
		tableData.setdefault(key.text, [])
	header = [string for string in header if string != ""]


	# Updates the lists in TableData with the correct data and removes the random non-ASCII values that are found for all-star
	for row in table.find_all(attrs={'class':'salary-row'}):
		for i, cell in enumerate(row.findAll('td')):
			tableData[header[i]].append(cell.text.replace("\xa0★", ""))
			
	# Creates JSON String with players firstname + lastname + stats for where JSON file location
	json_string = json.dumps(tableData, indent=4)
	playerName = soup.find('div', attrs={'id': 'info_box'}).h1.text
	
	
	# Returns File Location and header values for Table
	return [json_string, header, playerName]


scrapeURL("https://swishanalytics.com/optimus/nba/daily-fantasy-salary-changes")