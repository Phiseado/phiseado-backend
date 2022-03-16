import pandas
from sklearn import model_selection
from sklearn.tree import DecisionTreeClassifier
from urllib.parse import urlparse
from ..utils import url_properties

class UrlModel():

    def __init__(self):
        self.model = self.create_and_train_model()
    
    def create_and_train_model(self):
        input_file = 'input_data/dataset_url.csv'
        urls = pandas.read_csv(input_file, header=0)
        atributos = urls.loc[:, 'qty_dot_url':'domain_google_index']
        objetivo = urls['phishing']

        (atributos_entrenamiento, atributos_prueba, objetivo_entrenamiento, objetivo_prueba) = model_selection.train_test_split(
            atributos, objetivo,
            random_state=42,
            test_size=.33,
            stratify=objetivo)

        clasif_Tree = DecisionTreeClassifier(random_state=0)
        clasif_Tree.fit(atributos_entrenamiento, objetivo_entrenamiento)
        return clasif_Tree


def obtain_url_properties(url):
    properties = url_properties.get_number_of_each_property(url)
    properties.append(url_properties.get_length_top_level_domain(url))
    properties.append(len(url))
    properties.append(url_properties.check_is_email_present(url))
    return properties

def obtain_domain_properties(url):
    domain = urlparse(url).netloc
    properties = url_properties.get_number_of_each_property(domain)
    properties.append(url_properties.get_vowels_number(domain))
    properties.append(len(domain))
    properties.append(url_properties.ip_address_format(domain))
    properties.append(1 if "server" in domain or "client" in domain else 0)
    return properties
    
def obtain_directory_properties(url):
    directory = url_properties.get_url_directory(url)
    if directory == "": return [-1] * 18
    properties = url_properties.get_number_of_each_property(directory)
    properties.append(len(directory))
    return properties

def obtain_filename_properties(url):
    filename = url_properties.get_url_filename(url)
    if filename == "": return [-1] * 18
    properties = url_properties.get_number_of_each_property(filename)
    properties.append(len(filename))
    return properties

def obtain_parameters_properties(url):
    parameters = urlparse(url).query
    if parameters == "": return [-1] * 20
    properties = url_properties.get_number_of_each_property(parameters)
    properties.append(len(parameters))
    properties.append(url_properties.is_tld_present_in_params(parameters))
    properties.append(url_properties.number_parameters(parameters))
    return properties

def obtain_extra_properties(url):
    domain = urlparse(url).netloc
    time_response = url_properties.domain_lookup_time_response(domain)
    domain_spf = url_properties.domain_has_spf(domain)
    #asn_ip = delete from the csv
    time_domain_activation = url_properties.get_time_domain_activation(domain)
    time_domain_expiration = url_properties.get_time_domain_expiration(domain)
    #qty_ip_resolved = delete from the csv
    qty_nameservers = url_properties.get_nameservers_resolved(domain)
    qty_mx_servers = url_properties.get_mx_servers(domain)
    ttl_hostname = url_properties.get_tll(domain)
    tls_ssl_certificate = url_properties.has_valid_tls_ssl(url)
    qty_redirects = url_properties.number_redirects(url)
    url_google_index = url_properties.is_indexed_google(url)
    domain_google_index = url_properties.is_indexed_google(domain)
    # url_shortened = delete from csv
    return  [time_response, domain_spf, time_domain_activation, time_domain_expiration, qty_nameservers,
    qty_mx_servers, ttl_hostname, tls_ssl_certificate, qty_redirects, url_google_index, domain_google_index]


def predict_incoming_url(url):
    from ..apps import MainConfig
    incoming_url = []
    url_properties = obtain_url_properties(url)
    domain_properties = obtain_domain_properties(url)
    directory_properties = obtain_directory_properties(url)
    filename_properties = obtain_filename_properties(url)
    parameters_properties = obtain_parameters_properties(url)
    extra_properties = obtain_extra_properties(url)
    incoming_url = url_properties
    [incoming_url.append(property) for property in domain_properties]
    [incoming_url.append(property) for property in directory_properties]
    [incoming_url.append(property) for property in filename_properties]
    [incoming_url.append(property) for property in parameters_properties]
    [incoming_url.append(property) for property in extra_properties]

    prediction = MainConfig.model.predict([incoming_url])
    return prediction