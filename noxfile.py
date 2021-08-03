import nox

PYTHON_VERSION = "3.9"
nox.options.sessions = ["dev"]


@nox.session(python=PYTHON_VERSION, reuse_venv=True)
def dev(session):
    session.install("nox")
    session.install("-e", ".[black,flake8,isort,mypy,tests]")
    session.run("pytest", "tests/")


@nox.session(python=PYTHON_VERSION, reuse_venv=True)
def tests(session):
    session.install("nox")
    session.install(".[tests]")
    session.run("pip", "freeze")
    session.run("pytest", "tests/")


@nox.session(python=PYTHON_VERSION, reuse_venv=True)
def clean(session):
    session.install(".[isort,flake8]")
    session.run("black", "--version")
    session.run("isort", "--vn")
    session.run("black", "src/", "tests/")
    session.run("isort", "src/", "tests/")


@nox.session(python=PYTHON_VERSION, reuse_venv=True)
def flake8(session):
    session.install(".[flake8]")
    session.run("pip", "freeze")
    session.run("flake8", "--version")
    session.run("flake8", "src/", "tests/")


@nox.session(python=PYTHON_VERSION, reuse_venv=True)
def black(session):
    session.install(".[black]")
    session.run("pip", "freeze")
    session.run("black", "--version")
    session.run("black", "--check", "--diff", "src/", "tests/")


@nox.session(python=PYTHON_VERSION, reuse_venv=True)
def isort(session):
    session.install(".[isort]")
    session.run("pip", "freeze")
    session.run("isort", "--vn")
    session.run("isort", "--diff", "--check-only", "src/", "tests/")


@nox.session(python=PYTHON_VERSION, reuse_venv=True)
def mypy(session):
    session.install(".[mypy]")
    session.run("pip", "freeze")
    session.run("mypy", "--version")
    session.run("mypy", "src/")
