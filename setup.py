#
#  This is the pyenchant distutils setup script.
#  Originally developed by Ryan Kelly, 2004.
#
#  This script is placed in the public domain.
#

from distutils.core import setup, Extension
import distutils
import sys
import os

#  Version Information
VER_MAJOR = 1
VER_MINOR = 0
VER_PATCH = 0
VER_SUB = "_rc1"
VERSION = "%d.%d.%d%s" % (VER_MAJOR,VER_MINOR,VER_PATCH,VER_SUB)


# Package MetaData
NAME = "pyenchant"
DESCRIPTION = "Python bindings for the Enchant spellchecking system"
AUTHOR = "Ryan Kelly"
AUTHOR_EMAIL = "ryan@rfk.id.au"
URL = "http://www.rfk.id.au/software/projects/pyenchant"


#  Module Lists
PY_MODULES = []
PACKAGES = ["enchant"]
EXT_MODULES = []
PKG_DATA = {}
DATA_FILES = []
SCRIPTS = []


# Extension Objects

#  The distutils/swig integration doesnt seem to cut it for this module
#  For now, enchant_wrap.c will need to be distributed as well.  At least
#  then people wont *have* to have swig installed.
#  Generate it using `swig -python -noproxy enchant.i` to ensure that
#  proxy class stubs are not generated.
ext1 = Extension('enchant._enchant',['enchant/enchant_wrap.c'],
                 libraries=[],
                 library_dirs=[],
                )
# Include windows-specific build information if appropriate
if sys.platform == "win32":
    ext1.libraries.append("enchant-1")
    SCRIPTS.append("tools/wininst.py")
    # Use local dlls if available
    if os.path.exists(r".\windeps"):
        ext1.library_dirs.append("./windeps/bin")
        LOCAL_DLLS = ["libenchant-1","libglib-2.0-0","iconv","intl",
                      "libenchant_ispell-1","libgmodule-2.0-0"]
        PKG_DATA["enchant"] = []
        for dllName in LOCAL_DLLS:
            PKG_DATA["enchant"].append("./windeps/bin/%s.dll" % (dllName,))
        PKG_DATA["enchant/ispell"] = []
	# Also include local dictionaries
	dictPath = os.path.normpath("./windeps/ispell")
	for dictName in os.listdir(dictPath):
          if dictName.endswith(".hash"):
            PKG_DATA["enchant/ispell"].append(os.path.join(dictPath,dictName))
else:
    ext1.libraries.append("enchant")

EXT_MODULES.append(ext1)

# Try to simulate package_data for older distutils
# Since PKG_DATA is only populated on Windows, we know the path
# to site-packages
distutils_ver = map(int,distutils.__version__.split("."))
if distutils_ver[2] < 4:
    for k in PKG_DATA:
        DATA_FILES.append(("Lib/site-packages/%s"%(k,),PKG_DATA[k]))
    

setup(name=NAME,
      version=VERSION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      packages=PACKAGES,
      py_modules=PY_MODULES,
      ext_modules=EXT_MODULES,
      package_data=PKG_DATA,
      data_files=DATA_FILES,
      scripts=SCRIPTS,
     )

