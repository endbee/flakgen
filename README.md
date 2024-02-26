# Flakgen 
A tool written for the randomized generation of flaky test suites.

## Requirements
 - Python 3 (Python 3.11)
 - pip (pip 23.0.1)

## Installation
1. Clone repository
2. Create virtual environment: ``python3 -m venv venv``
3. Activate virtual environment: ``source venv/bin/activate`` (Mac), ``venv\Scripts\activate`` (Win)
4. Install dependencies: ``pip install -r requirements.txt``

## Usage
- ``python main.py`` (Generates the test suite and runs it once)
- ``python main.py --with_eval`` (Generates the test suite and runs the evaluation code, note that this might take several minutes)

### CharmFL usage
- Prerequisites
  - PyCharm 2021.2.4 PY-212.5712.39 December 21, 2021
  - [CharmFL](https://interactivefaultlocalization.github.io/tools/charmfl) plugin installed 
    - check documentation installation guidelines
- Trying out CharmFL with the generated test suites
  - Run: ``python main.py --for_charmfl`` (CharmFl requires the files to be structured in a certain way that does not fit other use cases of this tool. Thats why we seperated this kind of generation from the "normal" one.)
  - Now "Start Fault Localization" via the CharmFL context menu located on the top of the IDE

Note that neither of the command line arguments are intended to be used in combination. 
## Configuration
- The standard configuration is given in  the ``config.json`` file, these values can be altered 
- Also another configuration file could be created and then the file path could be passed to the tool like this:
  ``python main.py --config_file_path path_to_file``
