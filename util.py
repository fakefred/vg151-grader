import subprocess
import logging
import os
import re
import json


class Logger:
    _instance = None

    def __new__(cls, fileName="VG101GradeHelper.log", loggerName="myLogger"):
        if cls._instance is None:
            logger = logging.getLogger(loggerName)
            formatter = logging.Formatter(
                "[%(asctime)s][%(levelname)8s][%(filename)s %(lineno)3s]%(message)s"
            )
            logger.setLevel(logging.DEBUG)
            streamHandler = logging.StreamHandler()
            streamHandler.setFormatter(formatter)
            streamHandler.setLevel(logging.INFO)
            fileHandler = logging.FileHandler(filename=fileName)
            fileHandler.setFormatter(formatter)
            fileHandler.setLevel(logging.DEBUG)
            logger.addHandler(fileHandler)
            logger.addHandler(streamHandler)
            cls._instance = logger
        return cls._instance


def first(iterable, condition=lambda x: True):
    try:
        return next(x for x in iterable if condition(x))
    except StopIteration:
        return None


def getProjRepoName(arg):
    id_, name, projNum, *_ = arg
    eng = re.sub("[\u4e00-\u9fa5]", "", name)
    eng = "".join([word.title() for word in eng.split()])
    return f"{eng}{id_}-p{projNum}"


def passCodeQuality(path, language):
    if language == "matlab":
        with open(path, encoding="utf-8", errors="replace") as f:
            res = f.read()
        return "global " not in res
    if language in ["c", "llvm-c"]:
        res = subprocess.check_output(
            ["ctags", "-R", "-x", "--sort=yes", "--c-kinds=v", path]
        )
        lines = res.splitlines()
        return len([line for line in lines if b"const" not in line]) == 0
    if language in ["cc", "llvm-cc"]:
        res = subprocess.check_output(
            ["ctags", "-R", "-x", "--sort=yes", "--c++-kinds=v", path]
        )
        lines = res.splitlines()
        return len([line for line in lines if b"const" not in line]) == 0


def getAllFiles(root):
    for f in os.listdir(root):
        if os.path.isfile(os.path.join(root, f)):
            yield os.path.join(f)
    dirs = [
        d
        for d in os.listdir(root)
        if os.path.isdir(os.path.join(root, d)) and d != ".git"
    ]
    for d in dirs:
        dirfiles = getAllFiles(os.path.join(root, d))
        for f in dirfiles:
            yield os.path.join(d, f)

def loadJson(fp):
    with open(fp) as f:
        obj = json.load(f)
        f.close()
        return obj

def dumpJson(obj, fp):
    """Dump object `obj` to filepath `fp`."""
    with open(fp, "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.close()

def mergeDicts(*dicts) -> dict:
    """Merge values under the same key from multiple dict-valued dicts into one dict.

    Typically the keys will be student names. Example:

    mergeDicts(
        {"alice": {"indvComment": []}, "bob": {}},
        {"alice": {"groupComment": []}},
    )

    will return

    {"alice": {"indvComment": [], "groupComment": []}, "bob": {}}
    """
    res = {}
    for key in dicts[0].keys():
        res[key] = {}
        for d in dicts:
            res[key].update(d.get(key, {}))
    return res
