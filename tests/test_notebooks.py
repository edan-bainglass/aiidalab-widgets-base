import time

import requests
from selenium.webdriver.common.by import By


def test_notebook_service_available(notebook_service):
    url, token = notebook_service
    response = requests.get(f"{url}/?token={token}")
    assert response.status_code == 200


def test_process_list(selenium_driver, screenshot_dir):
    driver = selenium_driver("notebooks/process_list.ipynb")
    driver.find_element(By.XPATH, '//button[text()="Update now"]')
    driver.get_screenshot_as_file(f"{screenshot_dir}/process-list.png")


def test_aiida_datatypes_viewers(selenium_driver, screenshot_dir):
    driver = selenium_driver("notebooks/aiida_datatypes_viewers.ipynb")
    driver.set_window_size(1000, 2000)
    driver.find_element(By.CLASS_NAME, "widget-label")
    driver.find_element(By.XPATH, '//button[text()="Clear selection"]')
    time.sleep(5)
    driver.get_screenshot_as_file(f"{screenshot_dir}/datatypes-viewer.png")


def test_eln_configure(selenium_driver, screenshot_dir):
    driver = selenium_driver("notebooks/eln_configure.ipynb")
    driver.find_element(By.XPATH, '//button[text()="Set as default"]')
    driver.get_screenshot_as_file(f"{screenshot_dir}/eln-configure.png")


def test_process(selenium_driver, screenshot_dir):
    driver = selenium_driver("notebooks/process.ipynb")
    driver.find_element(By.XPATH, '//label[@title="Select calculation:"]')
    driver.get_screenshot_as_file(f"{screenshot_dir}/process.png")


def test_wizard_apps(selenium_driver, screenshot_dir):
    driver = selenium_driver("notebooks/wizard_apps.ipynb")
    driver.find_element(By.XPATH, '//label[@title="Delivery progress:"]')
    driver.get_screenshot_as_file(f"{screenshot_dir}/wizzard-apps.png")


def test_structures(selenium_driver, screenshot_dir):
    driver = selenium_driver("notebooks/structures.ipynb")
    driver.set_window_size(1000, 900)
    driver.find_element(By.XPATH, '//button[text()="Upload Structure (0)"]')
    driver.get_screenshot_as_file(f"{screenshot_dir}/structures.png")


def test_eln_import(selenium_driver, screenshot_dir):
    driver = selenium_driver("notebooks/eln_import.ipynb")
    # TODO: This find_element is not specific enough it seems,
    # on the screenshot the page is still loading.
    driver.find_element(By.ID, "tooltip")
    time.sleep(5)
    driver.get_screenshot_as_file(f"{screenshot_dir}/eln-import.png")


def test_computational_resources_code_setup(
    selenium_driver, aiidalab_exec, screenshot_dir
):
    """Test the quicksetup of the code"""
    # check the code pw-7.0 is not in code list
    output = aiidalab_exec("verdi code list").decode().strip()
    assert "pw-7.0" not in output

    driver = selenium_driver("notebooks/computational_resources.ipynb")

    # click the "Setup new code" button
    driver.find_element(By.XPATH, '(//button[text()="Setup new code"])[1]').click()

    # Select daint.cscs.ch domain
    driver.find_element(By.XPATH, '(//option[text()="daint.cscs.ch"])[1]').click()

    # Select computer multicore
    driver.find_element(By.XPATH, '(//option[text()="multicore"])[1]').click()

    # select code pw-7.0-multicore
    driver.find_element(By.XPATH, '(//option[text()="pw-7.0-multicore"])[1]').click()

    # fill the SSH username
    driver.find_element(
        By.XPATH, "(//label[text()='SSH username:'])[1]/following-sibling::input"
    ).send_keys("dummyuser")

    # click the quick setup
    driver.find_element(By.XPATH, '(//button[text()="Quick Setup"])[1]').click()
    time.sleep(1.0)

    # check the new code pw-7.0@daint-mc is in code list
    output = aiidalab_exec("verdi code list").decode().strip()
    assert "pw-7.0@daint-mc" in output

    # Set the second code of the same computer
    # issue https://github.com/aiidalab/aiidalab-widgets-base/issues/416
    # click the "Setup new code" button
    driver.find_element(By.XPATH, '(//button[text()="Setup new code"])[2]').click()

    # Select daint.cscs.ch domain
    driver.find_element(By.XPATH, '(//option[text()="daint.cscs.ch"])[2]').click()

    # Select computer multicore
    driver.find_element(By.XPATH, '(//option[text()="multicore"])[2]').click()

    # select code pw-7.0-multicore
    driver.find_element(By.XPATH, '(//option[text()="dos-7.0-multicore"])[2]').click()

    # fill the SSH username
    # Get the element of index 3 which is the SSH username of second widget
    # the one of index 2 is the SSH username in detail setup of the first widget.
    driver.find_element(
        By.XPATH, "(//label[text()='SSH username:'])[3]/following-sibling::input"
    ).send_keys("dummyuser")

    # click the quick setup
    driver.find_element(By.XPATH, '(//button[text()="Quick Setup"])[2]').click()
    time.sleep(1.0)

    # check the new code pw-7.0@daint-mc is in code list
    output = aiidalab_exec("verdi code list").decode().strip()
    assert "dos-7.0@daint-mc" in output

    # take screenshots
    driver.get_screenshot_as_file(f"{screenshot_dir}/computational-resources.png")
