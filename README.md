# ENGR151 Grader

VG101-Grade-Helper, reformatted, several bugs fixed.

Other changes and notes:

- Directly running with `-au` (check all, upload to canvas immediately) is
  _not_ recommended given how unstable JOJ is. Instead, run first with
  `-s` (export score to `output/scores.json`) and _without_ `-u`.
- JOJ is now single-processed. Expect turtle speed for matlab.
- Upload grades from `output/scores.json` to canvas by running with
  `-u` and without any of `-a, -i, -g, -j, -t`.

## Dependencies

- Python 3
- Everything in `requirements.txt`
- ctags if grading C/C++

## Preparation for homework grading

1. Obtain OAuth2 tokens from canvas and gitea.
2. Obtain session ID from JOJ cookies.
3. Obtain homework ID and problem IDs from JOJ URLs.
4. Obtain number of test cases for each exercise from JOJ scoreboard.
5. Copy `settings.example.py` to `settings.py`.
6. Fill in `CANVAS_TOKEN`, `GITEA_TOKEN`, `JOJ_INFO`, `MANDATORY_FILES` and `OPTIONAL_FILES`.

## Usage

```bash
$ python main.py -h HW_NUM -i -g -j -s
$ less output/scores.json # gut check grading before releasing
$ python main.py -h HW_NUM -u
```

Legacy documentation by Boming attached below.

# VG101-Grade-Helper

A script that perform cast-to-cast VG101 grading for UMJI VG101FA2020-1.

It helps you begin from clone repo from Gitea to giving grade to canvas with comment of rubric.

## Installation & Usage

First install [ctags](https://github.com/universal-ctags/ctags) for C code quality checking.

```bash
$ pip3 install -r requirement.txt
$ mv hgroups.example.json hgroups.json
$ vim hgroups.json
$ mv settings.example.py settings.py
$ vim settings.py
$ ./VG101GradeHelper.py --help
usage: VG101GradeHelper.py [--help] [-h HW] [-p PROJ] [-f FEEDBACK] [-m MS] [-r REJUDGE] [-a] [-s] [-t] [-d] [-i] [-g] [-j] [-u]

optional arguments:
  --help                show this help message and exit
  -h HW, --hw HW        # homework
  -p PROJ, --proj PROJ  # project
  -f FEEDBACK, --feedback FEEDBACK
                        give feedback to project
  -m MS, --ms MS        # milestone
  -r REJUDGE, --rejudge REJUDGE
                        rejudge group num or stu ID
  -a, --all             check all
  -s, --score           generate score
  -t, --tidy            check tidy
  -d, --dir             create dir for individual submission
  -i, --indv            check individual submission
  -g, --group           check group submission
  -j, --joj             check joj score
  -u, --upload          upload score to canvas
```

Please modify `JOJ_INFO` for different homework.

### Example

#### For homework

```bash
./VG101GradeHelper.py -h1 -au
```

#### For project

```bash
./VG101GradeHelper.py -p1 -m1
```

## Features

- [x] At least two days before the group deadline, all students should individually complete all the mandatory tasks and push their work to their personal branch of their group git repository and issue a pull request. Students late for the individual submission must open an issue featuring: (i) apologies to the reviewer, (ii) clear explanations on why the work is late, and (iii) a request for a new deadline fitting the reviewer. The reviewer is allowed to reject the request and should set the deadline based on his/her own schedule. **(-0.5 mark)**
- [x] A student should provide feedbacks to at least one teammate for each mandatory exercise. Low quality reviews will be ignored. Each student should receive feedbacks on his individual submission. e.g. for a three students group: student1 → student2 → student3 → student1. **(-1 mark)**
- [x] The final group submission, done on the master branch of the group repository, should successfully compile or be interpreted. **(-1 mark)**
- [x] Any group submission that is more than 24 hours late will be rejected. **(-2.5 marks)**
- [x] For each exercise, the final submission must pass at least 25% of the test cases. **(-0.25 mark per exercise, up to -0.5)**
- [x] For a homework the final submission must pass at least 50% of all the test cases. **(-0.5 mark)**
- [x] Using global variable, breaking the rule in code_quality.pdf. **(-0.5 mark)**

## Tips:

You need set a default grade for assignments on canvas before running the script, otherwise you can not get their submissions and edit scores.
