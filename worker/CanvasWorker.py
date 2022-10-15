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
        # scoreInfo data structure:
        # {criterion (str): deducted (int, non-zero when deduction applies), ...}
        # rubric data structure:
        # {criterion (str): [deduction (float, negative), comment (str)], ...}
        score = 0
        deductions = []
        for criterion, (deduction, comment) in self.rubric.items():
            if scoreInfo.get(criterion, 0):
                score += deduction  # deduction is negative
                deductions.append((deduction, comment))

        comment = "Good job"
        if score < 0:
            indvComment = "; ".join(scoreInfo.get("indvComment", []))
            groupComment = "; ".join(scoreInfo.get("groupComment", []))
            jojComment = "; ".join(scoreInfo.get("jojComment", []))
            deductionsComment = (
                "; ".join(
                    [f"{comment} ({deduction})" for deduction, comment in deductions]
                )
                or "N/A"
            )
            detailsComment = (
                "; ".join(
                    scoreInfo.get("indvComment", [])
                    + scoreInfo.get("groupComment", [])
                    + scoreInfo.get("jojComment", [])
                )
                or "N/A"
            )
            comment = (
                "[Deductions] " + deductionsComment + " [Details] " + detailsComment
            )
        return {
            "submission": {"posted_grade": max(score, -2.5)},
            "comment": {"text_comment": comment},
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
            self.logger.info(f"{name} {data['comment']['text_comment']}")
