import os
import time
import signal
import requests
import objc
import urllib3
from AppKit import NSWorkspace
from Foundation import NSAppleScript
from config import HASS_URL, HASS_TOKEN, UPDATE_INTERVAL, IGNORE_SSL_ERRORS, ATTRIBUTES

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "Authorization": f"Bearer {HASS_TOKEN}",
    "Content-Type": "application/json",
}

def get_frontmost_app_name():
    workspace = NSWorkspace.sharedWorkspace()
    active_app = workspace.frontmostApplication()
    return active_app.localizedName()

def get_frontmost_window_name():
    script = """
    tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
        tell process frontApp
            set frontWindow to name of front window
        end tell
    end tell
    """
    apple_script = NSAppleScript.alloc().initWithSource_(script)
    result, error = apple_script.executeAndReturnError_(None)
    if error:
        return None
    return result.stringValue()

def get_combined_app_window_name():
    app_name = get_frontmost_app_name()
    window_name = get_frontmost_window_name()
    if window_name and app_name != window_name:
        return f"{window_name} — {app_name}"
    return app_name

def update_hass_state(state):
    try:
        data = {
            "state": state,
            "attributes": ATTRIBUTES,
        }
        response = requests.post(
            HASS_URL,
            headers=HEADERS,
            json=data,
            verify=not IGNORE_SSL_ERRORS
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error updating Home Assistant state: {e}")

def handle_exit(signum, frame):
    print("Script exiting, setting state to 'unavailable'")
    update_hass_state("unavailable")
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    print("Script started, reporting frontmost app and window name to Home Assistant...")
    try:
        while True:
            combined_name = get_combined_app_window_name()
            print(f"Current frontmost app and window: {combined_name}")
            update_hass_state(combined_name)
            time.sleep(UPDATE_INTERVAL)
    except KeyboardInterrupt:
        handle_exit(None, None)