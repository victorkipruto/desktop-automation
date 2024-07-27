from automaton import webdriver
from automaton.options import DesktopOptions
from appium.webdriver.common.appiumby import AppiumBy
import logging
import time
caps = DesktopOptions()
caps.set_capability("app","C:\\Windows\\System32\\notepad.exe")

caps.set_capability("automationName", "Windows")
caps.set_capability("newCommandTimeout", 60)

driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723',
            options=caps)

driver.implicitly_wait(30)

editor = driver.find_element(AppiumBy.NAME, "RichEdit Control")



driver.execute_script('mobile: send_keys', {
        'elementId': editor,
        'text': 'Hello, this is a test.'
    })

    # Clear any existing text
   

    # Write text into the Notepad editor
editor.send_keys("Hello, this is a test.")
   
 