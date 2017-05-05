from distutils.core import setup
import py2exe

setup(name="liftr",
      version="0.1",
      author="Ryan Paul",
      author_email="segphault@arstechnica.com",
      url="https://launchpad.net/liftr",
      license="GNU General Public License (GPL)",
      packages=['liftr'],
      package_data={"liftr": ["ui/*"]},
      scripts=["bin/liftr"],
      windows=[{"script": "bin/liftr"}],
      options={"py2exe": {"skip_archive": True, "includes": ["sip"]}})