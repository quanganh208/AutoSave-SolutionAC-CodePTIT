from api.apiCodePTIT import *


def getListSourceCode(completeQuestionsList):
    for question in completeQuestionsList:
        solutionList = apiCodePTIT.getSolutionQuestion(question)
        for solution in solutionList:
            if solution.solutionStatus == "AC":
                apiCodePTIT.getSolutionAC(solution, question)
                break


def main():
    os.system("cls" if os.name == "nt" else "clear")
    if apiCodePTIT.getCookie() == False:
        input("Nhấn [Enter] để thoát chương trình: ")
        return

    # Check group
    groupList = apiCodePTIT.getGroupList()
    if len(groupList) > 1:
        print(
            f"{Fore.LIGHTMAGENTA_EX}Tìm thấy {len(groupList)} nhóm. Vui lòng chọn nhóm để tải source code:{Fore.RESET}"
        )
        for index, group in enumerate(groupList):
            print(f"{index + 1}. {group.groupName}")

        groupIndex = int(input(f"{Fore.LIGHTCYAN_EX}Nhập số thứ tự nhóm: {Fore.RESET}"))
        apiCodePTIT.setCourse(groupList[groupIndex - 1].groupID)
        print(
            f"{Fore.GREEN}Đã chọn nhóm {groupList[groupIndex - 1].groupName}{Fore.RESET}"
        )

    # Get list question
    print(f"{Fore.LIGHTYELLOW_EX}Đang tìm kiếm bài đã làm và chưa làm...{Fore.RESET}")
    apiCodePTIT.getPageCount()
    completeQuestionsList, incompleteQuestionsList = [], []
    for index in range(1, apiCodePTIT.pageCount + 1):
        completeList, incompleteList = apiCodePTIT.getQuestionsInPage(index)
        completeQuestionsList += completeList
        incompleteQuestionsList += incompleteList
    print(
        f"Đã tìm thấy {Fore.GREEN}{len(completeQuestionsList)} bài đã làm{Fore.RESET} và {Fore.RED}{len(incompleteQuestionsList)} bài chưa làm{Fore.RESET}"
    )

    # Get list source code
    print(f"{Fore.LIGHTGREEN_EX}Bắt đầu tải source code...{Fore.RESET}")
    getListSourceCode(completeQuestionsList)
    print(f"{Fore.LIGHTGREEN_EX}Hoàn thành tải source code{Fore.RESET}")
    input("Nhấn [Enter] để thoát chương trình: ")
    return


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    username = config["ACCOUNT"]["USERNAME"]
    password = config["ACCOUNT"]["PASSWORD"]
    apiCodePTIT = ApiCodePTIT(username, password)
    main()
