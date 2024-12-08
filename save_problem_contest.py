import configparser
import os

from api.apiCodePTIT import ApiCodePTIT


os.system("cls" if os.name == "nt" else "clear")
config = configparser.ConfigParser()
config.read("config.ini")
username = config["ACCOUNT"]["USERNAME"]
password = config["ACCOUNT"]["PASSWORD"]
apiCodePTIT = ApiCodePTIT(username, password)
if apiCodePTIT.getCookie() == False:
    input("Nhấn [Enter] để thoát chương trình: ")
    exit()
contestList = apiCodePTIT.getListContest()
for contest in contestList:
    problemList = apiCodePTIT.getQuestionListContest(contest)
    for problem in problemList:
        apiCodePTIT.getQuestionInfo(problem)
