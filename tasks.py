# pylint: disable=missing-function-docstring, missing-module-docstring, unused-argument
import pathlib
import subprocess
from importlib.metadata import version

from invoke import Context, task

from src.reportmodifier import ReportModifier

ROOT = pathlib.Path(__file__).parent.resolve().as_posix()


@task
def utests(context: Context) -> None:
    cmd = [
        "pytest",
        "--cov-report=term",
        "--cov-report=xml",  # use plugin coverage gutter to get shown the coverage in vscode directly
        "--cov=./src",
        "-v",
        f"{ROOT}/tests/utests",
    ]
    subprocess.run(" ".join(cmd), shell=True, check=False)


@task
def atests(context: Context) -> None:
    cmd = [
        "coverage",
        "run",
        "-m",
        "robot",
        f"--argumentfile={ROOT}/tests/rf_cli.args",
        f"--variable=root:{ROOT}",
        f"--outputdir={ROOT}/results",
        "--loglevel=TRACE:DEBUG",
        f"{ROOT}/tests/atests",
    ]
    subprocess.run(" ".join(cmd), shell=True, check=False)


@task(utests, atests)
def tests(context: Context) -> None:
    subprocess.run("coverage combine", shell=True, check=False)
    subprocess.run("coverage report", shell=True, check=False)
    subprocess.run("coverage html", shell=True, check=False)


@task
def typecheck(context: Context) -> None:
    subprocess.run(f"mypy {ROOT}/src", shell=True, check=False)
    subprocess.run(f"pyright {ROOT}/src", shell=True, check=False)


@task
def lint(context: Context) -> None:
    subprocess.run(f"ruff check {ROOT}", shell=True, check=False)
    # subprocess.run(f"pylint {ROOT}", shell=True, check=False)
    subprocess.run(f"robocop {ROOT}/tests/atests", shell=True, check=False)


@task
def formatcode(context: Context) -> None:
    subprocess.run(f"ruff check --fix {ROOT}", shell=True, check=False)
    subprocess.run(f"ruff format {ROOT}", shell=True, check=False)
    subprocess.run(f"robotidy {ROOT}/tests/atests", shell=True, check=False)


@task
def libdoc(context: Context) -> None:
    json_file = f"{ROOT}/src/reportmodifier/ReportModifier.py"
    source = f"ReportModifier::{json_file}"
    target = f"{ROOT}/docs/ReportModifier.html"
    current_version = version("robotframework-reportmodifier")
    cmd = [
        "python",
        "-m",
        "robot.libdoc",
        f"-v {current_version}",
        source,
        target,
    ]
    subprocess.run(" ".join(cmd), shell=True, check=False)


@task
def libspec(context: Context) -> None:
    json_file = f"{ROOT}/src/reportmodifier/ReportModifierVisitor.py"
    source = f"ReportModifierVisitor::{json_file}"
    target = f"{ROOT}/docs/ReportModifierVisitor.html"
    cmd = [
        "python",
        "-m",
        "robot.libdoc",
        f"-v {VERSION}",
        source,
        target,
    ]
    subprocess.run(" ".join(cmd), shell=True, check=False)


@task
def listenerlibdoc(context: Context) -> None:
    json_file = f"{ROOT}/src/ReportModifierListener/ReportModifierListener.py"
    source = f"ReportModifierListener::{json_file}"
    target = f"{ROOT}/docs/ReportModifierListener.html"
    cmd = [
        "python",
        "-m",
        "robot.libdoc",
        f"-v {VERSION}",
        source,
        target,
    ]
    subprocess.run(" ".join(cmd), shell=True, check=False)


@task
def readme(context: Context) -> None:
    front_matter = """---\n---\n"""
    with open(f"{ROOT}/docs/README.md", "w", encoding="utf-8") as readme_file:
        doc_string = ReportModifier.__doc__
        readme_file.write(front_matter)
        readme_file.write(str(doc_string).replace("\\", "\\\\").replace("\\\\*", "\\*"))


@task(formatcode, utests, readme)
def build(context: Context) -> None:
    subprocess.run("poetry build", shell=False, check=False)


@task(build)
def install(context: Context) -> None:
    subprocess.run("poetry install", shell=False, check=False)


@task(install, libdoc, libspec, listenerlibdoc, readme)
def publish(context: Context) -> None:
    subprocess.run("poetry publish -r nexus-snapshot", shell=False, check=False)
