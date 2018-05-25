import subprocess
from invoke import task

@task
def test(ctx):
    ctx.run('python -m unittest discover -v -s .')

@task
def coverage(ctx):
    from unittest import TestLoader, TextTestRunner
    from coverage import Coverage

    cov = coverage.Coverage()
    cov.start()

    suite = unittest.TestLoader().discover("./")
    unittest.TextTestRunner().run(suite)

    cov.stop()
    cov.save()

    covered = cov.report(show_missing=True)
    accepted_coverage = 90

    assert covered > accepted_coverage, "Not enough coverage. Minimum {} percent, current: {:.2f}%".format(
        accepted_coverage, covered)

@task
def freeze(ctx):
    # A bug in Ubuntu is including the 'pkg-resources' package into the freeze,
    # this crash in other OS, including Alpine Linux used to the GoCD Agents.
    # https://stackoverflow.com/questions/39577984/what-is-pkg-resources-0-0-0-in-output-of-pip-freeze-command
    ctx.run('pip freeze | grep -v "pkg-resources" > requirements.txt')

@task
def build(ctx, version):
    pass

@task
def deploy(ctx, app_name, env='dev'):
    pass

@task
def run(ctx):
    ctx.run('python application.py')
