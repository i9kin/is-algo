# experimental short script for manage competitive programing tasks
import json
import sys
import pathlib
from jinja2 import Template
from os import system
import os
import configparser
import re

EDITOR = "subl {{ filename }} "
TASK_DIR = pathlib.Path("../src/tasks")
UTILS_DIR = pathlib.Path(".")


def execute(**args):
    system(Template(args["command"]).render(args))


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


def read_task(task: pathlib.Path, cnt_examples=0, tutorial=False):
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
{{data['tutorial'] }}"""
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
    os.remove(TASK_DIR / (dir.name + ".md"))


def get_rating(task: pathlib.Path):
    cfg = get_cfg(task)["info"]
    if "rating" in cfg:
        return int(cfg["rating"])
    if "auto_rating" in cfg:
        return int(cfg["auto_rating"])
    return 1


def get_tasks():
    tasks = []
    for f in TASK_DIR.iterdir():
        if f.is_dir():
            tasks.append(f)
    return tasks


def get_tasks_sorted():
    tasks = get_tasks()
    tasks.sort(key=lambda x: get_rating(x))
    return tasks


def download_problemset():
    url = "https://codeforces.com/api/problemset.problems"
    from requests import get

    data = {}
    for problem in get(url).json()["result"]["problems"]:
        data[str(problem["contestId"]) + "/" + problem["index"]] = problem
    (UTILS_DIR / "problemset").write_text(json.dumps(data))


def auto_rating():
    data = json.loads((UTILS_DIR / "problemset").read_text())
    for task in get_tasks():
        cfg = get_cfg(task)
        source = cfg["info"]["source"]
        if source.strip("https://").startswith("codeforces"):
            if "problemset/problem/" in source:
                print(task, "[problemset]")
                continue
            m = re.search("/contest/(.+?)/problem/(.+?)", source)
            if m:
                number = int(m.group(1))
                alpha = m.group(2)
                cfg["info"]["auto_rating"] = str(
                    data[str(number) + "/" + alpha]["rating"]
                )
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


if __name__ == "__main__":
    argv = sys.argv[1:]
    if len(argv) == 0:
        download_problemset()
        tasks = get_tasks()
        for task in tasks:
            build(task)
    elif argv == ["d"]:
        tasks = get_tasks()
        for task in tasks:
            delete(task)
    elif argv[0] == "c":
        create_new_task()
