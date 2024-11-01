import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# Define the path to the ChromeDriver
chrome_driver_path = '/Users/jinwoopark/chromedriver'  # Update this path accordingly

# Create a Service object and pass it to the Chrome WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Open the login page
driver.get("https://etk.srail.kr/cmc/01/selectLoginForm.do?pageId=TK0701000000")

# Function to perform initial login
def perform_initial_login():
    try:
        # Wait for the login page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "srchDvCd3"))
        )

        # Click the 전화번호 button
        phone_checkbox = driver.find_element(By.ID, "srchDvCd3")
        phone_checkbox.click()

        # Enter the phone number into the 전화번호 input field
        phone_input = driver.find_element(By.ID, "srchDvNm03")
        phone_input.clear()
        phone_input.send_keys("Phone number")  # Input phone number in "000-0000-0000" format

        # Enter the password into the 비밀번호 input field
        password_input = driver.find_element(By.ID, "hmpgPwdCphd03")
        password_input.clear()
        password_input.send_keys("Password")  # Input password

        print("Login credentials entered. Please click the '확인' button and navigate to the '일반승차권 조회' page manually.")
    except Exception as e:
        print(f"Error during initial login: {e}")

# Function to set up departure, arrival information
def set_search_criteria():
    try:
        # Wait for the search form to load on the desired page
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "search-form"))
        )

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
        date_select.select_by_value("20240917")  # Input date in YYYYMMDD format

        # Select the time
        time_select = Select(driver.find_element(By.ID, "dptTm"))
        time_select.select_by_value("160000")  # Input time in HHMMSS format e.g. 160000

        # Select 1 adult passenger
        passenger_select = Select(driver.find_element(By.NAME, "psgInfoPerPrnb1"))
        passenger_select.select_by_value("1")  # Replace with the number of passengers

        print("Search criteria set: Departure (동대구), Arrival (수서), Date (2024/09/17), Time (16시), Passengers (1 adult)")
    except Exception as e:
        print(f"Error setting search criteria: {e}")

# Function to click the 조회하기 button to search for trains
def click_search_button():
    try:
        # Wait for the 조회하기 button to be clickable
        조회하기_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="조회하기"]'))
        )
        조회하기_button.click()
        print("조회하기 button clicked to search for trains.")
    except Exception as e:
        print(f"Error clicking 조회하기 button: {e}")

# Function to check for 예약하기 buttons and click the earliest one
def check_for_reservation_button():
    try:
        # Wait for the search results to load
        tbody = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//tbody'))
        )

        # Get all 예약하기 buttons under 일반실 column
        reservation_buttons = driver.find_elements(By.CSS_SELECTOR, 'td:nth-child(7) a.btn_small.btn_burgundy_dark')

        # Iterate through the buttons and check for the "예약하기" text
        for button in reservation_buttons:
            span_element = button.find_element(By.TAG_NAME, "span")
            if span_element.text.strip() == "예약하기":
                # Scroll the button into view
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                # Wait until the button is clickable
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
                # Click the parent <a> element
                button.click()
                print("Earliest 예약하기 button found and clicked!")
                return True  # Stop checking after clicking the earliest button
        print("No 예약하기 buttons found under 일반실 column.")
    except Exception as e:
        print(f"Error occurred during reservation check: {e}")

    return False

# Perform initial login
perform_initial_login()

# Wait for manual navigation to the 일반승차권 조회 page
try:
    # Wait until the URL matches the desired page
    desired_url = "https://etk.srail.kr/hpg/hra/01/selectScheduleList.do?pageId=TK0101010000"
    print(f"Please navigate to {desired_url} manually.")
    WebDriverWait(driver, 300).until(
        EC.url_to_be(desired_url)
    )
    print("Desired page reached. Proceeding with setting search criteria.")
except Exception as e:
    print(f"Error waiting for the desired page: {e}")
    driver.quit()
    exit()

# Set search criteria: departure, arrival, date, time, and passenger count
set_search_criteria()

# Continuously check for 예약하기 buttons
try:
    while True:
        # Click the 조회하기 button to refresh the search results
        click_search_button()
        # Wait for a short period to ensure results are loaded
        time.sleep(2)
        found = check_for_reservation_button()
        if found:
            # Keep the browser window open for manual interaction
            print("예약하기 button clicked. Keeping browser window open for manual interaction.")
            input("Press Enter to exit the script and close the browser.")
            break
        else:
            print("No 예약하기 buttons found. Retrying...")
            # Generate a random delay between 0.5 to 0.9 seconds
            delay = random.uniform(0.5, 0.8)
            print(f"Waiting for {delay:.2f} seconds before retrying.")
            time.sleep(delay)  # Sleep for the randomly chosen delay
except Exception as e:
    print(f"An unexpected error occurred: {e}")