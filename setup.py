import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("CHANGELOG.md", "r", encoding="utf-8") as fh:
    change_log = fh.read()

setuptools.setup(
    name="opensim-WillFreitag",
    version="1.1.1",
    author="Will Freitag",
    author_email="Wilhelm.Freitag@omp.de",
    description="OpenSim is a lightweight tool to send test data "
                "to an Orion Context Broker or FROST-Server respectively.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HYPERTEGRITY-AG/OpenSim",
    project_urls={
        "Bug Tracker": "https://github.com/HYPERTEGRITY-AG/OpenSim/projects/1",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)