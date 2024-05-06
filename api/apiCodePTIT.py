import os
import time
import random
import json
import configparser

try:
    import requests
    from colorama import Fore, init
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    print("Đang cài đặt các thư viện cần thiết, vui lòng chờ...")
    os.system("python3 -m pip install requests")
    os.system("python3 -m pip install colorama")
    os.system("python3 -m pip install beautifulsoup4")
    import requests
    from colorama import Fore, init
    from bs4 import BeautifulSoup

from api.model import *


class ApiCodePTIT:
    count = 0

    def __init__(self, username, password):
        init(autoreset=True)
        self.host = "https://code.ptit.edu.vn"
        self.header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        }
        self.course = None
        self.username = username
        self.password = password
        self.name = None
        self.id = None
        self.pageCount = 0

        self.path = os.getcwd()

        config = configparser.ConfigParser()
        config.read("config.ini")
        nameFolder = config["SETTINGS"]["NAME_FOLDER"]
        self.timeDelay = int(config["SETTINGS"]["TIME_DELAY"])

        self.path = f"{self.path}/{nameFolder}"
        try:
            os.makedirs(self.path)
        except FileExistsError:
            pass

    def getCookie(self):
        login = requests.get(url=f"{self.host}/login")
        set_cookie = login.headers.get("Set-Cookie").split("samesite=lax, ")[1]
        _token = login.text.split('_token" value="')[1].split('"')[0]
        data = {
            "username": self.username,
            "password": self.password,
            "_token": _token,
        }
        self.header.update({"Cookie": set_cookie})
        login = requests.post(url=f"{self.host}/login", data=data, headers=self.header)
        self.header.update(
            {"Cookie": login.headers.get("Set-Cookie").split("samesite=lax, ")[1]}
        )

        try:
            self.name = login.text.split('<p class="nav__profile__menu__name">')[
                1
            ].split("</p>")[0]
            self.id = login.text.split('<p class="nav__profile__menu__code">')[1].split(
                "</p>"
            )[0]
        except IndexError:
            print(
                f"{Fore.RED}Đăng nhập thất bại, vui lòng kiểm tra lại tài khoản{Fore.RESET}"
            )
            return False

        print(f"{Fore.GREEN}Đăng nhập thành công{Fore.RESET}")
        print(
            f"Xin chào {Fore.LIGHTBLUE_EX}{self.name}{Fore.RESET}. Mã sinh viên: {Fore.LIGHTBLUE_EX}{self.id}{Fore.RESET}"
        )

    def getGroupList(self):
        groups = requests.get(url=f"{self.host}/student/question", headers=self.header)
        groups = BeautifulSoup(groups.text, "html.parser").find("select")
        groupsList = []
        for group in groups.find_all("option"):
            try:
                groupID = group["value"]
                groupName = group.text.strip()
                groupsList.append(GroupInfo(groupID, groupName))
            except KeyError:
                pass
        return groupsList

    def setCourse(self, course):
        self.course = course

    def getPageCount(self):
        questions = requests.get(
            url=f"{self.host}/student/question",
            headers=self.header,
            params={"course": self.course},
        )
        pageCount = (
            BeautifulSoup(questions.text, "html.parser")
            .find_all("ul", class_="pagination")[0]
            .find_all("li")
        )
        self.pageCount = int(pageCount[-2].text.strip())

    def getQuestionsInPage(self, page):
        questions = requests.get(
            url=f"{self.host}/student/question",
            headers=self.header,
            params={
                "page": page,
                "course": self.course if self.course and page == 1 else "",
            },
        )
        completeQuestionsList = []
        incompleteQuestionsList = []
        try:
            problems = BeautifulSoup(questions.text, "html.parser").find_all("tbody")[0]
            problems = problems.find_all("tr")
            problems[0].find_all("a")[1]
        except IndexError:
            problems = BeautifulSoup(questions.text, "html.parser").find_all("tbody")[1]
            problems = problems.find_all("tr")
        for problem in problems:
            problemName = problem.find_all("a")[1].text.strip()
            problemName = " ".join(problemName.split())
            problemLink = problem.find_all("a")[0]["href"].strip()
            problemID = problem.find_all("a")[0].text.strip()
            problemGroup = problem.find_all("td")[4].text.strip()
            problemTopic = problem.find_all("td")[5].text.strip()
            problemDifficulty = problem.find_all("td")[6].text.strip()
            if "bg--10th" in problem.get("class", []):
                problemStatus = "Complete"
                completeQuestionsList.append(
                    ProblemInfo(
                        problemName,
                        problemLink,
                        problemID,
                        problemStatus,
                        problemGroup,
                        problemTopic,
                        problemDifficulty,
                    )
                )
            else:
                problemStatus = "Incomplete"
                incompleteQuestionsList.append(
                    ProblemInfo(
                        problemName,
                        problemLink,
                        problemID,
                        problemStatus,
                        problemGroup,
                        problemTopic,
                        problemDifficulty,
                    )
                )

        return completeQuestionsList, incompleteQuestionsList

    def getSolutionQuestion(self, question=ProblemInfo):
        questions = requests.get(url=f"{question.problemLink}", headers=self.header)
        solutionList = []
        index = 0
        while True:
            try:
                solutionTable = BeautifulSoup(questions.text, "html.parser").find_all(
                    "tbody"
                )[index]

                solutionTable = solutionTable.find_all("tr")
                for solution in solutionTable:
                    solutionID = solution.find_all("td")[0].text.strip()
                    solutionTimeSubmit = solution.find_all("td")[1].text.strip()
                    solutionName = solution.find_all("td")[2].text.strip()
                    solutionName = " ".join(solutionName.split())
                    solutionStatus = solution.find_all("td")[3].text.strip()
                    solutionLink = solution.find_all("td")[3].find_all("a")[0]["href"]
                    solutionTime = solution.find_all("td")[4].text.strip()
                    solutionMemory = solution.find_all("td")[5].text.strip()
                    solutionLanguage = solution.find_all("td")[6].text.strip()

                    solutionList.append(
                        SolutionInfo(
                            solutionID,
                            solutionTimeSubmit,
                            solutionName,
                            solutionLink,
                            solutionStatus,
                            solutionTime,
                            solutionLanguage,
                            solutionMemory,
                        )
                    )
                break
            except IndexError:
                index += 1
        return solutionList

    def getSolutionAC(self, solution=SolutionInfo, question=ProblemInfo):
        ApiCodePTIT.count += 1

        request = requests.get(url=f"{solution.solutionLink}", headers=self.header)
        solutionCode = BeautifulSoup(request.text, "html.parser").find(
            "input", id="source_code"
        )["value"]

        # CLean lại code
        lines = solutionCode.splitlines()
        cleaned_lines = [line.strip("\r") for line in lines if line.strip()]
        cleanedSolutionCode = "\n".join(cleaned_lines)

        # Save source code
        extensionFile = ".txt"
        for language in languageCodeList:
            if language.name == solution.solutionLanguage:
                extensionFile = language.extension
                break
        if os.path.exists(
            f"{self.path}/{question.problemID} - {question.problemName}{extensionFile}"
        ):
            print(
                f"{Fore.YELLOW}[{ApiCodePTIT.count}] Đã tồn tại source code bài {question.problemID} - {question.problemName}{Fore.RESET}"
            )
        else:
            with open(
                f"{self.path}/{question.problemID} - {question.problemName}{extensionFile}",
                "w",
                encoding="utf-8",
            ) as file:
                file.write(cleanedSolutionCode)
            print(
                f"{Fore.GREEN}[{ApiCodePTIT.count}] Tải source code bài {question.problemID} - {question.problemName} thành công{Fore.RESET}"
            )
        delay = random.uniform(1, self.timeDelay)
        print(f"{Fore.LIGHTCYAN_EX}Nghỉ ngơi {delay:.2f} giây{Fore.RESET}", end="\r")
        time.sleep(delay)
