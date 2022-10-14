#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
import os

from worker import CanvasWorker, GitWorker, JOJWorker, GiteaWorker
from settings import *
from util import loadJson, dumpJson, mergeDicts


def parseArgs():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "--help", action="store_true", help="show this help message and exit"
    )
    parser.add_argument("-h", "--hw", type=int, help="homework #")
    parser.add_argument("-p", "--proj", type=int, help="project #")
    parser.add_argument(
        "-f", "--feedback", action="store_true", help="give feedback to project"
    )
    parser.add_argument("-m", "--ms", type=int, help="milestone #")
    parser.add_argument(
        "-r", "--rejudge", type=int, default=-1, help="rejudge group num or stu ID"
    )
    parser.add_argument(
        "-a", "--all", action="store_true", help="check all (-i -d -g -j -t -s)"
    )
    parser.add_argument(
        "-s", "--score", action="store_true", help="save score to output/scores.json"
    )
    parser.add_argument("-t", "--tidy", action="store_true", help="check tidy")
    # TODO: automatically check moss
    parser.add_argument("-o", "--moss", action="store_true", help="check moss")
    parser.add_argument(
        "-d", "--dir", action="store_true", help="create dir for individual submission"
    )
    parser.add_argument(
        "-i", "--indv", action="store_true", help="check individual submission"
    )
    parser.add_argument(
        "-g", "--group", action="store_true", help="check group submission"
    )
    parser.add_argument("-j", "--joj", action="store_true", help="check joj score")
    parser.add_argument(
        "-u", "--upload", action="store_true", help="upload score to canvas"
    )
    parser.add_argument(
        "--upload-from-json",
        action="store_true",
        help="upload score from output/scores.json to canvas",
    )
    args = parser.parse_args()
    if args.help:
        parser.print_help()
        exit(0)
    if args.all:
        args.indv = True
        args.dir = True
        args.group = True
        args.joj = True
        args.tidy = True
        args.score = True
    return args


if __name__ == "__main__":
    hgroups = loadJson("hgroups.json")
    pgroups = loadJson("pgroups.json")
    names = [item[1] for value in hgroups.values() for item in value]
    args = parseArgs()
    indvScores, groupScores, jojScores = {}, {}, {}
    # earlier, mandatoryFiles was mutated to include every exercise on JOJ
    # but it is not necessarily useful
    mandatoryFiles = MANDATORY_FILES
    gitWorker = (
        GitWorker(
            args, hgroups, pgroups, JOJ_INFO["lang"], mandatoryFiles, OPTIONAL_FILES
        )
        if args.indv or args.group or args.proj
        else None
    )
    giteaWorker = GiteaWorker(args, GITEA_BASE_URL, ORG_NAME, GITEA_TOKEN, hgroups)
    if args.indv:
        indvScores = gitWorker.checkIndv()

    if args.group:
        groupScores = gitWorker.checkGroup()
        tmpScores = giteaWorker.checkReview()
        for student in groupScores.keys():
            groupScores[student] = {**groupScores.get(student, {}), **tmpScores.get(student, {})}

    if args.indv or args.group:
        if args.joj:
            jojWorker = JOJWorker(args, JOJ_COURSE_ID, JOJ_SESSION_ID, hgroups)
            jojScores = jojWorker.checkGroupJOJ(JOJ_INFO)
            dumpJson(jojScores, "output/joj.json")

    totalScores = mergeDicts(indvScores, groupScores, jojScores)
    if args.score:
        dumpJson(totalScores, "output/scores.json")

    if args.upload:
        if not totalScores:
            totalScores = loadJson("output/scores.json")
        canvasWorker = CanvasWorker(
            args,
            RUBRIC,
            CANVAS_TOKEN,
            COURSE_ID,
            names,
            totalScores,
        )
        canvasWorker.grade2Canvas()

    if args.proj:
        projScores = gitWorker.checkProj(args.proj, args.ms)
        if args.joj:
            jojWorker = JOJWorker(args, JOJ_COURSE_ID, JOJ_COURSE_ID, hgroups)
            jojScores = jojWorker.checkProjJOJ(PROJ_JOJ_INFO)
            for key in projScores.keys():
                projScores[key] = {**projScores.get(key, {}), **jojScores.get(key, {})}
        if args.feedback:
            giteaWorker.raiseIssues(projScores)
