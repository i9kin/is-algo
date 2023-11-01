import git
import pathlib
import shutil
import subprocess
import json

try:
    with open("secrets.json", "r") as f:
        config_json = json.load(f)
        USER = config_json["USER"]
        REPO = config_json["REPO"]
        GH_PASSWORD = config_json["GH_PASSWORD"]
except:
    print("error while reading secrets.json")
    exit(0)


URL = f"https://{USER}:{GH_PASSWORD}@github.com/{USER}/{REPO}"


def download():
    if not pathlib.Path(REPO).exists():
        git.Git(".").clone(URL)
        return

    repo = git.Repo(REPO)
    git.Repo(REPO).git.checkout("master")
    repo.remotes.origin.pull()


def rm_tree(pth: pathlib.Path):
    for child in pth.iterdir():
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()


def safe_rm(path):
    if path.exists():
        rm_tree(path)


def build():
    copy_dir = pathlib.Path(REPO + "_copy")
    sha = git.Repo(REPO).head.object.hexsha
    safe_rm(copy_dir)
    shutil.copytree(pathlib.Path(REPO), copy_dir, dirs_exist_ok=True, exist_ok=False)
    subprocess.Popen(["python3", "utils/task-manager.py"], cwd=copy_dir).wait()
    subprocess.Popen(["mdbook", "build"], cwd=copy_dir).wait()
    rm_tree(copy_dir / ".git")
    git.Repo(REPO).git.checkout("gh-pages")
    shutil.copytree(copy_dir / "book", pathlib.Path(REPO), dirs_exist_ok=True)
    git.Repo(REPO).git.add(all=True)
    git.Repo(REPO).git.commit(
        "-m", "deploy: " + sha
    )  # , author='deploy <deploy@deploy.com>'
    git.Repo(REPO).git.push("origin", "gh-pages")


safe_rm(pathlib.Path(REPO))
download()
build()
