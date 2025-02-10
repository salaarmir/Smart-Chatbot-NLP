import util

def startQandA(userName):

    QandA_BOW, QandA_vocabulary, QandA_answers = util.createDatasetBOW("../datasets/sports.csv")
    user_query = input("Chatbot: Sports General Knowledge! Ask me a random question about sports! Do you know what "
                       "WWE stands for? If you wanna leave, type 'back' to return to the main prompt or 'exit' to say"
                       " goodbye to me\n" + userName + ": ")

    while user_query != "back" and user_query != 'exit':
        processed_query = util.processQuery(user_query, QandA_vocabulary)
        response = util.generateResponse(QandA_BOW, processed_query, QandA_answers)
        print("Chatbot: " + str(response))
        user_query = input("" + userName + ": ")

    if user_query == "exit":
        print("Chatbot: See you soon " + userName + "!")
        exit()
