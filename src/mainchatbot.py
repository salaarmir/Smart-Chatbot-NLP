import util
from sports import startQandA
from intentmatching import intentMatcher
from smalltalk import startSmallTalk
from ufc import startUFCTalk

userName = util.getUsername()
userquery = util.getFirstUserQuery(userName)
while userquery != "exit":
    userIntent = intentMatcher(userquery)
    if userIntent == "Small talk":
        startSmallTalk(userName)
        userquery = util.getUserQuery(userName)
    elif userIntent == "UFC":
        startUFCTalk(userName)
        userquery = util.getUserQuery(userName)
    elif userIntent == "General knowledge":
        startQandA(userName)
        userquery = util.getUserQuery(userName)
    else:
        print('Chatbot: I didnt get that, could you please rephrase?')
        userquery = input("" + userName + ": ")

print("Chatbot: See you soon " + userName + "!")
