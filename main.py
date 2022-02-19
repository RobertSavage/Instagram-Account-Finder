from selenium import webdriver
from time import sleep
import urllib.request
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
import bs4
import webbrowser
from selenium.webdriver.common.by import By
import random
import datetime as dt
from concurrent.futures import ThreadPoolExecutor, as_completed


class BOT():
	def __init__(self):
		mobile_emulation = { "deviceName": "iPhone 6" }
		chrome_options = webdriver.ChromeOptions()
		#chrome_options.add_argument("--headless") 
		chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
		self.driver = webdriver.Chrome(executable_path=r'chromedriver.exe', chrome_options=chrome_options)

	def scrape(self,hashtag):
		self.driver.get('https://www.instagram.com/explore/tags/'+str(hashtag))
		sleep(2)
		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		sleep(2) 
		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		sleep(2)
		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		sleep(2)
		final_hrefs = []
		photos =[]
		inital_time = dt.datetime.now()
		counter = 1

		hrefs_in_view = self.driver.find_elements_by_tag_name('a')
		for href in hrefs_in_view:
			if href not in final_hrefs:
				final_hrefs.append(href)

		for pic in final_hrefs:
			temp = pic.get_attribute('href')
			if "/p/" in temp:
				photos.append(temp)

		photos_no_top_post = photos[9:]
		print('POST RECIVED FOR '+str(hashtag)+' ',len(photos_no_top_post))
		print('FILTERING...')
		for photo in photos_no_top_post:
			try:
				self.driver.get(photo)
				sleep(2)
				getname = self.driver.find_element_by_css_selector('#react-root > section > main > div > div > article > div.eo2As > div.Igw0E.IwRSH.eGOV_._4EzTm > div > div > a')
				name = getname.get_attribute('text')
				self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				sleep(2)
				gototaccount = self.driver.find_element_by_css_selector('#react-root > section > main > div > div > article > div.eo2As > div.Igw0E.IwRSH.eGOV_._4EzTm > div > div > a')
				gototaccount.click()
				sleep(2)
				followerstag = self.driver.find_element_by_css_selector('#react-root > section > main > div > ul > li:nth-child(2) > a')
				followers = followerstag.get_attribute('text').split()[0]
				f1 = followers.replace(',','')
				f2 = f1.replace('.','')
				f3 = f2.replace('k','000')
				with open(str(hashtag)+'.txt', "a") as chkc:
					chkc.write(str(name)+','+str(fixed)+"\n")
			except:
				continue
		print('DONE WITH: '+str(hashtag))
	def close(self):
		self.driver.quit()

hashtags = ['skate','streetwear']
BOT = BOT()
for i in range(25):
	for hashtag in hashtags:
		BOT.scrape(hashtag)
	print('END OF CYCLE: ', i+1)
