import nox

PYTHON_VERSION = "3.9"
BLACK_ARGS = ["black", "--extend-exclude", "/tests/model_tests/", "src/", "tests/"]
ISORT_ARGS = ["isort", "src/", "tests/"]

nox.options.sessions = ["dev"]


@nox.session(python=PYTHON_VERSION, reuse_venv=True)
def dev(session):
    session.install("nox")
    session.install("-e", ".[black,flake8,isort,mypy,tests]")
    session.run("pytest", "tests/")


@nox.session(python=PYTHON_VERSION)
def tests(session):
    session.install(".[tests]")
    session.run("pip", "freeze")
    session.run("pytest", "tests/")


@nox.session(python=PYTHON_VERSION)
def clean(session):
    session.install(".[isort,black]")
    session.run("black", "--version")
    session.run("isort", "--vn")
    session.run(*BLACK_ARGS)
    session.run(*ISORT_ARGS)


@nox.session(python=PYTHON_VERSION)
def flake8(session):
    session.install(".[flake8]")
    session.run("pip", "freeze")
    session.run("flake8", "--version")
    session.run("flake8", "src/", "tests/")


@nox.session(python=PYTHON_VERSION)
def black(session):
    session.install(".[black]")
    session.run("pip", "freeze")
    session.run("black", "--version")
    session.run(*BLACK_ARGS, "--check", "--diff")


@nox.session(python=PYTHON_VERSION)
def isort(session):
    session.install(".[isort]")
    session.run("pip", "freeze")
    session.run("isort", "--vn")
    session.run(*ISORT_ARGS, "--diff", "--check-only")


@nox.session(python=PYTHON_VERSION)
def mypy(session):
    session.install(".[mypy]")
    session.run("pip", "freeze")
    session.run("mypy", "--version")
    session.run("mypy", "src/")
