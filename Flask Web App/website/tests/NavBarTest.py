from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import NoSuchElementException
import time

service = Service()
options = webdriver.ChromeOptions()
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
        EC.presence_of_element_located((By.ID, 'recommender'))
    )
recom = driver.find_element(By.ID, 'recommender')
recom.click()
if WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'MuscleGroup'))):
    if WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'Equipment'))):
        print("Successfully Entered Recommender")
    else:
        print("Failed to Enter Recommended")
        
time.sleep(5)
WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'calendar'))
    )
calen = driver.find_element(By.ID, 'calendar')
calen.click()
if WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'calendarContainer'))):
        print("Successfully Entered Calendar")
else:
    print("Failed to Enter Calendar")

time.sleep(5)
WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'home'))
    )
hom = driver.find_element(By.ID, 'home')
hom.click()
if WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'container'))):
        print("Successfully Entered Home")
else:
    print("Failed to Enter Home")

time.sleep(5)
WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'workout'))
    )
wOut = driver.find_element(By.ID, 'workout')
wOut.click()
if WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'addExerciseButton'))):
        print("Successfully Entered Workout Page")
else:
    print("Failed to Enter Workout Page")

time.sleep(5)
WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'logout'))
    )
logOut = driver.find_element(By.ID, 'logout')
logOut.click()
if WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'email'))):
    if WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'password'))):
        print("Successfully Logged Out")
else:
    print("Failed to Log Out")
time.sleep(6)