from setuptools import setup

setup(
    name="manage",
    packages=["manage"],
    entry_points={
        "console_scripts": [
            "botaddphrases      = manage.botaddphrases:botaddphrases",
            "botblockperson     = manage.botblockperson:botblockperson",
            "botexportvoice     = manage.botexportvoice:botexportvoice",
            "botsubmissions     = manage.botsubmissions:botsubmissions",
        ],
    },
)
