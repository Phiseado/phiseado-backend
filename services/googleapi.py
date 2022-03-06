import requests
import json

#Loading the config file
with open('config.json') as file:
    config = json.load(file)

url = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + config["ApiKey"]
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