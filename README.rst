master:

.. image:: https://travis-ci.org/unfoldingWord-dev/obs_tools.svg?branch=master
:alt: Build Status
    :target: https://travis-ci.org/unfoldingWord-dev/obs_tools

.. image:: https://coveralls.io/repos/github/unfoldingWord-dev/obs_tools/badge.svg?branch=master
:alt: Build Status
    :target: https://coveralls.io/github/unfoldingWord-dev/obs_tools

develop:

.. image:: https://travis-ci.org/unfoldingWord-dev/obs_tools.svg?branch=develop
:alt: Build Status
    :target: https://travis-ci.org/unfoldingWord-dev/obs_tools

.. image:: https://coveralls.io/repos/github/unfoldingWord-dev/obs_tools/badge.svg?branch=develop
:alt: Build Status
    :target: https://coveralls.io/github/unfoldingWord-dev/obs_tools

unfoldingWord OBS Tools
=======================

A collection of Python scripts that have proven useful and have been reused.

All code should be compatible with Python 2.7 and 3.5

**To use this library, install it in your Python environment like this:**

::

    pip install obs-tools


**To install a particular version (tag, branch or commit) use this:**

::

    pip install git+git://github.com/unfoldingWord-dev/obs_tools.git@Tag-Branch-or-Commit#egg=obs_tools


Submitting to pypi
******************

**Add the library to pypi if you haven't already.**

1. Run ``python setup.py sdist bdist_wheel --universal``.
2. Go to https://pypi.python.org/pypi?%3Aaction=submit_form
3. Click "Choose File" and pick ``obs_tools.egg-info/PKG-INFO``, then click "Add Package Info."

**Install twine**

::

    sudo pip install twine

**Create settings file ``~/.pypirc`` with these contents:**

::

    [distutils]
    index-servers=pypi

    [pypi]
    repository = https://upload.pypi.org/legacy/
    username = <USER-NAME>
    password = <PASSWORD>

**Generate the packages and upload**

::

    python setup.py sdist bdist_wheel --universal
    twine upload dist/*

