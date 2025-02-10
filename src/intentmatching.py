import util

def generateIntentResponse(log_freq_bow, log_freq_query, intents):
    response = 0

    for id in log_freq_bow.keys():
        tempsimilarity = util.sim_cosine(log_freq_bow[id], log_freq_query)
        if tempsimilarity > 0.2:
            return intents[id]
        else:
            pass

    return "I didnt quite get that. Could you please rephrase?"


def intentMatcher(userquery):
    log_freq_bow, vocabulary, intents = util.createDatasetBOW("../datasets/intentmatching.csv")
    log_freq_query = util.processQuery(userquery, vocabulary)

    userintent = generateIntentResponse(log_freq_bow, log_freq_query, intents)
    return userintent
