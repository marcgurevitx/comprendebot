from setuptools import setup

setup(
    name="manage",
    packages=["manage"],
    entry_points={
        "console_scripts": [
            "botaddphrases = manage.botaddphrases:botaddphrases",
        ],
    },
)
