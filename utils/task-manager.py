# experimental short script for manage competitive programing tasks
import json
import sys
import pathlib
from jinja2 import Template
import utils
import os
import configparser
import re
from requests import get

EDITOR = "subl {{ filename }} "
TASK_DIR = pathlib.Path("src") / "tasks"
UTILS_DIR = pathlib.Path(".")
BOOK_DIR = pathlib.Path("src")


def execute(**args):
    utils.shell_command(Template(args["command"]).render(args))


def text_or_none(path: pathlib.Path):
    try:
        return path.read_text()
    except:
        return None


def get_cfg(task: pathlib.Path):
    cfg = configparser.ConfigParser(allow_no_value=True)
    cfg.read(task / "cfg.txt")
    return cfg


def get_examples(task: pathlib.Path):
    files = list(task.glob("example*.in"))
    res = []
    for file in files:
        filename = str(file.name)
        m = re.search("example(.+?).in", filename)
        if m:
            number = int(m.group(1))
            if not (task / f"example{number}.out").exists():
                raise Exception(f"example{number}.out nonexistent for task = {task}")
            res.append(number)
    res.sort()
    return res


def read_task(task: pathlib.Path, cnt_examples=100, tutorial=False):
    res = {
        "statement": text_or_none(task / "statement.md"),
        "examples": [],
        "path": task,
        "tutorial": text_or_none(task / "tutorial.md"),
        "cfg": get_cfg(task),
    }
    if cnt_examples > 0:
        examples = get_examples(task)
        examples = examples[: min(cnt_examples, len(examples))]
        for i, number in enumerate(examples):
            res["examples"].append(
                (
                    (task / f"example{number}.in").read_text(),
                    (task / f"example{number}.out").read_text(),
                    text_or_none(task / f"example{number}.note"),
                )
            )
    return res


def get_text(data):
    template = r"""# {{data['cfg']['info']['name'] }}
{{ href }}

## Условие 
{{data['statement'] }}

{% if data['examples']|length > 0 %}
### Примеры

| входные данные   |   выходные данные |
|----------|-------------|{% for test in data['examples'] %}
| {{ test[0]|replace("\n","<br>") }} | {{ test[1]|replace("\n","<br>") }} | {% endfor %}
{% endif %}

## Решение

~~~admonish collapsible=true title="Решение"
{{data['tutorial'] }}
~~~
"""
    href = data["cfg"]["info"]["source"]
    if "source_alpha" in data["cfg"]["info"]:
        alpha = data["cfg"]["info"]["source_alpha"]
        href = f"[Условие задачи {alpha}]({href})"
    else:
        href = f"[Условие задачи]({href})"
    return Template(template).render(data=data, href=href)


def build(dir, cnt_examples=100):
    data = read_task(dir, cnt_examples=cnt_examples)
    text = get_text(data)
    (TASK_DIR / (dir.name + ".md")).write_text(text)


def delete(dir):
    try:
        os.remove(TASK_DIR / (dir.name + ".md"))
    except:
        pass


def get_rating(task: pathlib.Path):
    cfg = get_cfg(task)["info"]
    if "rating" in cfg:
        return int(cfg["rating"])
    if "auto_rating" in cfg:
        return int(cfg["auto_rating"])
    return None


def get_tasks():
    tasks = []
    for f in TASK_DIR.iterdir():
        if f.is_dir():
            tasks.append(f)
    return tasks


def get_sorted_tasks():
    tasks = get_tasks()
    tasks.sort(key=lambda x: get_rating(x))
    return tasks


def download_problemset():
    url = "https://codeforces.com/api/problemset.problems"
    data = {}
    for problem in get(url).json()["result"]["problems"]:
        data[str(problem["contestId"]) + "/" + problem["index"]] = problem
    (UTILS_DIR / "problemset").write_text(json.dumps(data))


def codeforces_rating(task: pathlib.Path, data):
    cfg = get_cfg(task)
    source = cfg["info"]["source"]
    if source.strip("https://").startswith("codeforces"):
        if "problemset/problem/" in source:
            print(task, "[problemset]")
            exit(-1)
    m = re.search("/contest/(.+?)/problem/(.+?)", source)
    if m:
        number = int(m.group(1))
        alpha = m.group(2)
        return data[str(number) + "/" + alpha]["rating"]
    return None


def auto_rating():
    data = json.loads((UTILS_DIR / "problemset").read_text())
    for task in get_tasks():
        cfg = get_cfg(task)
        raring = codeforces_rating(task, data)
        if raring is not None:
            cfg["info"]["auto_rating"] = str(raring)
            print(task, raring)
            with open(task / "cfg.txt", "w") as f:
                cfg.write(f)


def create_new_task_(dir_name, task_name, source, cnt_examples):
    task = TASK_DIR / dir_name
    if task.exists():
        return Exception("task with this name already exists")
    task.mkdir()
    (task / "statement.md").write_text("")
    (task / "tutorial.md").write_text("")
    (task / "cfg.txt").write_text(f"[info]\nname = {task_name}\nsource = {source}\n")
    for i in range(cnt_examples):
        (task / f"example{i + 1}.in").write_text("")
        (task / f"example{i + 1}.out").write_text("")
    execute(command=EDITOR, filename=task / "statement.md")
    execute(command=EDITOR, filename=task / "tutorial.md")


def create_new_task():
    dir_name = input("dir name = ")
    task_name = input("task name = ")
    source = input(
        "source of this task (link to codeforces.com or some text [otherwise type enter]) = "
    )
    cnt_examples = input("number of examples [otherwise type enter] = ")
    if len(cnt_examples) == 0:
        cnt_examples = 0
    else:
        cnt_examples = int(cnt_examples)
    create_new_task_(dir_name, task_name, source, cnt_examples)


def task_info():
    err = False
    for task in get_tasks():
        if get_rating(task) is None:
            err = True
            print(
                task,
                "does not have a rating, run auto-rating (r) or add a rating in config",
            )
    if err:
        exit(-1)
    print("rating of all tasks correct")


def tasks_summary():
    book_summary = (BOOK_DIR / "SUMMARY.md").read_text().split("\n")
    start = book_summary.index("- [Решаем задачи](./tasks/README.MD)") + 1
    end = start
    while end < len(book_summary) and book_summary[end].startswith("\t"):
        end += 1
    book_summary = book_summary[start:end]
    tasks_summary = set()
    for line in book_summary:
        m = re.search("\(.+\)", line)
        assert m
        tasks_summary.add(m.group(0)[len("./tasks/") + 1 : -4])
    for task in get_sorted_tasks():
        data = get_cfg(task)["info"]
        if "todo" in data:
            print("[todo]", task)
    for task in get_sorted_tasks():
        data = get_cfg(task)["info"]
        if "todo" in data:
            continue
        if task.name not in tasks_summary:
            print(f"- [{data['name'].title()}](./{pathlib.Path(*task.parts[1:])}.md)")


if __name__ == "__main__":
    argv = sys.argv[1:]
    if len(argv) == 0:
        # download_problemset()
        tasks = get_tasks()
        for task in tasks:
            build(task)
    elif argv == ["d"]:
        tasks = get_tasks()
        for task in tasks:
            delete(task)
    elif argv[0] == "c":
        create_new_task()
    elif argv[0] == "i":
        task_info()
    elif argv[0] == "r":
        auto_rating()
    elif argv[0] == "s":
        tasks_summary()
    else:
        print("invalid option")
        exit(-1)
