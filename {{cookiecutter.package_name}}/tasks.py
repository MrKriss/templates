from invoke import task


@task
def lint(c):
    """Run all static code checks."""

    c.run("flake8 --config ./package/setup.cfg ./package")
    c.run("black --check ./package")
    c.run("bandit -rq ./package/{{cookiecutter.package_name}}/")


@task
def install(c):
    """Install package fully to python library."""

    with c.cd("./package"):
        c.run("python setup.py install", echo=True, hide="out")


@task
def test(c):
    """Run pytest test suite."""

    c.run("pytest ./package -q")


@task(pre=[lint, install, test])
def ci(c):
    pass
