

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.ie.options import Options as IEOptions


@pytest.fixture(params=[
    {
        "browserName": "chrome",
        "goog:chromeOptions": {
            "browserVersion": "88.0",
            "platformName": "Windows 10",
            "LT:Options": {
                "username": "prashanthmadhur",
                "accessKey": "RmOBOK6QjpOp9VkzlqUX87oHcGSxss3C7nay2XYUzDmmde4f62",
                "build": "88",
                "project": "Untitled",
                "w3c": True,
                "plugin": "python-python"
            }
        }
    },
    {
        "browserName": "MicrosoftEdge",
        "ms:edgeOptions": {
            "browserVersion": "87.0",
            "platformName": "macOS Sierra",
            "LT:Options": {
                "username": "prashanthmadhur",
                "accessKey": "RmOBOK6QjpOp9VkzlqUX87oHcGSxss3C7nay2XYUzDmmde4f62",
                "build": "87",
                "project": "Untitled",
                "w3c": True,
                "plugin": "python-python"
            }
        }
    },
    {
        "browserName": "firefox",
        "moz:firefoxOptions": {
            "browserVersion": "82.0",
            "platformName": "Windows 7",
            "LT:Options": {
                "username": "prashanthmadhur",
                "accessKey": "RmOBOK6QjpOp9VkzlqUX87oHcGSxss3C7nay2XYUzDmmde4f62",
                "build": "87",
                "project": "Untitled",
                "w3c": True,
                "plugin": "python-python"
            }
        }
    },
    {
        "browserName": "internet explorer",
        "se:ieOptions": {
            "browserVersion": "11.0",
            "platformName": "Windows 10",
            "LT:Options": {
                "username": "prashanthmadhur",
                "accessKey": "RmOBOK6QjpOp9VkzlqUX87oHcGSxss3C7nay2XYUzDmmde4f62",
                "build": "11.0",
                "project": "Untitled",
                "w3c": True,
                "plugin": "python-python"
            }
        }
    }
])
def driver(request):
    capabilities = request.param
    if capabilities["browserName"] == "chrome":
        options = ChromeOptions()
    elif capabilities["browserName"] == "MicrosoftEdge":
        options = EdgeOptions()
    elif capabilities["browserName"] == "firefox":
        options = FirefoxOptions()
    elif capabilities["browserName"] == "internet explorer":
        options = IEOptions()
    else:
        raise ValueError("Invalid browser parameter.")

    for option_name, option_value in capabilities.get(capabilities["browserName"] + ":Options", {}).items():
        options.set_capability(option_name, option_value)

    # Enable video recording
    options.set_capability("video", True)
    options.set_capability("videoName", "test_video.mp4")
    options.set_capability("screen-resolution", "1920x1080")

    # Enable network logs
    options.add_argument("--enable-logging")

    # Construct the LambdaTest URL with username and access token
    username = capabilities.get(capabilities["browserName"] + ":Options", {}).get("LT:Options", {}).get("username")
    access_token = capabilities.get(capabilities["browserName"] + ":Options", {}).get("LT:Options", {}).get("accessKey")
    command_executor_url = f'https://{username}:{access_token}@hub.lambdatest.com/wd/hub'

    driver = webdriver.Remote(
        command_executor=command_executor_url,
        desired_capabilities=options.to_capabilities()
    )
    yield driver
    driver.quit()
def test_simple_form_demo(driver):
    # Step 1: Open LambdaTest's Selenium Playground
    driver.get("https://www.lambdatest.com/selenium-playground")

    # Step 2: Click "Simple Form Demo" under Input Forms
    simple_form_demo_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Simple Form Demo"))
    )
    simple_form_demo_link.click()

    # Step 3: Validate that the URL contains "simple-form-demo"
    assert "simple-form-demo" in driver.current_url, "URL validation failed."

    # Step 4: Create a variable for a string value
    message = "Welcome to LambdaTest"

    # Step 5: Use the variable to enter values in the "Enter Message" text box
    enter_message_box = driver.find_element(By.ID, "user-message")
    enter_message_box.send_keys(message)

    # Step 6: Click "Get Checked Value"
    get_message_button = driver.find_element(By.XPATH, "//button[text()='Get Checked Value']")
    get_message_button.click()

    # Step 7: Validate whether the same text message is displayed in the right-hand panel
    your_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "message"))
    ).text

    assert your_message == f"Your Message: {message}", "Message validation failed."

def test_input_form_submit(driver):
    driver.get("https://www.lambdatest.com/selenium-playground")
    wait = WebDriverWait(driver, 10)

    # Click "Input Form Submit" link
    input_form_submit_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Input Form Submit")))
    input_form_submit_link.click()

    # Click "Submit" without filling in any information
    submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    submit_button.click()

    # Assert "Please fill in the fields" error message
    error_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='contact_form_error']/p")))
    assert error_message.text == "Please fill in the fields", "Error message not displayed correctly."

    # Fill in Name, Email, and other fields
    name_input = driver.find_element(By.NAME, "name")
    email_input = driver.find_element(By.NAME, "email")
    phone_input = driver.find_element(By.NAME, "phone")
    address_input = driver.find_element(By.NAME, "address")
    city_input = driver.find_element(By.NAME, "city")
    zip_input = driver.find_element(By.NAME, "zip")

    name_input.send_keys("John Doe")
    email_input.send_keys("johndoe@example.com")
    phone_input.send_keys("1234567890")
    address_input.send_keys("123 Main Street")
    city_input.send_keys("New York")
    zip_input.send_keys("10001")

    # Select "United States" from the Country drop-down using the text property
    country_dropdown = Select(driver.find_element(By.NAME, "country"))
    country_dropdown.select_by_visible_text("United States")

    # Click "Submit"
    submit_button.click()

    # Validate the success message "Thanks for contacting us, we will get back to you shortly."
    success_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='contact_reply']/h1")))
    assert success_message.text == "Thanks for contacting us, we will get back to you shortly.", "Success message not displayed correctly."


if __name__ == "__main__":
    pytest.main(["-v", "-s", "test_certtest.py"])