class ProblemInfo:
    def __init__(
        self,
        problemName,
        problemLink,
        problemID,
        problemStatus,
        problemGroup,
        problemTopic,
        problemDifficulty,
    ):
        self.problemName = problemName
        self.problemLink = problemLink
        self.problemID = problemID
        self.problemStatus = problemStatus
        self.problemGroup = problemGroup
        self.problemTopic = problemTopic
        self.problemDifficulty = problemDifficulty


class SolutionInfo:
    def __init__(
        self,
        solutionID,
        solutionTimeSubmit,
        solutionName,
        solutionLink,
        solutionStatus,
        solutionTime,
        solutionLanguage,
        solutionMemory,
    ):
        self.solutionID = solutionID
        self.solutionTimeSubmit = solutionTimeSubmit
        self.solutionName = solutionName
        self.solutionLink = solutionLink
        self.solutionStatus = solutionStatus
        self.solutionTime = solutionTime
        self.solutionLanguage = solutionLanguage
        self.solutionMemory = solutionMemory


class GroupInfo:
    def __init__(self, groupID, groupName):
        self.groupID = groupID
        self.groupName = groupName


class LanguageCode:
    def __init__(self, name, extension):
        self.name = name
        self.extension = extension


languageCodeList = [
    LanguageCode("C", ".c"),
    LanguageCode("C/C++", ".cpp"),
    LanguageCode("Python 3", ".py"),
    LanguageCode("Java", ".java"),
    LanguageCode("C#", ".cs"),
    LanguageCode("Golang", ".go"),
]
