#!/usr/bin/env python3
from setuptools import setup

# skill_id=package_name:SkillClass
PLUGIN_ENTRY_POINT = 'skill-epic-horror-theatre.jarbasai=skill_epic_horror_theatre:EpicHorrorTheatreSkill'

setup(
    # this is the package name that goes on pip
    name='ovos-skill-epic-horror-theatre',
    version='0.0.1',
    description='ovos wayne june lovecraft readings skill plugin',
    url='https://github.com/JarbasSkills/skill-public-domain-cartoons',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    package_dir={"skill_epic_horror_theatre": ""},
    package_data={'skill_epic_horror_theatre': ['locale/*', 'res/*', 'ui/*']},
    packages=['skill_epic_horror_theatre'],
    include_package_data=True,
    install_requires=["ovos_workshop~=0.0.5a1"],
    keywords='ovos skill plugin',
    entry_points={'ovos.plugin.skill': PLUGIN_ENTRY_POINT}
)
