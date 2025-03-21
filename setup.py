from setuptools import setup, find_packages

setup(
    name="wizards_of_x",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "tweepy==4.14.0",
        "mysql-connector-python==8.0.33",
        "paramiko==3.4.0",
        "prometheus-client==0.19.0",
        "python-json-logger==2.0.7",
    ],
    extras_require={
        "elizaos": ["elizaos==14.8.0"],
    },
    python_requires=">=3.8",
) 