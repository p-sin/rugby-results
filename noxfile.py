import nox

# options
nox.options.sessions = (
    "pytest",
    "mypy",
    "ruff",
    "black",
    "isort",
    "coverage",
    "safety",
    "checkov",
)
nox.options.reuse_existing_virtualenvs = True
SILENT_DEFAULT = True
SILENT_CODE_MODIFIERS = False
RUNNER = "poetry"

# targets
PACKAGE_LOCATION = "."


@nox.session(python="3.12", tags=["lint"])
def ruff(session: nox.Session) -> None:
    """Lint with ruff."""
    _install(session)
    _run(session, "ruff", "check", PACKAGE_LOCATION)


@nox.session(python="3.12", tags=["format"])
def black(session: nox.Session) -> None:
    """Reformat with black."""
    _install(session)
    _run_code_modifier(session, "black", PACKAGE_LOCATION)


@nox.session(python="3.12", tags=["format"])
def isort(session: nox.Session) -> None:
    """Sort imports with isort."""
    _install(session)
    _run_code_modifier(session, "isort", PACKAGE_LOCATION)


@nox.session(python="3.12", tags=["test"])
def pytest(session: nox.Session) -> None:
    """Run the test suite with pytest."""
    args = session.posargs or ("--cov", "-m", "not e2e")
    _install(session)
    _run(session, "pytest", *args)


@nox.session(python="3.12", tags=["ci"])
def coverage(session: nox.Session) -> None:
    """Upload coverage data."""
    args = session.posargs or [
        "--cov",
        "-m",
        "not e2e",
        "--cov-report=xml",
        "--cov-fail-under=0",
    ]
    _install(session)
    _run(session, "pytest", *args)


@nox.session(python="3.12", tags=["typecheck"])
def mypy(session: nox.Session) -> None:
    """Verify types using mypy (so it is static)."""
    _install(session)
    _run(session, "mypy", PACKAGE_LOCATION)


@nox.session(python="3.12", tags=["security"])
def safety(session: nox.Session) -> None:
    """Check dependencies for vulnerabilities."""
    _install(session)
    _run(session, "safety", "check")


@nox.session(python="3.12", tags=["security"])
def checkov(session: nox.Session) -> None:
    """Run Checkov to scan infrastructure as code (IaC)."""
    _install(session)
    _run(session, "checkov", "--directory", PACKAGE_LOCATION)


@nox.session(python="3.12", tags=["security"])
def trufflehog(session: nox.Session) -> None:
    """Scan repository for secrets."""
    _install(session)
    _run(session, "trufflehog", "--regex", "--entropy=True", PACKAGE_LOCATION)


def _install(session: nox.Session, *args: str) -> None:
    session.run(RUNNER, "install", *args, external=True, silent=SILENT_DEFAULT)


def _run(
    session: nox.Session,
    target: str,
    *args: str,
    silent: bool = SILENT_DEFAULT,
) -> None:
    session.run(RUNNER, "run", target, *args, external=True, silent=silent)


def _run_code_modifier(session: nox.Session, target: str, *args: str) -> None:
    _run(session, target, *args, silent=SILENT_CODE_MODIFIERS)
