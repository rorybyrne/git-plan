default:
    @just --list

tox:
    @tox

test:
    @pytest -s

pylint:
    rye run pylint git_plan

flake8:
    rye run flake8 git_plan

pyright:
    rye run pyright git_plan

lint:
    just pylint
    just flake8
    just pyright


lint-safe:
    - just pylint
    - just flake8
    - just pyright

