from appium.options.common import AppiumOptions
from appium.options.common.browser_name_option import BROWSER_NAME

from typing import Any, Dict, TypeVar
import copy
APPIUM_PREFIX = 'appium:'
T = TypeVar('T', bound='AppiumOptions')
PLATFORM_NAME = 'platformName'

class DesktopOptions(AppiumOptions):
    W3C_CAPABILITY_NAMES = frozenset(
        [
            'acceptInsecureCerts',
            BROWSER_NAME,
            'browserVersion',
            PLATFORM_NAME,
            #Added this part
            "app",
            #--------------
            'pageLoadStrategy',
            'proxy',
            'setWindowRect',
            'timeouts',
            'unhandledPromptBehavior',
        ]
    )

    #---No code change, copy paste from Appium options, done to access custom 3C_CAPABILITY_NAMES 
    def set_capability(self: T, name: str, value: Any) -> T:
        w3c_name = name if name in self.W3C_CAPABILITY_NAMES or ':' in name else f'{APPIUM_PREFIX}{name}'
        if value is None:
            if w3c_name in self._caps:
                del self._caps[w3c_name]
        else:
            self._caps[w3c_name] = value
        return self
    
    def get_capability(self, name: str) -> Any:
        """Fetches capability value or None if the capability is not set"""
        return self._caps[name] if name in self._caps else self._caps.get(f'{APPIUM_PREFIX}{name}')
    #--------------------------------------------------------
    
    @staticmethod
    def as_w3c(capabilities: Dict) -> Dict:
       
        """
        Formats given capabilities to a valid W3C session request object

        :param capabilities: Capabilities mapping
        :return: W3C session request object
        """

        def process_key(k: str) -> str:
            key = AppiumOptions._OSS_W3C_CONVERSION.get(k, k)

            #Changed this part from AppiumOptions.W3C_CAPABILITY_NAMES to use custom Capability names
            if key in DesktopOptions.W3C_CAPABILITY_NAMES:
                return key
            return key if ':' in key else f'{APPIUM_PREFIX}{key}'
            #-----------------------------------------------------------------------------------------

        processed_caps = {process_key(k): v for k, v in copy.deepcopy(capabilities).items()}

        #Changed here from
        # return {'capabilities': {'firstMatch': [{}], 'alwaysMatch': processed_caps}}
        #TO
        return {"desiredCapabilities":processed_caps}