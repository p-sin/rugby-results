# py-template

Python repository template

1. Install python (interpreter) and poetry (dependency manager)
    - Python: <https://www.python.org/downloads/>
    - Poetry: <https://python-poetry.org/docs/>

2. VS code settings
    - Auto save on focus change
    - Black linting

3. Extensions
    - autopep8
    - Black Formatter
    - isort
    - Mypy
    - Pylance
    - Pylint
    - Python
    - Ruff

    - Even Better TOML
    - markdownlint
    - Jupyter
    - rainbow csv
    - parquet viewer
    - SQLite viewer

    - GitHub Pull Requests
    - GitLens - Git supercharged
    - GitHub Actions

    - autoDocstring
    - Error Lens
    - GitHub CoPilot

4. Set up python version (if needed)
    - <https://github.com/pyenv/pyenv>
    - pyenv install [version number]
    - pyenv local [version number]
    - poetry install
    - poetry env use [version]

5. Poetry (dependency manager)
    - Create empty project folder
    - ```poetry new [project-name]``` or ```poetry init``` for existing project
    - Add depdendencies: ```poetry add```
    - Remove dependencies: ```poetry remove```
    - Use ```poetry install``` to make/update virutal environment from poetry config
    - If does not create new virtual env, is because it is in one. Set to base python in select interpreter, then install again

    - poetry.dependencies:
        - python
        - safety
        - checkov
        - mypy

    - dev-dependencies:
        - nox
        - pre-commit
        - black
        - isort
        - ruff
        - mypy
        - typing-extensions
        - pandas-stubs
        - pytest
        - pytest-cov
        - pytest-mock
        - coverage

6. Set up git repo
    - Create repo on github
    - Create local folder
    - ```git init```
    - ```git remote add origin [url]```
    - Add/Configure .gitignore

7. Dev tools
    - Added as dependencies in pyproject.toml with Config added in pyproject.toml or separate files
    - Called by pre-commit, github workflow and nox
    - Tools:

        - Black (configured through ruff)
        - Ruff (configured in pyproject.toml)
        - Mypy (configured in pyproject.toml and .github/linters/.mypy.ini)
        - isort
        - coverage (configured in .coveragerc)
        - pre-commit (configured in pre-commit-config.yaml then run ```pre-commit install```)
        - Nox (configured in noxfile.py), includes:
            - ruff
            - black
            - isort
            - pytest
            - coverage
            - mypy
            - safety
            - checkov
            - trufflehog
        - pytest (configured in pyproject.toml)

8. GitHub workflows
    - Configured in .github/workflows

Look at running deployment/infra workflows in separate repo
Limit to running on certain file changes

1. get secrets
2. set up linters
3. set up tests
4. run linters and tests
5. alerts

Draft releases and deploy into test

    Basic CI/CD: Set up a simple workflow to run Python tests

    Data Pipeline Automation: Schedule data processing tasks

    Environment Management: Handle secrets and credentials safely

    Reusable Workflows: Create shared components (addresses the cost issue mentioned above)

    Notifications & Monitoring: Set up Slack alerts for pipeline status

9. Useful libraries
    - Pydantic (model validation)
