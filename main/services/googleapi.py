import requests
import json

#Loading the config file
with open('config.json') as file:
    config = json.load(file)

uri = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + config["ApiKey"]


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



  