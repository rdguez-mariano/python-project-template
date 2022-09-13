#!/usr/bin/env python
import os
import shutil
import subprocess

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)
AI_LIGHTNING_REPO_DIR = "lightning_src"
GITHUB_ACTIONS_WORKFLOWS_DIR = ".github/workflows"
SPHINX_DOCS_DIR = "docs"


def remove_filepath(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
    except:
        print(f"failed to remove {path}")
        pass


def move_folder(src_path, dst_path):
    shutil.copytree(
        src_path,
        dst_path,
        dirs_exist_ok=True,
    )
    remove_filepath(src_path)


def execute(*args, ignore_exception=False, cwd=None):
    cur_dir = os.getcwd()

    try:
        if cwd:
            os.chdir(cwd)

        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out, err = proc.communicate()
        out = out.decode("utf-8")
        err = err.decode("utf-8")
        if err and not ignore_exception:
            raise Exception(err)
        else:
            return out
    finally:
        os.chdir(cur_dir)


def init_git():
    if not os.path.exists(os.path.join(PROJECT_DIRECTORY, ".git")):
        execute("git", "init", ignore_exception=True, cwd=PROJECT_DIRECTORY)
        execute(
            "git",
            "checkout",
            "-b",
            "main",
            ignore_exception=True,
            cwd=PROJECT_DIRECTORY,
        )


def poetry_install():
    execute("poetry", "install", cwd=PROJECT_DIRECTORY)


def init_commit():
    execute("git", "add", "--all", cwd=PROJECT_DIRECTORY)
    execute("git", "commit", "-m", "feat: initial commit", cwd=PROJECT_DIRECTORY)


def install_pre_commit_hooks():
    execute("poetry", "run", "pre-commit", "install", cwd=PROJECT_DIRECTORY)


if __name__ == "__main__":
    enable_github_actions_ci = "{{cookiecutter.enable_github_action_ci}}" == "y"
    enable_sphinx_docs = "{{cookiecutter.enable_sphinx_docs}}" == "y"
    enable_lightning_repo = "{{cookiecutter.enable_lightning_repo}}" == "y"

    try:
        if enable_lightning_repo:
            move_folder(
                os.path.join(AI_LIGHTNING_REPO_DIR,"vscode"),
                ".vscode",
            )
            move_folder(
                os.path.join(AI_LIGHTNING_REPO_DIR,"gin-files"),
                "gin-files",
            )
            move_folder(
                AI_LIGHTNING_REPO_DIR,
                os.path.join("src","{{cookiecutter.pkg_shelf}}","{{cookiecutter.pkg_name}}"),
            )
        else:
            remove_filepath(AI_LIGHTNING_REPO_DIR)

        if not enable_github_actions_ci:
            remove_filepath(GITHUB_ACTIONS_WORKFLOWS_DIR)

        if not enable_sphinx_docs:
            remove_filepath(SPHINX_DOCS_DIR)

        init_git()
        poetry_install()
        init_commit()
        install_pre_commit_hooks()
    except Exception as e:
        print(str(e))
        print(
            "Post-generation script failed, you may need to init version control, install the package and setup pre-commit hooks by yourself"
        )
