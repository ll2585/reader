from distutils.core import setup
import py2exe, crammer

setup(console=['main.py'], options={"py2exe": {"includes": ["sip"]}})