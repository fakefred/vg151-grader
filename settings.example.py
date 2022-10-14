CANVAS_TOKEN = ""
COURSE_ID = 41
MOSS_USER_ID = 000000
JOJ_COURSE_ID = "vg151_fall_2022_manuel"
JOJ_SESSION_ID = ""
GITEA_BASE_URL = "https://focs.ji.sjtu.edu.cn/git/api/v1"
GITEA_TOKEN = ""
CANVAS_BASE_URL = "https://jicanvas.com/api/v1"
ORG_NAME = "ENGR151-22"
RUBRIC = {
    "indvFailSubmit": [-0.5, "Individual submission missing"],
    "indvNoReadme": [-0.5, "Individual submission missing README"],
    "indvUntidy": [-0.25, "Individual branch untidy"],
    "groupFailSubmit": [-2.5, "Group submission missing"],
    "groupNoReadme": [-0.5, "Group submission missing README"],
    "groupUntidy": [-0.25, "Group submit untidy"],
    "jojFailHomework": [-0.5, "JOJ: <50% test cases passed for homework"],
    "jojFailExercise": [-0.25, "JOJ: <25% test cases passed for single exercise"],
    "jojFailCompile": [-1, "JOJ: Fails to compile"],
    "indvLowCodeQuality": [-0.25, "Low code quality in individual submission"],
    "groupLowCodeQuality": [-0.25, "Low code quality in group submission"],
    "noReview": [-1, "Did not review teammates' code"],
}
# h3
JOJ_INFO = {
    "lang": "matlab",
    "homeworkID": "6343c69eb6a0b300081b4d46",
    "problemInfo": [
        [["ex1.m"], "6343c517b6a0b300081b4d34", 1],
        [["ex3.m"], "6343c54db6a0b300081b4d37", 1],
        [["ex5.m"], "6343c570b6a0b300081b4d3a", 10],
    ]
}

MANDATORY_FILES = [
    f"ex{i}.m" for i in [1, 3, 5]
]

OPTIONAL_FILES = [
    f"ex{i}.m" for i in [2, 4, 6]
]

PROJ_JOJ_INFO = {
    2: {
        "homeworkID": "5facbf7c9fedcc000661ff9d",
        "problemID": "5facbee89fedcc000661ff8e",
    },
    3: {
        "homeworkID": "5facbf7c9fedcc000661ff9d",
        "problemID": "5facbee89fedcc000661ff8e",
    },
}
