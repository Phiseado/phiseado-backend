import pandas
from sklearn import model_selection
from sklearn.tree import DecisionTreeClassifier
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
nltk.download('stopwords')

class ContentModel():
    
    def __init__(self):
        '''
        This class is used to train the model and to predict if a message is phishing or not.
        '''
        self.model = self.create_and_train_model()

    def create_and_train_model(self):
        input_file = 'input_data/dataset_content.csv'
        urls = pandas.read_csv(input_file, header=0)
        atributos = urls.loc[:, 'Total Number of Characters C':'Unique Words']
        objetivo = urls['Phishing Status']

        (atributos_entrenamiento, atributos_prueba, objetivo_entrenamiento, objetivo_prueba) = model_selection.train_test_split(
            atributos, objetivo,
            random_state=42,
            test_size=.33,
            stratify=objetivo)

        clasif_Tree = DecisionTreeClassifier(random_state=0)
        clasif_Tree.fit(atributos_entrenamiento, objetivo_entrenamiento)

        return clasif_Tree

def get_function_words(message):
    stop_words = set(stopwords.words('spanish'))
    word_tokens = word_tokenize(message)
    filtered_sentence = [w for w in word_tokens if w in stop_words]
    return len(filtered_sentence)

def obtain_message_properties(message):
    number_words = len(message.split())
    number_characters = len(message)
    vocabulary_richness = number_words / number_characters
    format_message = message.lower()
    account = format_message.count("cuenta")
    acces = format_message.count("acceso") + format_message.count("accesos")
    bank = format_message.count("banco")
    credit = format_message.count("crédito") + format_message.count("créditos") + format_message.count("creditos")
    click = format_message.count("click")
    identity = format_message.count("identidad")
    inconvenience = format_message.count("inconveniente")
    information = format_message.count("información") + format_message.count("informacion")
    limited = format_message.count("limitado")
    minutes = format_message.count("minutos")
    password = format_message.count("contraseña")
    recently = format_message.count("recientemente")
    risk = format_message.count("riesgo")
    social = format_message.count("social")
    security = format_message.count("seguridad")
    service = format_message.count("servicio")
    suspended = format_message.count("suspendido")
    number_functions_words = get_function_words(message) / number_words
    unique_words = len(set(format_message.split()))
    return [number_characters,vocabulary_richness,account,acces,bank,credit,click,identity,inconvenience,information,limited,
    minutes,password,recently,risk,social,security,service,suspended,number_functions_words,unique_words]

def predict_incoming_message(message):
    from ..apps import CONTENT_model
    
    incoming_message = obtain_message_properties(message)
    prediction = CONTENT_model.predict([incoming_message])
    return prediction