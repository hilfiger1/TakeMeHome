import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service

# Define the path to the ChromeDriver
chrome_driver_path = '/Users/jinwoopark/chromedriver'

# Create a Service object and pass it to the Chrome WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Open the webpage
driver.get("https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000")

# Function to set up the form with the correct stations, date, time, and passenger count
def set_search_criteria():
    # Input for Departure Station
    dpt_station_input = driver.find_element(By.ID, "dptRsStnCdNm")
    dpt_station_input.clear()
    dpt_station_input.send_keys("동대구")  # Input departure station name
    
    # Input for Arrival Station
    arv_station_input = driver.find_element(By.ID, "arvRsStnCdNm")
    arv_station_input.clear()
    arv_station_input.send_keys("수서")  # Input arrival station name

    # Select the date
    date_select = Select(driver.find_element(By.ID, "dptDt"))
    date_select.select_by_value("Date")  # Input the date in YYYYMMDD format
    
    # Select the time
    time_select = Select(driver.find_element(By.ID, "dptTm"))
    time_select.select_by_value("Time")  # Input the time in HHMMSS format e.g. "160000"

    # Select number of passengers
    passenger_select = Select(driver.find_element(By.NAME, "psgInfoPerPrnb1"))
    passenger_select.select_by_value("1")  # Select 2 adults
    
    print("Search criteria set: Departure (동대구), Arrival (수서), Date (2024/10/09), Time (16시), Passengers (2 adults)")

# Function to check for 예약하기 buttons and click the earliest one
def check_for_reservation_button():
    try:
        # Click the 조회하기 button to search for trains
        조회하기_button = driver.find_element(By.CSS_SELECTOR, 'input[value="조회하기"]')
        조회하기_button.click()

        # Wait for results to load
        time.sleep(2)

        # Get all 예약하기 buttons
        reservation_buttons = driver.find_elements(By.CSS_SELECTOR, 'a.btn_small.btn_burgundy_dark span')  # Find all 예약하기 buttons

        # Iterate through the buttons and check for the "예약하기" text
        for button in reservation_buttons:
            if button.text == "예약하기":
                # Click the first (earliest) 예약하기 button and notify the user
                button.click()
                print("Earliest 예약하기 button found and clicked!")
                fill_login_info()
                return True  # Stop checking after clicking the earliest button
    except Exception as e:
        print(f"Error occurred: {e}")

    return False

# Function to fill 전화번호 and 비밀번호 and click the 확인 button
def fill_login_info():
    try:
        # Click the 휴대전화번호 checkbox
        phone_checkbox = driver.find_element(By.ID, "srchDvCd3")
        phone_checkbox.click()

        # Enter the phone number into the 전화번호 input field
        phone_input = driver.find_element(By.ID, "srchDvNm03")
        phone_input.clear()
        phone_input.send_keys("Your phone number") # Fill in 전화번호

        # Enter the password into the 비밀번호 input field
        password_input = driver.find_element(By.ID, "hmpgPwdCphd03")
        password_input.clear()
        password_input.send_keys("Your password")

        # Click the 확인 button
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.submit.btn_pastel2.loginSubmit'))
        )
        confirm_button.click()

        print("휴대전화번호 and 비밀번호 entered, and 확인 button clicked!")
    except Exception as e:
        print(f"Error during login process: {e}")

# Set search criteria: departure, arrival, date, time, and passenger count
set_search_criteria()

# Continuously check for 예약하기 buttons
while True:
    found = check_for_reservation_button()
    if found:
        # Keep the browser window open for user interaction
        print("예약하기 button clicked. Keeping browser window open for manual interaction.")
        input("Press Enter to exit the script and close the browser.")
        break
    else:
        print("No 예약하기 buttons found. Refreshing...")

        # Generate a random delay between 0.5 to 3 seconds
        delay = random.uniform(0.5, 0.9)
        print(f"Waiting for {delay:.2f} seconds before refreshing.")
        time.sleep(delay)  # Sleep for the randomly chosen delay