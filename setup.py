from setuptools import setup

from setuptools import setup
import re

with open('discord/ext/customs/commands/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open("README.md", "r") as f:
	long_desc = f.read()

setup(
  name = 'discord.customs',
  packages = ['discord.ext.customs.commands'],
  version = version,
  license='AGPL',
  url="https://github.com/FrostiiWeeb/",
  long_description=long_desc,
long_description_content_type="text/markdown",        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A small pypi project, that adds more extensions to your discord.py bot.',   # Give a short description about your library
  author = 'Alex Hutz',
  author_email = 'frostiiweeb@gmail.com',
  keywords = ['extensions', 'dpy', 'discord.py', 'discord'],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: AGPL-2.0 License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)
