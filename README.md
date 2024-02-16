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
Run main: ``python main.py``

## Configuration
- The standard configuration is given in  the ``config.json`` file, these values can be altered 
- Also another configuration file could be created and then the file path could be passed to the tool like this:
  ``python main.py --config_file_path path_to_file``

## Evaluation
Run main with evaluation ``python main.py --with_eval``
