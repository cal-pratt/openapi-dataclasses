import nox

PYTHON_VERSION = "3.9"
nox.options.sessions = ["dev"]


@nox.session(python=PYTHON_VERSION, reuse_venv=True)
def dev(session):
    session.install("nox")
    session.install("-e", ".[black,flake8,isort,mypy]")


@nox.session(python=PYTHON_VERSION, reuse_venv=True)
def mypy(session):
    session.install(".[mypy]")
    session.run("mypy", "--version")
    session.run("mypy", "src/")


@nox.session(python=PYTHON_VERSION, reuse_venv=True)
def flake8(session):
    session.install(".[flake8]")
    session.run("flake8", "--version")
    session.run("flake8", "src/")


@nox.session(python=PYTHON_VERSION, reuse_venv=True)
def black(session):
    session.install(".[black]")
    session.run("black", "--version")
    session.run("black", "--check", "--diff", "src/")


@nox.session(python=PYTHON_VERSION, reuse_venv=True)
def isort(session):
    session.install(".[isort]")
    session.run("isort", "--vn")
    session.run("isort", "--diff", "--check-only", "src/")


@nox.session(python=PYTHON_VERSION, reuse_venv=True)
def clean(session):
    session.install(".[isort,flake8]")
    session.run("black", "--version")
    session.run("isort", "--vn")
    session.run("black", "src/")
    session.run("isort", "src/")
