# Usage:
1. Install python [here](https://www.python.org/downloads/windows/). *(I tested on version 3.12.3)*
    - *Be sure to check this box in the installation window*: **Add python exe to PATH**
2. Log into the pishock account, plug the pishock hub in, turn the collar on. Make sure you can see the collar in the web interface.
3. Download this repo's [Latest Release]()
4. Run `setup.py` and wait until it says it is done. It will probably have a few dependancies to install.
5. Run `Yugioh_shocker.pyw` and the interface should pop up. The program will send a 1 second beep when it opens to let you know the collar is working as expected.
    - If nothing shows up, try installing the microsoft-c++-redistributable [here](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170)

# Configuration:
`config.json` contains the following configurable settings:
- Account
  - Username: From pishock.com
  - API_Key: From pishock.com
  - Share_code: From pishock.com
  - Program name: This one can be anything you want.
- Bot Behaviour
  - Detection Threshold: This is the threshold for the image recognition. It was tested and working for me on 0.8 but if you have false positives you should lower this. Raise this if your Defeat screen is not detected.
  - Scanning cooldown after shocking - ms: This is the cooldown before scanning begins again after a Defeat is detected and a shock is sent. This time is in ms so take the amount of seconds you want and multiply it by 1000. Default is 120000 aka 120 seconds / 2 mins
  - Screen scan interval - ms: This is the interval between scans to check for a Defeat. If your computer slows down while scanning is active, try raising this value in increments of 250 until performance improves.

 # Libraries Used:
  Signals are sent to the pishock using [Pishockpy by UWUplus](https://github.com/UWUplus/pishockpy)
