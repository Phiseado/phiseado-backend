import pandas
from sklearn import model_selection
from sklearn.tree import DecisionTreeClassifier
from urllib.parse import urlparse
import re
import socket

class UrlModel():

    def __init__(self):
        self.model = self.create_and_train_model()
    
    def create_and_train_model(self):
        input_file = 'input_data/tb1_tb2_dataset_urls.csv'
        urls = pandas.read_csv(input_file, header=0)
        atributos = urls.loc[:, 'qty_dot_url':'email_in_url']
        objetivo = urls['phishing']

        (atributos_entrenamiento, atributos_prueba, objetivo_entrenamiento, objetivo_prueba) = model_selection.train_test_split(
            atributos, objetivo,
            random_state=42,
            test_size=.33,
            stratify=objetivo)

        clasif_Tree = DecisionTreeClassifier(random_state=0)
        clasif_Tree.fit(atributos_entrenamiento, objetivo_entrenamiento)
        return clasif_Tree

def get_length_top_level_domain(url):
    url = urlparse(url)
    domain = url.netloc
    domain = domain.split('.')
    return (0, len(domain[-1]))[len(domain)>1]

def check_is_email_present(url):
    if re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url):
        return 1
    else:
        return 0

def get_vowels_number(domain):
    vowels = 0
    for i in domain:
        if i in "aeiouAEIOU":
            vowels += 1
    return vowels

def ip_address_format(domain):
    try:
        socket.inet_aton(domain)
        return 1
    except socket.error:
        return 0

def obtain_url_properties(url):
    qty_dot = url.count('.')
    qty_hyphen = url.count('-')
    qty_underline = url.count('_')
    qty_slash = url.count('/')
    qty_questionmark = url.count('?')
    qty_equal = url.count('=')
    qty_at = url.count('@')
    qty_and = url.count('&')
    qty_exclamation = url.count('!')
    qty_space = url.count(' ')
    qty_tilde_url = url.count('~')
    qty_comma_url = url.count(',')
    qty_plus_url = url.count('+')
    qty_asterisk_url = url.count('*')
    qty_hash_url = url.count('#')
    qty_dollar_url = url.count('$')
    qty_percent_url = url.count('%')
    qty_length_top_level_domain = get_length_top_level_domain(url)
    length = len(url)
    is_email_present = check_is_email_present(url)

    return [qty_dot, qty_hyphen, qty_underline, qty_slash, qty_questionmark, qty_equal, qty_at, qty_and, qty_exclamation, qty_space, qty_tilde_url, qty_comma_url, qty_plus_url, qty_asterisk_url, qty_hash_url, qty_dollar_url, qty_percent_url, qty_length_top_level_domain, length, is_email_present]

def obtain_domain_properties(url):
    domain = urlparse(url).netloc
    qty_dot = domain.count('.')
    qty_hyphen = domain.count('-')
    qty_underline = domain.count('_')
    qty_slash = domain.count('/')
    qty_questionmark = domain.count('?')
    qty_equal = domain.count('=')
    qty_at = domain.count('@')
    qty_and = domain.count('&')
    qty_exclamation = domain.count('!')
    qty_space = domain.count(' ')
    qty_tilde_domain = domain.count('~')
    qty_comma_domain = domain.count(',')
    qty_plus_domain = domain.count('+')
    qty_asterisk_domain = domain.count('*')
    qty_hash_domain = domain.count('#')
    qty_dollar_domain = domain.count('$')
    qty_percent_domain = domain.count('%')
    qty_vowels = get_vowels_number(domain)
    qty_length = len(domain)
    domain_in_ip = ip_address_format(domain)
    server_client = (0, 1)["server" in domain or "client" in domain]

    return [qty_dot, qty_hyphen, qty_underline, qty_slash, qty_questionmark, qty_equal, qty_at, qty_and, qty_exclamation, qty_space, qty_tilde_domain, qty_comma_domain, qty_plus_domain, qty_asterisk_domain, qty_hash_domain, qty_dollar_domain, qty_percent_domain, qty_vowels, qty_length, domain_in_ip, server_client]

def predict_incoming_url(url):
    from ..apps import MainConfig
    incoming_url = []
    url_properties = obtain_url_properties(url)
    domain_properties = obtain_domain_properties(url)
    incoming_url = url_properties
    [incoming_url.append(property) for property in domain_properties]

    prediction = MainConfig.model.predict([incoming_url])
    return prediction