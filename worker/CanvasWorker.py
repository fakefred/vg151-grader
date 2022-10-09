from canvasapi import Canvas
from util import first, Logger, dumpJson, mergeDicts
import json


class CanvasWorker:
    def __init__(
        self,
        args,
        rubric,
        canvasToken,
        courseID,
        names,
        totalScores,
        logger=Logger(),
    ):
        self.args = args
        self.rubric = rubric
        self.canvas = Canvas("https://jicanvas.com/", canvasToken)
        self.course = self.canvas.get_course(courseID)
        self.users = self.course.get_users()
        self.assignments = self.course.get_assignments()
        self.logger = logger
        self.scores = {}
        self.names = names
        self.scores = totalScores

    def generateHomeworkData(self, scoreInfo):
        score = 0
        comment = []
        for key, value in self.rubric.items():
            for _ in range(scoreInfo.get(key, 0)):
                score += value[0]
                comment.append(f"{value[1]}, {value[0]}")
        if not comment:
            comment = ["Good job"]
        else:
            comment.insert(0, "General Info:")
            comment.append("")
            comment.append("Details:")
            comment.extend(
                scoreInfo.get("indvComment", [])
                + scoreInfo.get("groupComment", [])
                + scoreInfo.get("jojComment", [])
            )
        return {
            "submission": {"posted_grade": max(score, -2.5)},
            "comment": {"text_comment": "\n".join(comment)},
        }

    def grade2Canvas(self):
        hwNum = self.args.hw
        assignment = first(self.assignments, lambda x: x.name.startswith(f"h{hwNum}"))
        for submission in assignment.get_submissions():
            currentUser = first(self.users, lambda user: user.id == submission.user_id)
            if currentUser is None:
                continue
            name = currentUser.name.strip()
            if name.lower() not in [n.lower() for n in self.names]:
                continue
            if not self.scores[name.title()]:
                continue
            data = self.generateHomeworkData(self.scores[name.title()])
            self.logger.debug(f"{name} {data.__repr__()}")
            submission.edit(**data)
            self.logger.info(f"Canvas: graded {name}")
