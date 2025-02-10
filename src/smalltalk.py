import util


def startSmallTalk(userName):
    smalltalkBOW, small_talk_vocabulary, small_talk_responses = util.createDatasetBOW("../datasets/basicsmalltalk.csv")
    user_query = input("Chatbot: Small talk it is! We can talk about a lot of different things! Try asking me to tell "
                       "you a joke! If you wanna leave, type 'back' to return to the main prompt or 'exit' to shut me"
                       " down\n" + userName + ": ")

    while user_query != "back" and user_query != 'exit':
        processed_query = util.processQuery(user_query, small_talk_vocabulary)
        response = util.generateResponse(smalltalkBOW, processed_query, small_talk_responses)
        print("Chatbot: " + str(response))
        user_query = input("" + userName + ": ")

    if user_query == "exit":
        print("Chatbot: See you soon " + userName + "!")
        exit()
