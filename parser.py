from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import pandas as pd
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

def wait_for(condition_function):
  start_time = time.time()
  while time.time() < start_time + 3:
    if condition_function():
      return True
    else:
      time.sleep(0.1)

class wait_for_page_load(object):
  def __init__(self, browser):
    self.browser = browser
  def __enter__(self):
    self.old_page = self.browser.find_element_by_tag_name('html')
  def page_has_loaded(self):
    new_page = self.browser.find_element_by_tag_name('html')
    return new_page.id != self.old_page.id
  def __exit__(self, *_):
    wait_for(self.page_has_loaded)

driver = webdriver.Chrome(executable_path= r'/Users/macos/Documents/chromedriver')
driver.get("https://itdashboard.gov/")


with wait_for_page_load(driver):
  driver.find_element_by_link_text("DIVE IN").click()


price_block = driver.find_element_by_id("agency-tiles-widget")

prices = price_block.find_elements_by_class_name("w900")
names = price_block.find_elements_by_class_name("w200")

list1 = []
list2 = []

for item in prices:
  list1.append(item.text)

for name in names:
  list2.append(name.text)

document = dict(zip(list1, list2))

df = pd.DataFrame(data=document, index=['department'])
df = (df.T)
#print (df)
df.to_excel('dict1.xlsx')
print('DONE')

names[0].click()

driver.implicitly_wait(15)
check = driver.find_element_by_id("investments-table-container")
select = Select(check.find_element_by_class_name("c-select"))
select.select_by_visible_text('All')
driver.implicitly_wait(10)

idd = []
bureau =[]
intitle = []
total = []
typee = []
cio = []
projects = []
time.sleep(10)

rows=1+len(driver.find_elements_by_xpath("/html/body/main/div/div/div/div[4]/div/div/div/div[2]/div/div[1]/div/div/div/div/div[3]/div[2]/table/tbody/tr"))
print(rows)

def get_info(listt, number_of_column):
  for i in range(1,rows):
    element = driver.find_element_by_xpath("/html/body/main/div/div/div/div[4]/div/div/div/div[2]/div/div[1]/div/div/div/div/div[3]/div[2]/table/tbody/tr[" + str(i) + "]/td["+str(number_of_column)+"]")
    listt.append(element.text)
  return listt

get_info(idd,1)
get_info(bureau,2)
get_info(intitle,3)
get_info(total,4)
get_info(typee,5)
get_info(cio,6)
get_info(projects,7)

dict = {'UUI':idd, 'Bureau': bureau, 'Invesment Title': intitle, 'Total FY2021 Spending ($M)': total, 'Type': typee, 'CIO Rating': cio, '# of Projects': projects}
df = pd.DataFrame(dict)
df.to_excel('table2.xlsx')
print('DONE')

links = []
for href in range(1,rows):
  try:
    bit = driver.find_element_by_xpath("/html/body/main/div/div/div/div[4]/div/div/div/div[2]/div/div[1]/div/div/div/div/div[3]/div[2]/table/tbody/tr[" + str(href) + "]/td[1]/a")
    #print(bit.get_attribute("href"))
    links.append(bit.get_attribute("href"))
  except NoSuchElementException:
    continue

for link in links:
  driver.get(link)
  driver.find_element_by_link_text("Download Business Case PDF").click()
  time.sleep(5)

driver.close()