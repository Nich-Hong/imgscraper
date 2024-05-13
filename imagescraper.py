from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import sys
import os

def launch_scraper(webpage):
  options = webdriver.ChromeOptions()
  options.add_argument("--incognito")
  options.add_experimental_option("detach",True)
  driver = webdriver.Chrome(options = options)
  driver.set_window_size(100,100)
  driver.get(webpage)
  src_list = []
  try:
      body = WebDriverWait(driver, 10).until(
          EC.presence_of_all_elements_located((By.TAG_NAME, "img"))
      )
      for i in body:
        src_list.append(i.get_attribute('src'))
  finally:
      driver.quit()
  return src_list

def extract_name(url): 
      file_name = url.split("/")[-1]
      return file_name

def download_img(srcs, download_fld):
  for src in srcs:
    print("File: "+src)
    res = requests.get(src)
    with open(download_fld+'\\'+extract_name(src),'wb') as f:
      f.write(res.content) 

if __name__ == "__main__":
  #command format: python imgscraper.py "https://google.com" [file_destination]
  print(sys.argv)
  webpage = sys.argv[1]
  if len(sys.argv) > 2:
    folder = sys.argv[2]
  else:
    folder = os.getcwd()+r'\\imgscraped'
    if not os.path.exists(folder):
      os.makedirs(folder)
  try:
    src_list = launch_scraper(webpage)
    download_img(src_list, folder)
    print("Finished file downloads")
  except:
     print("Invalid arguments")