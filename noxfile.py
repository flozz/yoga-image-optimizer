import nox


PYTHON_FILES = [
    "yoga_image_optimizer",
    "setup.py",
    "noxfile.py",
]


@nox.session(reuse_venv=True)
def lint(session):
    session.install("flake8", "black")
    session.run("flake8", *PYTHON_FILES)
    session.run("black", "--check", *PYTHON_FILES)


@nox.session(reuse_venv=True)
def black_fix(session):
    session.install("black")
    session.run("black", *PYTHON_FILES)


# NOTE All Gtk dependencies and introspection files must be installed for this
# to work.
@nox.session(python=["3.6", "3.7", "3.8", "3.9"], reuse_venv=True)
def test(session):
    session.install("pytest")
    session.install("-e", ".")
    session.run("pytest", "--doctest-modules", "yoga_image_optimizer")
