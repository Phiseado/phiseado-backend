import requests
import json
import os

try:
  with open('config.json') as file:
      config = json.load(file)
      API_KEY = config["ApiKey"]
except FileNotFoundError:
  print("The specified file doesn't exist. Falling back to environment variables.")
  API_KEY = os.environ.get("ApiKey")

url = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + API_KEY
body = {
    "client": {
      "clientId":      "yourcompanyname",
      "clientVersion": "1.5.2"
    },
    "threatInfo": {
      "threatTypes":      ["MALWARE", "SOCIAL_ENGINEERING", "THREAT_TYPE_UNSPECIFIED", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
      "platformTypes":    ["ANY_PLATFORM"],
      "threatEntryTypes": ["URL"],
      "threatEntries": [
        {"url": "http://m.ok-ai.be/c/0gjf3i"},
        {"url": "https://testsafebrowsing.appspot.com/s/phishing.html"},
        {"url": "http://t.paack.co/t/3bed044c"}
      ]
    }
  }

req = requests.post(url, json = body)
print(req.text)