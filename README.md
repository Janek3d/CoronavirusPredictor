# Python Project for Python programming and data analysis

Authors: Szymon Krasuski & Janusz Mikłuszka

# Setup
In order to setup python evnironment required is Python >=3.6 (At least code was not tested with versions before 3.6).

All requirements are specified in requirements.txt file.
`pip install -r requirements.txt` will install them with pip.

# Run
In order to run application execute run.py script (`python run.py` or `run.py` if you have python binary under /usr/bin/python path).
Afterwards, go to your favourite web browser and enter address `127.0.0.1:8080`.
You should open GUI which allow to load data, set predict horizon dates and desired model for training.
With all set parameters Predict button will show interactive graph.

## Alternative use
Project is modular and may be used with any GUI (or without one), so if you prefer to execute next prediction steps from python code - `example.py` file shows how it may be done in harder way and only with matplotlib plot (no beautiful interactive graphs).

# Tests
Tests may be run with `tox` command (tox should be installed before with `pip install tox`).
This command will run unit tests and test which checks whether code match PEP8 standards.
