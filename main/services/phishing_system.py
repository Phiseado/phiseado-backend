from . import googleapi, url_model
import re

def check_message(message):
    url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
    if len(url) == 0:
        return None
    
    url = url[0]

    if googleapi.check_url(url):
        return True
    else:
        prediction = url_model.predict_incoming_url(url)
        if prediction == 1:
            return True
        else:
            # TODO: check message content model
            return False