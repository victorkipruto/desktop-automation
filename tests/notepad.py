from automaton import webdriver
from automaton.options import DesktopOptions
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.keys import Keys
caps = DesktopOptions()
caps.set_capability("app","C:\\Windows\\System32\\notepad.exe")

caps.set_capability("automationName", "Windows")
caps.set_capability("newCommandTimeout", 60)

driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723',
            options=caps)
with open(file="example",mode="r") as f:
    content=f.readlines()

driver.implicitly_wait(30)
elm = driver.find_element(AppiumBy.NAME, "Text editor")
editor = driver.create_web_element(list(elm.values())[0])
for line in content:
    editor.send_keys(line)
    editor.send_keys(Keys.RETURN)
editor.send_keys(Keys.CONTROL, "s")

# driver.close()
# driver.execute_script('mobile: send_keys', {
#         'elementId': editor,
#         'text': 'Hello, this is a test.'
#     })

    # Clear any existing text
   

    # Write text into the Notepad editor

   
 