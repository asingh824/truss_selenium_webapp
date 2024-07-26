import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_webdriver():
    try:
        service = Service('/Users/asingh247/Downloads/chromedriver-mac-x64/chromedriver')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("WebDriver initialized successfully.")
        return driver
    except Exception as e:
        logging.error(f"Failed to initialize WebDriver: {e}")
        raise

def navigate_to_login(driver):
    try:
        driver.get('https://provider.trusshealth.ai')
        logging.info("Navigated to the login page.")
    except Exception as e:
        logging.error(f"Failed to navigate to the login page: {e}")
        raise

def locate_login_elements(driver):
    try:
        wait = WebDriverWait(driver, 10)
        email_field = wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
        logging.info("Email field located.")

        password_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))
        logging.info("Password field located.")

        login_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[data-testid="SubmitLogin"]')))
        logging.info("Login button located.")

        return email_field, password_field, login_button
    except TimeoutException as e:
        logging.error(f"Failed to locate login elements: {e}")
        raise

def login(driver, email, password):
    try:
        email_field, password_field, login_button = locate_login_elements(driver)
        email_field.send_keys(email)
        logging.info("Email typed: True")
        password_field.send_keys(password)
        logging.info("Password typed: True")
        login_button.click()
        logging.info("Login button clicked.")
    except Exception as e:
        logging.error(f"Login failed: {e}")
        raise

def navigate_to_patients(driver):
    wait = WebDriverWait(driver, 20)
    try:
        wait.until(EC.url_contains('/doctorDashboard/overview'))
        logging.info("in dashboard/overview")
        # Wait for the "Patients" button to be present and clickable
        dropdown_menu = wait.until(
            EC.element_to_be_clickable((By.XPATH, '/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/header[1]/div[1]/button[1]')))
        #EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Patients')]")))
        dropdown_menu.click()
        logging.info("drop down menu clicked.")
        patients_button = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//body[1]/div[5]/div[1]/div[1]/div[2]/section[1]/div[1]/div[1]/div[1]/div[1]/nav[1]/div[1]/div[1]/div[1]/div[1]/button[2]/div[1]/div[1]')))
        patients_button.click()
        logging.info("clicked PATIENTS...")
        wait.until(EC.url_contains('/doctorDashboard/patientlist'))
        logging.info("sidebar active...")
        #driver.execute_script("document.querySelector('body').click();")
        retract_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '/html[1]/body[1]/div[5]/div[1]/div[1]/div[1]')))   
        retract_dropdown.click()
        logging.info("Clicked in the middle of the screen to retract the sidebar.")

        time.sleep(10)
        wound_form_button = wait.until(
            EC.visibility_of_element_located((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[2]/td[6]/div[1]/*[name()='svg'][1]")))
        wound_form_button.click()
        logging.info("WOUND BUTTON CLICKED !!")
        time.sleep(10)

    except (TimeoutException, NoSuchElementException) as e:
        logging.error(f"Navigation to Patients page failed: {e}")
        driver.save_screenshot("error_screenshot.png")
        logging.info("Screenshot saved as 'error_screenshot.png'.")
        raise

def upload_and_submit(driver, digital_image_path, thermal_image_path, retries=3):
    wait = WebDriverWait(driver, 15)
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]"))
        )
        logging.info("on image upload page wound page.")
        for attempt in range(retries):
            try:
                # wait.until(EC.url_contains('/doctordashboard/wound/'))
                # logging.info("On the image upload page /doctordashboard/wound/.")
                # Locate the thermal image input element
                thermal_image_input = wait.until(
                     EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]"))
                )
                # Upload the thermal image
                thermal_image_input.send_keys(thermal_image_path)
                logging.info("Thermal image uploaded.")
                driver.save_screenshot("thermal_upload_screenshot.png")
                logging.info("Screenshot saved as 'thermal_upload_screenshot.png'.")
                # Verify the thermal image upload success
                # WebDriverWait(driver, 10).until(
                #     EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'thermal_image')]"))
                # )
                # # Locate the digital image input element
                
                digital_image_input = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]"))
                )
                # # Upload the digital image
                digital_image_input.send_keys(digital_image_path)
                logging.info("Digital image uploaded.")
                driver.save_screenshot("dig_upload_screenshot.png")
                logging.info("Screenshot saved as 'dig_upload_screenshot.png'.")

                break #exit retry loop if successful
            except Exception as e:
                logging.error(f"Upload attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    logging.info("Retrying upload...")
                    time.sleep(5)  # Wait before retrying
                else:
                    driver.save_screenshot("error_screenshot.png")
                    logging.info("Screenshot saved as 'error_screenshot.png'.")
                    raise  # Re-raise the exception if out of retries

                # #thermal_image_input = wait.until(
                # #    EC.visibility_of_element_located((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]")))
                # #thermal_image_input.send_keys(thermal_image_path)
                # logging.info("thermal upload verification complete")
                # time.sleep(5)
                # #debug step - checkpoint
                # driver.save_screenshot("checkpoint_screenshot.png")
                # logging.info("Screenshot saved as 'checkpoint_screenshot.png'.")
                
                # # Locate the digital image input element
                # digital_image_input = driver.find_element(By.XPATH, "//input[@type='file' and contains(@class, 'mantine-Dropzone')]")
                # # Upload the digital image
                # digital_image_input.send_keys(digital_image_path)
                # logging.info("Digital image uploaded.")

                # # digital_image_input = wait.until(
                # #     EC.visibility_of_element_located((By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]")))
                
                # # digital_image_input.send_keys(digital_image_path)
                # # logging.info("Digital image uploaded.")
                
                # take_snapshot_button = driver.find_element(By.XPATH, "//button[text()='Take Snapshot']")
                # take_snapshot_button.click()
                # logging.info("Take Snapshot button clicked. now waiting for AI results")
                
                # WebDriverWait(driver, 30).until(
                #     EC.presence_of_element_located((By.XPATH, "//button[text()='Save & Continue']"))
                # )
                # logging.info("Save & Continue button located.")
                
                # save_continue_button = driver.find_element(By.XPATH, "//button[text()='Save & Continue']")
                # driver.execute_script("arguments[0].scrollIntoView();", save_continue_button)
                # save_continue_button.click()
                # logging.info("Save & Continue button clicked.")
    except Exception as e:
        logging.error(f"Error during upload and submit process: {e}")
        raise

def main():
    driver = None
    try:
        driver = initialize_webdriver()
        navigate_to_login(driver)
        login(driver, 'drtest@trusshealth.ai', 'testing')
        navigate_to_patients(driver)
        digital_image_path = '/Users/asingh247/Downloads/Truss_provider_auto/surgery_images/digital2.jpeg'
        thermal_image_path = '/Users/asingh247/Downloads/Truss_provider_auto/surgery_images/thermal2.jpeg'
        upload_and_submit(driver, digital_image_path, thermal_image_path)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()
            logging.info("WebDriver closed.")

if __name__ == "__main__":
    main()
