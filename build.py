import os
import shutil
import subprocess

import click

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ASSETS_DIR = os.path.join(CURRENT_DIR, "assets")
SRC_DIR = os.path.join(CURRENT_DIR, "src")
BUILD_DIR = os.path.join(CURRENT_DIR, "build")
CONTENTS_DIR = os.path.join(BUILD_DIR, "Contents")
CODE_DIR = os.path.join(CONTENTS_DIR, "Code")
LIBRARIES_DIR = os.path.join(CONTENTS_DIR, "Libraries", "Shared")


@click.command()
def build():
    if not os.path.exists(BUILD_DIR):
        os.makedirs(BUILD_DIR)

    if os.path.exists(CONTENTS_DIR):
        shutil.rmtree(CONTENTS_DIR)

    os.makedirs(CODE_DIR)
    os.makedirs(LIBRARIES_DIR)

    copy_assets()
    copy_source()
    install_libraries()


def copy_assets():
    for filename in os.listdir(ASSETS_DIR):
        shutil.copyfile(
            os.path.join(ASSETS_DIR, filename),
            os.path.join(CONTENTS_DIR, filename),
        )


def copy_source():
    for filename in os.listdir(SRC_DIR):
        src_file = os.path.join(SRC_DIR, filename)
        if os.path.isdir(src_file):
            continue
        if filename.endswith("_test.py"):
            continue
        shutil.copyfile(
            src_file,
            os.path.join(CODE_DIR, filename),
        )


def install_libraries():
    subprocess.check_call(
        ["pip", "install", "--target", LIBRARIES_DIR, "-r", "requirements-build.txt"]
    )


if __name__ == "__main__":
    build()
