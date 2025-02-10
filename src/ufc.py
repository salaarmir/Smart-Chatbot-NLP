import nltk
import requests
import wikipedia
from nltk import tokenize

import util
from util import preProcess, createBOW


def createUFCTextFile(url):
    res = requests.get(url)
    res.raise_for_status()
    result = wikipedia.search("UFC")
    firstpage = wikipedia.page(result[0])
    secondpage = wikipedia.page(result[1])
    content = firstpage.content
    content = content + secondpage.content

    return content


def processUFCData(content):
    tokeniser = nltk.RegexpTokenizer(r"\w+")
    sent_tokens = tokenize.sent_tokenize(content)
    sent_dict = {}
    id = 0
    for sent in sent_tokens:
        sent_dict[id] = sent
        id += 1

    stemmed_data = preProcess(sent_dict)

    return stemmed_data, sent_dict


def createUFCVocabulary(data):
    vocabulary = []
    for word in data:
        if word not in vocabulary:
            vocabulary.append(word)

    return vocabulary


def generateUFCResponse(log_freq_bow, log_freq_query, sentences):
    responses = []
    for id in log_freq_bow.keys():

        tempsimilarity = util.sim_cosine(log_freq_bow[id], log_freq_query)
        if tempsimilarity == util.largestSimilarity(log_freq_bow, log_freq_query):
            if tempsimilarity > 0.45:

                responses.append(sentences[id])
                if id != 0:
                    responses.append(sentences[id - 1])
                responses.append(sentences[id + 1])
            else:
                pass
    if len(responses) == 0:
        responses.append("I didnt quite get that. Could you please rephrase?")

    return responses


def startUFCTalk(userName):
    UFC_data = createUFCTextFile("https://en.wikipedia.org/wiki/Ultimate_Fighting_Championship")
    stemmed_tokens, sent_dict = processUFCData(UFC_data)

    ufc_vocabulary = util.createVocabulary(stemmed_tokens)

    ufc_bow = createBOW(stemmed_tokens, ufc_vocabulary)

    logfreq_bow = {}
    for id in ufc_bow:
        logfreq_bow[id] = util.logfreq_weighting(ufc_bow[id])

    user_query = input(
        "Chatbot: You picked the UFC! Type in a word or phrase to get information about that topic! If you wanna "
        "leave, type 'back' to return to the main prompt or 'exit' if you dont want to talk to me anymore\n" +
        userName + ": ")
    while user_query != "back" and user_query != 'exit':
        processed_query = util.processQuery(user_query, ufc_vocabulary)
        response = generateUFCResponse(ufc_bow, processed_query, sent_dict)
        if len(response) > 1:
            print("Chatbot: ")
            for sent in response:
                print(sent)
        else:
            error_response = response[0]
            print("Chatbot: " + str(error_response))
        user_query = input("" + userName + ": ")

    if user_query == "exit":
        print("Chatbot: See you soon " + userName + "!")
        exit()
