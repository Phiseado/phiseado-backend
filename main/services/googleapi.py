import requests
import json
import os

try:
  with open('config.json') as file:
      config = json.load(file)
      API_KEY = config["ApiKey"]
except FileNotFoundError:
  print("The specified file doesn't exist. Falling back to environment variables.")
  API_KEY = os.environ.get("API_KEY")

uri = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + API_KEY


def check_url(url):
  body = {
      "client": {
        "clientId":      "phiseado",
        "clientVersion": "0.0.1"
      },
      "threatInfo": {
        "threatTypes":      ["MALWARE", "SOCIAL_ENGINEERING", "THREAT_TYPE_UNSPECIFIED", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
        "platformTypes":    ["ANY_PLATFORM"],
        "threatEntryTypes": ["URL"],
        "threatEntries": [
          {"url": url}
        ]
      }
    }
  
  response = requests.post(uri, json = body).json()
  return "matches" in response



  