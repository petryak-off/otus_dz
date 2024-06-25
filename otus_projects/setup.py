from setuptools import find_packages, setup

setup(
    name="otus_projects",
    packages=find_packages(exclude=["otus_projects_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
