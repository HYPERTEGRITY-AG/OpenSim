import os

from setuptools import find_packages, setup

folder = os.path.dirname(os.path.realpath(__file__))
requirementPath = folder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("CHANGELOG.md", "r", encoding="utf-8") as fh:
    change_log = fh.read()

setup(
    name="oscsim-WillFreitag",
    version="1.1.1",
    author="Will Freitag",
    author_email="Wilhelm.Freitag@omp.de",
    description="Open Smart City-Sim is a lightweight tool to send test data "
                "to an Orion Context Broker or FROST-Server respectively.",
    license='MIT License',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HYPERTEGRITY-AG/OpenSim",
    project_urls={
        "Bug Tracker": "https://github.com/HYPERTEGRITY-AG/OpenSim/projects/1",
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    entry_points={'console_scripts': ['oscsim = oscsim.run:main']},
    python_requires='>=3.6',
    install_requires=install_requires
)
