import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Initialize Chrome using Selenium Manager (no manual driver path needed)
opts = Options()
# If Chrome is in a non-standard location, uncomment and set the path below:
# opts.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
driver = webdriver.Chrome(options=opts)

# Open the login page
driver.get("https://etk.srail.kr/cmc/01/selectLoginForm.do?pageId=TK0701000000")

# Function to perform initial login
def perform_initial_login():
    try:
        # Wait for the login page to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "srchDvCd3"))
        )

        def find_first_present(by, ids):
            for element_id in ids:
                try:
                    return driver.find_element(by, element_id)
                except Exception:
                    continue
            raise Exception(f"None of the elements found for IDs: {ids}")

        print("Choose login method: 1) 회원번호  2) 이메일  3) 휴대전화번호")
        method = input("Enter 1, 2, or 3: ").strip()

        if method == "1":
            # 회원번호
            # Click 회원번호 option
            find_first_present(By.ID, ["srchDvCd1"]).click()
            member_no = input("Enter 회원번호 (e.g., 12345678): ").strip()
            password = input("Enter password (e.g., MySecurePass123!): ").strip()

            # Fill ID and password
            id_input = find_first_present(By.ID, ["srchDvNm01"])  # 회원번호 입력
            id_input.clear()
            id_input.send_keys(member_no)

            pwd_input = find_first_present(By.ID, ["hmpgPwdCphd01", "hmpgPwdCphd", "hmpgPwdCphd03", "hmpgPwdCphd02"])  # try common IDs
            pwd_input.clear()
            pwd_input.send_keys(password)

        elif method == "2":
            # 이메일
            find_first_present(By.ID, ["srchDvCd2"]).click()
            email = input("Enter email (e.g., user@example.com): ").strip()
            password = input("Enter password (e.g., MySecurePass123!): ").strip()

            id_input = find_first_present(By.ID, ["srchDvNm02"])  # 이메일 입력
            id_input.clear()
            id_input.send_keys(email)

            pwd_input = find_first_present(By.ID, ["hmpgPwdCphd02", "hmpgPwdCphd", "hmpgPwdCphd03", "hmpgPwdCphd01"])  # try common IDs
            pwd_input.clear()
            pwd_input.send_keys(password)

        else:
            # 휴대전화번호 (default)
            find_first_present(By.ID, ["srchDvCd3"]).click()
            phone = input("Enter phone number (e.g., 010-1234-5678): ").strip()
            password = input("Enter password (e.g., MySecurePass123!): ").strip()

            phone_input = find_first_present(By.ID, ["srchDvNm03"])  # 전화번호 입력
            phone_input.clear()
            phone_input.send_keys(phone)

            pwd_input = find_first_present(By.ID, ["hmpgPwdCphd03", "hmpgPwdCphd", "hmpgPwdCphd02", "hmpgPwdCphd01"])  # try common IDs
            pwd_input.clear()
            pwd_input.send_keys(password)

        print("Login credentials entered. Please click the '확인' button and navigate to the '일반승차권 조회' page manually.")
    except Exception as e:
        print(f"Error during initial login: {e}")

# Function to set up departure, arrival information
def set_search_criteria(dpt_station_name, arv_station_name, date_yyyymmdd, time_hhmmss, num_adult_passengers):
    try:
        # Wait for the search form to load on the desired page
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "search-form"))
        )

        # Input for Departure Station
        dpt_station_input = driver.find_element(By.ID, "dptRsStnCdNm")
        dpt_station_input.clear()
        dpt_station_input.send_keys(dpt_station_name)  # Input departure station name

        # Input for Arrival Station
        arv_station_input = driver.find_element(By.ID, "arvRsStnCdNm")
        arv_station_input.clear()
        arv_station_input.send_keys(arv_station_name)  # Input arrival station name

        # Select the date
        date_select = Select(driver.find_element(By.ID, "dptDt"))
        date_select.select_by_value(date_yyyymmdd)  # Input date in YYYYMMDD format

        # Select the time
        time_select = Select(driver.find_element(By.ID, "dptTm"))
        time_select.select_by_value(time_hhmmss)  # Input time in HHMMSS format e.g. 160000

        # Select 1 adult passenger
        passenger_select = Select(driver.find_element(By.NAME, "psgInfoPerPrnb1"))
        passenger_select.select_by_value(str(num_adult_passengers))  # Replace with the number of passengers
        print(f"Search criteria set: Departure ({dpt_station_name}), Arrival ({arv_station_name}), Date ({date_yyyymmdd}), Time ({time_hhmmss}), Passengers ({num_adult_passengers} adult)")
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

# Function to check for 예약하기 buttons and click the correct time
def check_for_reservation_button(requested_time):
    try:
        # Wait for the search results to load
        tbody = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//tbody'))
        )

        # Get all 예약하기 buttons by looking for any link with "예약하기" text
        reservation_buttons = driver.find_elements(By.XPATH, "//a[.//span[contains(text(), '예약하기')]]")

        # Iterate through the buttons and check for the "예약하기" text
        print(f"Found {len(reservation_buttons)} potential reservation buttons")
        for i, button in enumerate(reservation_buttons):
            try:
                # Try to find span element and check text
                span_element = button.find_element(By.TAG_NAME, "span")
                button_text = span_element.text.strip()
                print(f"Button {i+1} text: '{button_text}'")
                
                if "예약하기" in button_text:
                    # Find the departure time for this train row
                    train_row = button.find_element(By.XPATH, "./ancestor::tr")
                    time_element = train_row.find_element(By.CSS_SELECTOR, "em.time")
                    departure_time = time_element.text.strip()
                    print(f"Button {i+1} departure time: '{departure_time}'")
                    
                    # Check if this time matches the requested time
                    # Convert requested time from HHMMSS to HH:MM format for comparison
                    requested_hhmm = f"{requested_time[:2]}:{requested_time[2:4]}"
                    print(f"Comparing: found time '{departure_time}' with requested time '{requested_hhmm}'")
                    
                    if departure_time == requested_hhmm:
                        # Scroll the button into view
                        driver.execute_script("arguments[0].scrollIntoView(true);", button)
                        # Wait until the button is clickable
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button))
                        # Click the parent <a> element
                        button.click()
                        print(f"예약하기 button clicked for requested time {requested_hhmm}!")
                        return True
                    else:
                        print(f"Time mismatch: found {departure_time}, requested {requested_hhmm}")
            except Exception as e:
                print(f"Error processing button {i+1}: {e}")
                continue
        
        print("No 예약하기 buttons found or all buttons failed to process.")
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

# Collect user inputs and set search criteria
try:
    user_dpt_station = input("Enter Departure Station (e.g., 동대구): ").strip()
    user_arv_station = input("Enter Arrival Station (e.g., 수서): ").strip()
    user_date = input("Enter Date YYYYMMDD (e.g., 20240917): ").strip()
    user_time = input("Enter Time HHMMSS (e.g., 160000): ").strip()
    user_passengers_raw = input("Enter number of adult passengers (e.g., 1): ").strip()

    try:
        user_passengers = int(user_passengers_raw)
    except ValueError:
        print("Invalid passengers input. Defaulting to 1.")
        user_passengers = 1

    set_search_criteria(user_dpt_station, user_arv_station, user_date, user_time, user_passengers)
except Exception as e:
    print(f"Error collecting search criteria inputs: {e}")

# Continuously check for 예약하기 buttons
try:
    while True:
        # Click the 조회하기 button to refresh the search results
        click_search_button()
        # Wait for a short period to ensure results are loaded
        time.sleep(2)
        found = check_for_reservation_button(user_time)
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