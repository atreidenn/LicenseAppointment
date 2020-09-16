import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

# I plan to add a notification via email or a pop-up notification on my laptop screen.
# import smptlib
# import email


PATH = '/Users/juandiegougueto/Documents/PY/chromedriver'
form_url = 'https://sedeapl.dgt.gob.es:7443/WEB_NCIT_CONSULTA/solicitarCita.faces'
driver = webdriver.Chrome(PATH)
num = 0


def appointment_search():
    global num
    driver.get(form_url)
    office_id = []

    # Find all values of the offices to iterate through. 2 different ways to do it.

    # offices = driver.find_element_by_name('publicacionesForm:oficina')
    # office_id.append(offices.find)
    # offices = str(offices[0]).split('\n')
    # offices.pop(0)

    offices = driver.find_element(By.NAME, 'publicacionesForm:oficina')
    selector = Select(offices)

    # Waiting for the values to load
    loading = WebDriverWait(driver, 10).until(EC.element_to_be_selected(selector.options[0]))

    options = selector.options

    for index in range(1, len(options) - 1):
        office_id.append(options[index].text)

    # Select an office for appointment. Should iterate through all options.
    drop_down1 = Select(driver.find_element_by_id("publicacionesForm:oficina"))
    drop_down1.select_by_visible_text(office_id[num])

    # Select specific appointment type.
    try:
        drop_down2 = Select(driver.find_element_by_name('publicacionesForm:tipoTramite'))
        drop_down2.select_by_value('3')  # This value is for license swap.
    except NoSuchElementException:
        time.sleep(3)
        num += 1
        appointment_search()

    # Select country.
    drop_down3 = Select(driver.find_element_by_name('publicacionesForm:pais'))
    drop_down3.select_by_value('21')  # This specific value is for Venezuela.

    # Click search.
    search_button = driver.find_element_by_name('publicacionesForm:j_id70')
    search_button.click()

    # If there is no available appointment, start a loop.
    error_msg = driver.find_element_by_class_name('msgError')

    if error_msg:
        num += 1
        if num == len(office_id) - 1:
            num = 0
        time.sleep(5)
        appointment_search()
    else:
        print(f'Appointment found at: {office_id[num]}.')


appointment_search()
