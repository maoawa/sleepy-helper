# config.py
HASS_URL = "https://your-home.example.net/api/states/input_text.my_windows"
HASS_TOKEN = "Long-lived access tokens generated at the bottom of user page (bottom left corner of dashboard)"
UPDATE_INTERVAL = 10
IGNORE_SSL_ERRORS = False
ATTRIBUTES = {
    "editable": "true",
    "min": 0,
    "max": 255,
    "pattern": "null",
    "mode": "text",
    "icon": "mdi:monitor",
    "friendly_name": "My Windows",
}