from typing import Dict
# from appium.options.common.base import AppiumOptions
from .options import DesktopOptions as AppiumOptions
from appium.webdriver.webdriver import WebDriver as WD
from selenium.webdriver.remote.command import Command as RemoteCommand
from selenium.common.exceptions import (
    InvalidArgumentException,
    SessionNotCreatedException,
   
)
from typing import Any, Callable, Dict,Optional
class Remote(WD):
    """
    This is to confiure the method  start_session
    """

    def start_session(self, capabilities: Dict | AppiumOptions, browser_profile: str | None = None) -> None:

        if not isinstance(capabilities, (dict, AppiumOptions)):
            raise InvalidArgumentException('Capabilities must be a dictionary or AppiumOptions instance')
        

        w3c_caps = AppiumOptions.as_w3c(capabilities) if isinstance(capabilities, dict) else capabilities.to_w3c()
        response = self.execute(RemoteCommand.NEW_SESSION, w3c_caps)

        # https://w3c.github.io/webdriver/#new-session
        if not isinstance(response, dict):
            raise SessionNotCreatedException(
                f'A valid W3C session creation response must be a dictionary. Got "{response}" instead'
            )
        
        # Due to a W3C spec parsing misconception some servers
        # pack the createSession response stuff into 'value' dictionary and
        # some other put it to the top level of the response JSON nesting hierarchy
        get_response_value: Callable[[str], Optional[Any]] = lambda key: response.get(key) or (
            response['value'].get(key) if isinstance(response.get('value'), dict) else None
        )
        session_id = get_response_value('sessionId')
        if not session_id:
            raise SessionNotCreatedException(
                f'A valid W3C session creation response must contain a non-empty "sessionId" entry. '
                f'Got "{response}" instead'
            )
        self.session_id = session_id

        #--- UPDATED  THIS SECTION ----
        # self.caps = get_response_value('capabilities') or {}
        # To 
        self.caps = get_response_value('value') or {}
       