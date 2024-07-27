### Desktop Automation with WinAppDriver and Python 

#### Problem: "Bad capabilities. Specify either app or appTopLevelWindow to create a session"

When you try to open windows app you get the following error


``` 
HTTP/1.1 400 Bad Request
Content-Length: 141
Content-Type: application/json

{"status":100,"value":{"error":"invalid argument","message":"Bad capabilities. Specify either app or appTopLevelWindow to create a session"}}
```
### Setup 
* WinAppDriver v1.2.1
* Appium-Python-Client 4.0.1 
* Selenium 4.23.1

### Cause 
WinAppDriver doesn't recognize capabilities sent by appium 

Capabilities sent by appium
```
    {'capabilities': {'firstMatch': [{}], 'alwaysMatch': processed_caps}}
```

Capabilies expected by winappdriver

```
    {'desiredCapabilities':processed_caps}
```

### Solution
Wrote a wrapper arround `webdriver` and `AppiumOptions` to return the response required by winappdriver
The solution was packaged as a python library, which has a dependency on Appium-Python-Client 

Library name: automaton for lack of better name :)

### Parts that changed

**Web driver**

Overide the `start_session` method , to use custom options `DesktopOptions` which has been imported as AppiumOptions

```
# from appium.options.common.base import AppiumOptions
from .options import DesktopOptions as AppiumOptions
```

```
 #--- UPDATED  THIS SECTION ----
        # self.caps = get_response_value('capabilities') or {}
        # To 
        self.caps = get_response_value('value') or {}
```

**Desktop Options**
Inherited `AppiumOptions` override `W3C_CAPABILITY_NAME` and include `app` this is to avoid addition of `appium:app` to this capability, since this is what will result `winappdriver` not to recognize app

```
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

    ....
```

I had to include the methods below so as to override the parent one and include a local `W3C_CAPABILITY_NAMES` 

```
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
```

Finally I did override static method `as_w3c`  to user custom `DesktopOptions` and also alter its return type

```
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

```

