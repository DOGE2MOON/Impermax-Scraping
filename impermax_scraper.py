import time
import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import pandas as pd
import gspread
from gspread_pandas import Spread, Client

# IF YOU LACK THE ABOVE LIBRARIES, INSTALL VIA THE FOLLOWING COMMANDS
# pip3 install selenium
# pip3 install pandas
# pip3 install gspread
# pip3 install gspread_pandas
# if you encounter errors with the chrome webdriver version, download a driver compatible with your chrome version from: https://chromedriver.chromium.org/home
# then, edit /selenium/webdriver/chrome/webdriver.py to point to the chrome driver file you just downloaded

# obtain user input and pass it into a variable, ensuring that the URL loads correctly
print("Please type the FULL name of the chain you wish to scrape (ex: Polygon)")
txt = input("Desired Chain: ")
# to save time, you can hardcode this value in line #89 where email is reference and remove the input from line #22
email = input("Gmail Account to Share Output: ") 

if txt == "Ethereum":
	txt = "app"
else:
	txt = txt
if txt == "ethereum":
	txt = "app"
else:
	txt = txt
url = 'https://' + txt + ".impermax.finance"

# load the driver and webpage
driver = webdriver.Chrome()
driver.get(url)
# sleep so that the webpage can load
time.sleep(5)

# intialize variables
df = pd.DataFrame()
pairs = []
rates1 = []
rates2 = []
br1 = []
br2 = []

# fetch the length of the rates table
numrows = len(driver.find_elements_by_css_selector("a[class='row pairs-table-row']"))

# fetch values and iterate over the whole table
for b in range(1,numrows):
	
	# find name, lending rates, and borrow rates for coin1
	coin1 = driver.find_element_by_xpath('//*[@id="impermax-app"]/div/div/div/div[2]/div[4]/div/div/div/div/div/a[%d]/div[1]/div/div[2]/div[1]' %b)
	apr1 = driver.find_element_by_xpath('//*[@id="impermax-app"]/div/div/div/div[2]/div[4]/div/div/div/div/div/a[%d]/div[4]/div[1]' %b)
	borrow1 = driver.find_element_by_xpath('//*[@id="impermax-app"]/div/div/div/div[2]/div[4]/div/div/div/div/div/a[%d]/div[5]/div[1]' %b)
	
	# find name and lending rates of coin2
	coin2 = driver.find_element_by_xpath('//*[@id="impermax-app"]/div/div/div/div[2]/div[4]/div/div/div/div/div/a[%d]/div[1]/div/div[2]/div[2]' %b)
	apr2 = driver.find_element_by_xpath('//*[@id="impermax-app"]/div/div/div/div[2]/div[4]/div/div/div/div/div/a[%d]/div[4]/div[2]' %b)
	borrow2 = driver.find_element_by_xpath('//*[@id="impermax-app"]/div/div/div/div[2]/div[4]/div/div/div/div/div/a[%d]/div[5]/div[2]' %b)
	
	# append values to a list because Pandas is annoying
	pairs.append(coin1.text + " - " + coin2.text)
	rates1.append(apr1.text)
	rates2.append(apr2.text)
	br1.append(borrow1.text)
	br2.append(borrow2.text)

# add list values to dataframe
df['Pair'] = pairs
df['Coin 1 Supply Rate'] = rates1
df['Coin 2 Supply Rate'] = rates2
df['Coin 1 Borrow Rate'] = br1
df['Coin 2 Borrow Rate'] = br2

# appropriately name files and export locally before trying Google Sheets
if txt == "app":
	txt = "Ethereum"
else:
	txt = txt
name = txt + " scraping results.csv"
df.to_csv(name, encoding='utf-8')

# export values and share to Google Sheets
gc = gspread.service_account(filename='PATH_TO_GOOGLE_SHEETS_API.json')
sh = gc.create("Impermax Scraping Data")
sh = gc.open('Impermax Scraping Data')
sh.share(email, perm_type='user', role='writer')
sh = sh.get_worksheet(0)
sh.update([df.columns.values.tolist()] + df.values.tolist())

