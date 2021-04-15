import pathlib

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
    session.run("black", "--check", "--diff", "--color", *PYTHON_FILES)


@nox.session(reuse_venv=True)
def black_fix(session):
    session.install("black")
    session.run("black", *PYTHON_FILES)


# NOTE All Gtk dependencies and introspection files must be installed for this
# to work.
@nox.session(python=["3.7", "3.8", "3.9"], reuse_venv=True)
def test(session):
    session.install("pytest")
    session.install("-e", ".")
    session.run(
        "pytest",
        "--doctest-modules",
        "yoga_image_optimizer",
        env={"LANG": "C"},  # Force using the default strings
    )


@nox.session
def locales_update(session):
    # Extract messages in .pot
    session.run(
        "xgettext",
        "--from-code=UTF-8",
        "-o",
        "locales/messages.pot",
        "yoga_image_optimizer/data/ui/main-window.glade",
        *[
            p.as_posix()
            for p in pathlib.Path("yoga_image_optimizer/").glob("**/*.py")
        ],
        external=True,
    )
    # Updates locales
    for po_file in pathlib.Path("locales").glob("*.po"):
        session.run(
            "msgmerge",
            "--update",
            "--no-fuzzy-matching",
            po_file.as_posix(),
            "locales/messages.pot",
            external=True,
        )


@nox.session
def locales_compile(session):
    LOCAL_DIR = pathlib.Path("yoga_image_optimizer/data/locales")
    for po_file in pathlib.Path("locales").glob("*.po"):
        output_file = (
            LOCAL_DIR
            / po_file.name[: -len(po_file.suffix)]
            / "LC_MESSAGES"
            / "org.flozz.yoga-image-optimizer.mo"
        )
        print(output_file.as_posix())
        output_file.parent.mkdir(parents=True, exist_ok=True)
        session.run(
            "msgfmt",
            po_file.as_posix(),
            "-o",
            output_file.as_posix(),
            external=True,
        )
