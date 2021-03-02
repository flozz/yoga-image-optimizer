import nox


@nox.session
def lint(session):
    session.install("flake8")
    session.run("flake8", "yoga_image_optimizer", "noxfile.py")


@nox.session(python=["3.6", "3.7", "3.8", "3.9"])
def test(session):
    session.install("pytest")
    session.install(".")
    session.run("pytest", "--doctest-modules", "yoga_image_optimizer")
