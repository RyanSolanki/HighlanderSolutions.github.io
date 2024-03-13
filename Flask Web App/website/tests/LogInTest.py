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

def emailEntry():
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )
    inputElement = driver.find_element(By.ID, 'email')
    
    emailList = ['tim', 'tim12', 'tim@gmail.com', '93bill', '@Tim@', 'ewgrwg3f@yah.com']
    
    for index, email in enumerate(emailList):
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'email'))
        )
        inputElement.clear()
        inputElement.send_keys(email)
        time.sleep(1)  # Add a short delay to allow the text field to update
        
        emailText = driver.find_element(By.ID, 'email')
        text = emailText.get_attribute('value')
        
        if '@' not in text or text.count('@') != 1:
            print(f'{email} is an invalid email address')
        else:
            print(f'{email} is a valid email address')
        
        time.sleep(1)
    time.sleep(2)


def loginTest():
    driver.get('http://127.0.0.1:5000')
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, 'email'))
    )
    
    email = 'tim@gmail.com'
    password = '1234567'
    
    inputElement = driver.find_element(By.ID, 'email')
    passwordElement = driver.find_element(By.ID, 'password')
    
    inputElement.clear()
    inputElement.send_keys(email)
    
    passwordElement.clear()
    passwordElement.send_keys(password + Keys.ENTER)
    
    time.sleep(2)  # Add a short delay to allow the text field to update
    
    try:
        # Locate the success message element after the page reloads
        success = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert.alert-success.alter-dismissable.fade.show'))
        )
        print(success.text)
        if 'Logged in successfully!' in success.text:
            print('Login Successful')
        else:
            print('Login Unsuccessful')
            inputElement.clear()
    except NoSuchElementException:
        print('Login Unsuccessful: No success message found')
    
    time.sleep(2)  # Optional delay between iterations
    
    time.sleep(3)
    
emailEntry()
loginTest()
driver.quit