from aiohttp import request
import requests

url = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=APIKEY"
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