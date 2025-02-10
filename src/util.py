from math import log10
import random
import nltk
import numpy as np
import pandas as pd
from nltk import SnowballStemmer
from nltk.corpus import stopwords
from scipy import spatial


def tokenize(data):
    tokenizer = nltk.RegexpTokenizer(r'\w+')

    tok_data = {}
    for id in data:
        tok_data[id] = tokenizer.tokenize(data[id])

    return tok_data


def lowereddata(data):
    lowered_data = {}
    for id in data:
        lowered_data[id] = [word.lower() for word in data[id]]

    return lowered_data


def filterdata(data):
    filtered_data = {}
    english_stopwords = stopwords.words('english')
    for id in data:
        filtered_data[id] = [word for word in data[id] if word not in english_stopwords]

    return filtered_data


def stemmer(data):
    sb_stemmer = SnowballStemmer('english')
    stemmed_data = {}
    for id in data:
        stemmed_data[id] = [sb_stemmer.stem(word) for word in data[id]]

    return stemmed_data


def preProcess(data):
    tok_data = tokenize(data)

    lowered_data = lowereddata(tok_data)

    stemmed_data = stemmer(lowered_data)

    return stemmed_data


def createVocabulary(data):
    vocabulary = []
    for id in data:
        for stem in data[id]:
            if stem not in vocabulary:
                vocabulary.append(stem)

    return vocabulary


def createBOW(data, vocabulary):
    bow = {}
    for id in data:
        bow[id] = np.zeros(len(vocabulary))
        for stem in data[id]:
            index = vocabulary.index(stem)
            bow[id][index] += 1
    return bow


def createDatasetBOW(filepath):
    df = pd.read_csv(filepath)

    data = {}
    labels = {}
    row = 0

    # Add user input to data array
    for entry in df["Input"]:
        data[row] = entry
        row += 1

    # Add ai response to labels array
    row = 0
    for entry in df['Response']:
        labels[row] = entry
        row += 1

    # Preprocess the small talk data and covert it into stemmed documents
    stemmed_data = preProcess(data)

    # Create vocabulary based on small talk dataset
    vocabulary = createVocabulary(stemmed_data)

    # Create Bag of Words model using stemmed data and vocabulary
    bow = createBOW(stemmed_data, vocabulary)

    logfreq_bow = {}
    for id in bow:
        logfreq_bow[id] = logfreq_weighting(bow[id])

    return logfreq_bow, vocabulary, labels


def logfreq_weighting(vector):
    lf_vector = []
    for frequency in vector:
        lf_vector.append(log10(1 + frequency))
    return np.array(lf_vector)


def sim_cosine(vector_1, vector_2):
    if vector_2.any() == 0:
        return 0
    similarity = 1 - spatial.distance.cosine(vector_1, vector_2)
    return similarity


def getUsername():
    userName = input("Chatbot: Hey User! What Can I Call You: \nUser: ")
    return userName;


def getFirstUserQuery(userName):
    userInput = input(
        "Chatbot: Its nice to meet you " + userName + "! I am Chatbot, would you like to engage in small talk, "
                                                      "get information about the UFC or improve your sports general "
                                                      "knowledge? "
                                                      "If you no longer wanna talk please type 'exit'.\n" + userName + ": ")
    return userInput


def getUserQuery(userName):
    userInput = input(
        "Chatbot: Welcome back to the main prompt " + userName + "! Would you like to engage in small talk, "
                                                                 "get information about the UFC or improve your "
                                                                 "sports general "
                                                                 "knowledge? Otherwise type 'exit' if you wanna leave.\n" + userName +
        ": ")
    return userInput


def preProcessQuery(query):
    # Tokenise query
    tokeniser = nltk.RegexpTokenizer(r"\w+")
    tok_query = tokeniser.tokenize(query)

    # Convert query to lower case
    lowered_query = [word.lower() for word in tok_query]

    # Remove stopwords from query
    english_stopwords = stopwords.words('english')
    english_stopwords.remove("doing")
    english_stopwords.remove("how")
    english_stopwords.remove("from")
    english_stopwords.remove("you")
    filtered_query = [word for word in lowered_query if word not in english_stopwords]

    # Stem query
    sb_stemmer = SnowballStemmer('english')
    stemmed_query = [sb_stemmer.stem(word) for word in filtered_query]
    return stemmed_query


def querytoBOW(stemmed_query, vocabulary):
    vector_query = np.zeros(len(vocabulary))
    for stem in stemmed_query:
        if stem in vocabulary:
            index = vocabulary.index(stem)
            vector_query[index] += 1
    logfreq_vector_query = logfreq_weighting(vector_query)
    return logfreq_vector_query


def largestSimilarity(log_freq_bow, log_freq_query):
    similarity = 0
    for id in log_freq_bow.keys():
        tempsimilarity = sim_cosine(log_freq_bow[id], log_freq_query)
        if tempsimilarity > similarity:
            similarity = tempsimilarity
    return similarity


def generateResponse(log_freq_bow, log_freq_query, labels):
    responses = []
    similarity = largestSimilarity(log_freq_bow, log_freq_query)
    for id in log_freq_bow.keys():
        tempsimilarity = sim_cosine(log_freq_bow[id], log_freq_query)
        if tempsimilarity == similarity:
            if tempsimilarity > 0.3:
                responses.append(id)
            else:
                return "I didnt quite get that. Could you please rephrase?"""
    id = random.choice(responses)

    return labels[id]


def processQuery(query, vocabulary):
    stemmed_query = preProcessQuery(query)
    log_freq_query = querytoBOW(stemmed_query, vocabulary)
    return log_freq_query
