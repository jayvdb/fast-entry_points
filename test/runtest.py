#!/usr/bin/env python3
import difflib
import os
#import pathlib
import shutil
import subprocess
import sys
try:
    import pathlib2 as pathlib
except:
    import pathlib

TEST_DIR = pathlib.Path(__file__).absolute().parent
PROJECT_DIR = TEST_DIR.parent
EXPECTED_OUTPUT = r"""# -*- coding: utf-8 -*-
# EASY-INSTALL-ENTRY-SCRIPT: 'dummypkg==0.0.0','console_scripts','hello'
__requires__ = 'dummypkg==0.0.0'
import re
import sys

from dummy import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())"""

if sys.version_info[0] == 2:
    use_virtualenv = True
# Python 2 needs virtualenv, and Travis already executes in a virtualenv
use_virtualenv = True

if False:
    EXPECTED_OUTPUT = '\n'.join(
        [line for line in EXPECTED_OUTPUT.splitlines()
         if not line.startswith('# EASY-INSTALL-ENTRY-SCRIPT')
         and not line.startswith('__requires__')]
    )


def run(*args, **kwargs):
    if sys.version_info[0] == 3:
        subprocess.run(*args, check=True, **kwargs)
    else:
        subprocess.call(*args, **kwargs)


def main():
    fep_copy = TEST_DIR / "fastentrypoints.py"
    shutil.copy2(str(PROJECT_DIR/"fastentrypoints.py"), str(fep_copy))

    testenv = pathlib.Path("testenv")
    testpython = testenv / "bin" / ("python" + str(sys.version_info[0]))
    pip = testenv / "bin" / "pip"
    if use_virtualenv:
        run([sys.executable, "-m", "virtualenv", str(testenv)])
    else:
        run([sys.executable, "-m", "venv", str(testenv)])

    run([str(pip), "install", "-e", str(TEST_DIR)])

    try:
        with open(str(testenv / "bin" / "hello")) as output:
            #output.readline()  # eat shabang line, which is non-deterministic.
            result = output.read().strip()
            assert result == EXPECTED_OUTPUT, result + str(list(difflib.unified_diff(EXPECTED_OUTPUT.splitlines(), result.splitlines())))
    finally:
        shutil.rmtree(str(testenv))
        os.remove(str(fep_copy))


if __name__ == '__main__':
    main()
