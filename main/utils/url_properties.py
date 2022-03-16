import re
import socket
import time
import dns.resolver
import whois
import datetime
import ssl
import urllib.request as request
from urllib.parse import urlparse
from googlesearch import search

def get_number_of_each_property(string):
    characters = ['.', '-', '_', '/', '?', '=', '@', '&', '!', ' ', '~', ',', '+', '*', '#', '$', '%']
    count_properties = []
    for character in characters:
        count_properties.append(string.count(character))
    return count_properties

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

def get_url_directory(url):
    path = urlparse(url).path
    paths = path.split('/')
    if '.' in paths[-1]:
        return '/'.join(paths[:-1])
    else:
        return path

def get_url_filename(url):
    path = urlparse(url).path
    paths = path.split('/')
    if '.' in paths[-1]:
        return paths[-1]
    else:
        return ""

def is_tld_present_in_params(parameters):
    params = parameters.split('&')
    for param in params:
        if 'tld' in param:
            return 1
    return 0

def number_parameters(parameters):
    if parameters == "":
        return 0
    number_params = len(parameters.split('&'))
    return number_params

def domain_lookup_time_response(domain):
    start = time.time()
    try:
        dns.resolver.query(domain, 'A')
    except:
        pass
    end = time.time()
    return end - start

def domain_has_spf(domain):
    try:
        answers = dns.resolver.query(domain, 'TXT')
        for rdata in answers:
            if rdata.to_text().find('v=spf1') != -1:
                return 1
            else:
                return 0
    except:
        return 0

def get_time_domain_activation(domain):
    try:
        whois_info = whois.whois(domain)
        creation_date = whois_info.creation_date
        if creation_date:
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            return (datetime.datetime.now() - creation_date).days            
        else:
            return -1
    except Exception as e:
        return -1

def get_time_domain_expiration(domain):
    try:
        whois_info = whois.whois(domain)
        expiration_date = whois_info.expiration_date
        if expiration_date:
            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]
            return (expiration_date - datetime.datetime.now()).days
        else:
            return -1
    except:
        return -1

def get_nameservers_resolved(domain):
    try:
        ns = dns.resolver.query(domain, 'NS')
        return len(ns)
    except:
        return 0

def get_mx_servers(domain):
    try:
        ns = dns.resolver.query(domain, 'MX')
        return len(ns)
    except:
        return 0

def get_tll(domain):
    try:
        resolver = dns.resolver.Resolver()
        dns_response = resolver.query(domain, 'A')
        ttl = dns_response.rrset.ttl
        return ttl
    except:
        return -1

def has_valid_tls_ssl(url):
    try:
        context = ssl._create_unverified_context()
        request.urlopen(url, context=context)
        return 1
    except:
        return 0

def number_redirects(url):
    try:
        response = request.urlopen(url)
        num_redirects = 0
        while response.geturl() != url:
            num_redirects += 1
            url = response.geturl()
            response = request.urlopen(url)
        return num_redirects
    except:
        return -1

def is_indexed_google(url):
    query = "site:" + url
    for result in search(query, pause=1):
        return 1
    return 0
