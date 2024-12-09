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
    os.execv(sys.executable, ['python'] + sys.argv)

def wait_until_target_time(target_time):
    """
    Waits until the specified target time.

    Parameters:
    target_time (datetime.time): The time to wait until.
    """
    while True:
        current_time = datetime.now().time()
        if current_time >= target_time:
            print("Target time reached!")
            break
        else:
            # Calculate the time difference
            current_datetime = datetime.combine(datetime.today(), current_time)
            target_datetime = datetime.combine(datetime.today(), target_time)
            time_to_wait = (target_datetime - current_datetime).total_seconds()
            # Sleep for the remaining time
            time_module.sleep(time_to_wait)


def refresh_until_found(text_to_find, sleep_time, url_check):
    while True:
        try:
            # Check if the text is present in the page source
            if text_to_find in driver.page_source:
                print("Text found!")
                break
            if url_check not in driver.current_url:
                print("URL changed...Restarting from beginig")
                restart_program()
            else:
                print("Text not found, refreshing the page...")
                driver.refresh()
                time_module.sleep(sleep_time)  # Wait for 5 seconds before checking again
        except NoSuchElementException:
            print("Element not found, refreshing the page...")
            driver.refresh()
            time_module.sleep(sleep_time)  # Wait for 5 seconds before checking again

#The site is congested due to heavy access.
def refresh_until_not_found(text_to_find, sleep_time):
    while True:
        try:
            # Check if the text is present in the page source
            if text_to_find in driver.page_source:
                print("The site is congested due to heavy access. found!")
                driver.refresh()
                time_module.sleep(sleep_time)  # Wait for 5 seconds before checking again

            else:
                print("Text not found, exiting...")
            break
        except NoSuchElementException:
            print("Element not found, refreshing the page...")
            driver.refresh()
            time_module.sleep(sleep_time)  # Wait for 5 seconds before checking again
# Set the target time to 13:59:57


print("Opening the site main page")
#
website = "https://reserve.pokemon-cafe.jp/reserve/step1"
chrome_options = Options()
# chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chromedriver = "chromedriver"
driver = webdriver.Chrome(options=chrome_options)
driver.get(website)

target_time = time(13, 59, 30)
print("Waiting until:", target_time)
wait_until_target_time(target_time)

#checking if "Table Reservation" page successfully opened. If not - refresh the page

# Define the text to find
text_to_find = "Number of Guests"
# Wait time before refresh
sleep_time = 2
num_of_guests = 2

url2check = 'https://reserve.pokemon-cafe.jp/reserve/step1'
refresh_until_found(text_to_find, sleep_time, url2check)
#number of guests
# 席の予約 HTML 3 - Select number of guest
print("Selecting the number of guests")
select = Select(driver.find_element(By.NAME, 'guest'))
select.select_by_index(num_of_guests)

text_to_find = "The site is congested due to heavy access"
refresh_until_not_found(text_to_find, sleep_time)
refresh_until_found( '次の月を見る', sleep_time, url2check)

#next month
print("Selecting the next month")
#driver.find_element(By.XPATH, "//*[contains(text(), '次の月を見る')]").click()
driver.find_element(By.CSS_SELECTOR, "div:nth-child(3) > .calendar-pager").click()



#31 from now would be
future_date = datetime.now() + timedelta(days=31)
print("The day of the month 31 days from now is:", future_date.day)
#element = driver.find_element(By.XPATH, "//*[contains(text(), " + str(future_date.day) + ")]")
#element = driver.find_element(By.XPATH, "//*[contains(@class, 'calendar-day-cell') and contains(text(), " + str(future_date.day) + ")]")

text_to_find = "The site is congested due to heavy access"
refresh_until_not_found(text_to_find, sleep_time)

element = driver.find_element(By.XPATH, "//li[contains(@class, 'calendar-day-cell') and contains(., " + str(future_date.day) + ")]")

#driver.execute_script("arguments[0].scrollIntoView();", element)
element.click()

#driver.find_element(By.XPATH, "//*[contains(text(), " + str(future_date.day) + ")]").click()
#
print("Pressing Next step button")
driver.find_element(By.XPATH, "//*[@class='button' and @id='submit_button']").click()
text_to_find = "The site is congested due to heavy access"
refresh_until_not_found(text_to_find, sleep_time)



text_to_find = "Available"
# Wait time before refresh
sleep_time = 2
url2check = 'https://reserve.pokemon-cafe.jp/reserve/step2'
refresh_until_found(text_to_find, sleep_time, url2check)


##########################Available
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




# Close the WebDriver
#driver.quit()

#Number of Guests

# def create_booking(day_of_month, num_of_guests, location):
#   '''Create a reservation for Pokemon Cafe in Tokyo
#   Keyword arguments:
#   day_of_month -- day of the month to book
#   num_of_guests -- number of guests to book (1-8)
#   '''
#
#   if location == "Tokyo":
#     website = "https://reserve.pokemon-cafe.jp/"
#   elif location == "Osaka":
#     website = "https://osaka.pokemon-cafe.jp/"
#
#   chrome_options = Options()
#   # chrome_options = webdriver.ChromeOptions()
#   chrome_options.add_experimental_option("detach", True)
#   chromedriver = "chromedriver"
#   driver = webdriver.Chrome(options=chrome_options)
#   driver.get(website)
#
#   try:
#     # 席の予約 HTML 1 - Make a reservation
#     driver.find_element(By.XPATH, "//*[@class='button arrow-down']").click()
#
#     # 席の予約 HTML 2 - Agree T&C
#     driver.find_element(By.XPATH, "//*[@class='agreeChecked']").click()
#     driver.find_element(By.XPATH, "//*[@class='button']").click()
#
#     # 席の予約 HTML 3 - Select number of guest
#     select = Select(driver.find_element(By.NAME, 'guest'))
#     select.select_by_index(num_of_guests)
#
#     # 席の予約 HTML 4 - Select from calendar
#     driver.find_element(By.XPATH, "//*[contains(text(), '次の月を見る')]").click()
#     driver.find_element(By.XPATH, "//*[contains(text(), " + str(day_of_month) + ")]").click()
#     driver.find_element(By.XPATH, "//*[@class='button']").click()
#   except NoSuchElementException:
#     pass


#num_iterations = 1
#day_of_month='01'
#num_of_guests=2
#location = 'Tokyo'
#location = 'Osaka'
#[create_booking(day_of_month, num_of_guests, location) for x in range(num_iterations)]
