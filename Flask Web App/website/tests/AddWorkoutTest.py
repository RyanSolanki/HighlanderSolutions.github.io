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
time.sleep(4)
emailInput = driver.find_element(By.ID, 'email')
emailInput.clear()
emailInput.send_keys('tim@gmail.com')
time.sleep(5)
passwordInput = driver.find_element(By.ID, 'password')
passwordInput.clear()
passwordInput.send_keys('1234567' + Keys.ENTER)

time.sleep(5)
WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'workout'))
    )
wOut = driver.find_element(By.ID, 'workout')
wOut.click()
if WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'addExerciseButton'))):
        print('Successfully Entered Workout Page')
else:
    print('Failed to Enter Workout Page')
    
time.sleep(5)
selectExercise = driver.find_element(By.ID, 'addExerciseButton')
selectExercise.click()

time.sleep(2)
selectExercise = driver.find_element(By.CLASS_NAME, 'list-group-item')
selectExercise.click()

time.sleep(2)
selectExercise = driver.find_element(By.CLASS_NAME, 'close')
selectExercise.click()

time.sleep(3)
button_text = 'Exercise Info'
exerciseInfo = driver.find_element(By.XPATH, f"//button[text()='{button_text}']")
exerciseInfo.click()
time.sleep(3)
WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'sets'))
    )
selectSets = driver.find_element(By.ID, 'sets')
selectSets.clear()
selectSets.send_keys('1' + Keys.ENTER)
time.sleep(2)

#Access Exercise Info Reps TextBox
WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"//input[@placeholder='{'Reps for set 1'}']"))
    )
selectReps = driver.find_element(By.XPATH, f"//input[@placeholder='{'Reps for set 1'}']")
selectReps.send_keys('10' + Keys.ENTER)
time.sleep(3)
#Access Exercise Infor Weight TextBox
WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"//input[@placeholder='{'Weight for set 1'}']"))
    )
selectSets = driver.find_element(By.XPATH, f"//input[@placeholder='{'Weight for set 1'}']")
#selectSets.click()
selectSets.send_keys('15' + Keys.ENTER)
time.sleep(2)
selectSets = driver.find_element(By.ID, 'modalButton')
selectSets.click()

time.sleep(2)
WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'workoutName'))
    )

time.sleep(4)
selectName = driver.find_element(By.ID,'workoutName')
selectName.clear()
selectName.send_keys('Chest Workout')


time.sleep(3)
WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'submitWorkoutButton'))
    )
submit = driver.find_element(By.ID, 'submitWorkoutButton')
submit.click()
time.sleep(10)
if(WebDriverWait(driver), 5).until(EC.presence_of_all_elements_located((By.XPATH, f"//button[text()='{}']"))):
    print('Successfully created exercise')
else:
    print('Failed to create exercise')
driver.quit()