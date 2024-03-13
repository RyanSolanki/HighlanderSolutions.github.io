from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException
import time

service = Service()
#options = webdriver.ChromeOptions()
driver = webdriver.Chrome()

driver.get('http://127.0.0.1:5000')

WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )
emailInput = driver.find_element(By.ID, 'email')
emailInput.clear()
emailInput.send_keys('tim@gmail.com')
time.sleep(5)
passwordInput = driver.find_element(By.ID, 'password')
passwordInput.clear()
passwordInput.send_keys('1234567' + Keys.ENTER)
time.sleep(5)
WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'logout'))
    )
logout = driver.find_element(By.ID, 'logout')
logout.click()
time.sleep(6)
if WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID,'login'))):
    print('Successfully Logged Out')
else:
    print('Failed to Log Out')
driver.quit()