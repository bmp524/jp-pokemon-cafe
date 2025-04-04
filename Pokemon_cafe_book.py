# Pokemon cafe reservation booking tool (Tokyo or Osaka)
#-----------------------------------------------------

# Run code to open reservation page. Script will pause for 15 seconds to allow user to pass human test
# Human check is required every 7-10 min

# Added a location parameter for user to select between Tokyo and Osaka
# Added text_to_find to output messages to clarify code status
# Added error handling for advancing calendar month during high traffic
# Updated XPath date search to only select unique dates (i.e. if future_date.day = 2, do not select previous month's 27 day)

# Successful reservation on 3/21/25

#-----------------------------------------------------

# User defined parameters
cafe_location = 'Tokyo' #or 'Osaka'
num_of_guests = 2 #number of guests for reservation
sleep_time = 3 #wait time before refresh

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time as time_module
from datetime import datetime, time, timedelta

def restart_program():
    """Restarts the current program."""
    print("Restarting program...")

def wait_until_target_time(target_time):
    # Pause for 15 seconds to allow human interaction with webpage (captcha)
    # target_time represents now + 15 seconds
    
    while True:
        current_time = datetime.now()#.time()
        if current_time >= target_time:
            print("Time up for human test")
            break
        else:
            # Calculate the time difference
            current_datetime = datetime.combine(datetime.today(), current_time.time())
            target_datetime = datetime.combine(datetime.today(), target_time.time())
            time_to_wait = (target_datetime - current_datetime).total_seconds()
            # Sleep for the remaining time
            time_module.sleep(time_to_wait)


def refresh_until_found(text_to_find, sleep_time):
    # Scan webpage for text indicating page can be interacted with, break out of function
    # Otherwise refresh the page

    while True:
        try:
            # Check if the text is present in the page source
            if text_to_find in driver.page_source:
                print(text_to_find,"Text found!")
                break
            else:
                print(text_to_find,"Text not found, refreshing the page...")
                driver.refresh()
                time_module.sleep(sleep_time)  # Wait for sleep_time seconds before checking again
        except NoSuchElementException:
            print("Element not found, refreshing the page...")
            driver.refresh()
            time_module.sleep(sleep_time)  # Wait for sleep_time seconds before checking again

def refresh_until_not_found(text_to_find, sleep_time):
    # Scan webpage for text indicating "The site is congested due to heavy access."
    # Refresh page based on status

    while True:
        try:
            # Check if the text is present in the page source
            if text_to_find in driver.page_source:
                print("The site is congested due to heavy access. found!")
                driver.refresh()
                time_module.sleep(sleep_time)  # Wait for sleep_time seconds before checking again

            else:
                print(text_to_find,"Text not found, exiting...")
            break
        except NoSuchElementException:
            print("Element not found, refreshing the page...")
            driver.refresh()
            time_module.sleep(sleep_time)  # Wait for sleep_time seconds before checking again


print("Opening the site main page")
#

if cafe_location == "Tokyo":
    website = "https://reserve.pokemon-cafe.jp/reserve/step1"
elif cafe_location == "Osaka":
    website = "https://osaka.pokemon-cafe.jp/reserve/step1"

chrome_options = Options()
# chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chromedriver = "chromedriver"
driver = webdriver.Chrome(options=chrome_options)
driver.get(website)

target_time = datetime.now() + timedelta(seconds=15) #current time + 15 seconds wait time for human test
#target_time = datetime.now().time() + timedelta(seconds=15)
print("Waiting for human input until:", target_time)
wait_until_target_time(target_time)
# Allow user to complete human verfication

#checking if "Table Reservation" page successfully opened. If not - refresh the page
# Define the text to find
text_to_find = "Number of Guests"

# Input number of guests using user defined guests parameter
refresh_until_found(text_to_find, sleep_time)
#number of guests
# 席の予約 HTML 3 - Select number of guest
print("Selecting the number of guests")
select = Select(driver.find_element(By.NAME, 'guest'))
select.select_by_index(num_of_guests)

# Check for high congestion page and refresh if necessary
text_to_find = "The site is congested due to heavy access"
refresh_until_not_found(text_to_find, sleep_time)

# Advance reservation calendar to next month
print("Selecting the next month")
#driver.find_element(By.XPATH, "//*[contains(text(), '次の月を見る')]").click()

while True: 
    try:
        if driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) > .calendar-pager").is_displayed() == True:
            driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) > .calendar-pager").click()
            print("Next month clicked")
            break
        else:
        #except NoSuchElementException:
            print("Next month element not found, refreshing the page...")
            driver.refresh()
            time_module.sleep(sleep_time)  # Wait for sleep_time seconds before checking again
    except:
        print("Error on next month attempt")
        break

# Check again for high traffic page
refresh_until_not_found(text_to_find, sleep_time)

# Bookings open 31 days out, search for openings 31 days from today and select date
future_date = datetime.now() + timedelta(days=31)
print("The day of the month 31 days from now is:", future_date.day)

#Updated XPath search to only select unique dates (i.e. if future_date.day = 2, do not select previous month's 27 day)
date_xpath = f"//li[contains(@class, 'calendar-day-cell')]//div[normalize-space(text())='{future_date.day}']"
element = driver.find_element(By.XPATH, date_xpath)
element.click()

#driver.find_element(By.XPATH, "//*[contains(text(), " + str(future_date.day) + ")]").click()
#
print("Pressing Next step button")
driver.find_element(By.XPATH, "//*[@class='button' and @id='submit_button']").click()

# Check again for high traffic page
text_to_find = "The site is congested due to heavy access"
refresh_until_not_found(text_to_find, sleep_time)


# Scan for available time slots and refresh if needed
text_to_find = "Available"
refresh_until_found(text_to_find, sleep_time)


##########################Available
# Once available time slot is found, select and check for high traffic if needed
try:
    # Find the 'div' element containing the text 'Available'
    element = driver.find_element(By.XPATH, "//div[contains(text(), 'Available')]")

    # Click the element
    element.click()
    print("Element with text 'Available' clicked.")
    
    text_to_find = "The site is congested due to heavy access"
    refresh_until_not_found(text_to_find, sleep_time)
    
except NoSuchElementException:
    print("Element with text 'Available' not found.")
