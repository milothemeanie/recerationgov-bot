import time

from dateutil import parser
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

WEB_DRIVER_EXEC = "/home/cward/webdrivers/chromedriver_linux64/chromedriver"

USER_NAME = ""
PASSWORD = ""

# Highly available one https://www.recreation.gov/camping/campgrounds/233543
# Originally requested  https://www.recreation.gov/camping/campgrounds/232768
CAMP_GROUND_URL = "https://www.recreation.gov/camping/campgrounds/232768"
# MM/DD/YYYY
START_DATE = "06/08/2022"
# MM/DD/YYYY
END_DATE = "06/12/2022"

POLL_SPEED_SEC = 1

def main():
    print("Starting recreation.gov bot")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    browser = webdriver.Chrome(executable_path=WEB_DRIVER_EXEC, options=options)
    browser.get('https://www.recreation.gov/')

    try:

        login_button = browser.find_element(By.ID, "ga-global-nav-log-in-link")

        if login_button:
            print("Need to log in first")
            login_button.click()
            email = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "email")))

            if email:
                print("Logging in")
                email.send_keys(USER_NAME)

                password = browser.find_element(By.ID, "rec-acct-sign-in-password")
                password.send_keys(PASSWORD)

                browser.find_element(By.XPATH, "//button[@type='submit' and @title='Log In']").click()

                logged_in = WebDriverWait(browser, 500).until(
                    EC.presence_of_element_located((By.ID, "ga-global-nav-account-cart-link")))

                if logged_in:
                    print("I'm in!")
                    browser.get(CAMP_GROUND_URL)

                    exit_tutorial = find_button_with_label("Close modal", browser)
                    exit_tutorial.click()

                    begin_date = parser.parse(START_DATE)
                    end_date = parser.parse(END_DATE)
                    navigate_to_date_range(browser, begin_date, end_date)

                    available_begin_dates = find_available_dates(browser, begin_date)
                    available_end_dates = find_possible_res_dates(browser, end_date)

                    counter = 0
                    while len(available_begin_dates) == 0 or len(available_end_dates) == 0:
                        next_five = find_button_with_label("Go Forward 5 Days", browser)
                        browser.execute_script('arguments[0].scrollIntoView();', next_five)
                        time.sleep(POLL_SPEED_SEC)
                        counter = counter + 1
                        print("Attempt {0}".format(str(counter)))
                        refresh_button = browser.find_element(By.XPATH,
                                                              "//span[@class = 'sarsa-button-content' and contains(text(), 'Refresh Table')]")

                        browser.execute_script('arguments[0].scrollIntoView();', refresh_button)
                        actions = ActionChains(browser)
                        actions.move_to_element(refresh_button).click().perform()

                        available_begin_dates = find_available_dates(browser, begin_date)
                        available_end_dates = find_possible_res_dates(browser, end_date)

                    matches = list()
                    for b_date in available_begin_dates:
                        for e_date in available_end_dates:
                            b_acc_name = str(b_date.accessible_name)[b_date.accessible_name.index("-"):]
                            e_acc_name = str(e_date.accessible_name)[e_date.accessible_name.index("-"):]

                            if b_acc_name == e_acc_name:
                                matches.append((b_date, e_date))
                                available_end_dates.remove(e_date)
                                break

                    for match in matches:
                        browser.execute_script(
                            "document.getElementById('availability-table').style.zIndex = '999';")

                        browser.execute_script('arguments[0].scrollIntoView();', match[0])

                        match[0].click()
                        match[1].click()

                        browser.execute_script(
                            "document.getElementsByClassName('rec-campground-availability-book-now')["
                            "0].parentNode.style.position = 'relative';")

                        cart_button = browser.find_element(By.XPATH,
                                                           "//span[@class = 'sarsa-button-content' and contains(text(), 'Add to Cart')]")

                        browser.execute_script('arguments[0].scrollIntoView(false);', cart_button)

                        actions = ActionChains(browser)
                        actions.move_to_element(cart_button).click().perform()

                        break

        # This is to keep the webdriver open until user is finished
        WebDriverWait(browser, 5000).until(EC.presence_of_element_located((By.ID, "derp")))

    finally:
        print("Finished")


def find_available_dates(browser, date):
    date_abr = date.strftime("%b %-d, %Y")
    date_buttons = browser.find_elements(By.XPATH,
                                         "//button[@class='rec-availability-date' and contains(@aria-label, '{0}')]".format(
                                             date_abr))

    return [x for x in date_buttons if x.text == 'A' and not 'PAVILION' in str(x.accessible_name)]


def find_possible_res_dates(browser, date):
    date_abr = date.strftime("%b %-d, %Y")
    date_buttons = browser.find_elements(By.XPATH,
                                         "//button[@class='rec-availability-date' and contains(@aria-label, '{0}')]".format(
                                             date_abr))

    return [x for x in date_buttons if (x.text == 'NR' or x.text == 'A') and not 'PAVILION' in str(x.accessible_name)]


def navigate_to_date_range(browser, begin_date, end_date):
    next_five = find_button_with_label("Go Forward 5 Days", browser)
    browser.execute_script('arguments[0].scrollIntoView();', next_five)

    begin_date_str = begin_date.strftime("%A %B %-d, %Y")
    begin_columns = find_date_buttons(begin_date_str, browser)

    end_date_str = end_date.strftime("%A %B %-d, %Y")
    end_columns = find_date_buttons(end_date_str, browser)

    while len(begin_columns) == 0 or len(end_columns) == 0:
        print(str(check_start_label(browser)))

        next_five = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='button' and @aria-label = 'Go Forward 5 Days']")))

        next_five.click()
        begin_columns = find_date_buttons(begin_date_str, browser)
        end_columns = find_date_buttons(end_date_str, browser)


def check_start_label(browser):
    starting_date_element = browser.find_element(By.CLASS_NAME, 'sarsa-text')
    starting_date_label = starting_date_element.text.replace('Starting ', '')
    return parser.parse(starting_date_label)


def find_buttons_with_label(date_str, browser):
    columns = browser.find_elements(By.XPATH,
                                    "//button[@type='button' and @aria-label = '{0}']".format(
                                        date_str))
    return columns


def find_button_with_label(date_str, browser):
    columns = browser.find_element(By.XPATH,
                                   "//button[@type='button' and @aria-label = '{0}']".format(
                                       date_str))
    return columns


def find_date_buttons(date_str, browser):
    columns = browser.find_elements(By.XPATH,
                                    "//button[@aria-label = '{0}']".format(
                                        date_str))
    return columns


if __name__ == '__main__':
    main()
