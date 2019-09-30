---
name: Bug Report
about: Simfin gives unexpected results, raises an exception, or causes another problem
title: Bug Report
labels: bug
assignees: ''

---

# Bug Report

If you experience errors or bugs, please make a serious effort to solve the
problem yourself before asking here. The problem is quite likely in your own
code and a simple Google search for the error-message may help you solve it.
If it is a problem directly related to simfin, then please search the closed
GitHub issues, because it may already have been answered there.

Please make sure you have the latest simfin package installed by running:

    pip install --upgrade simfin
 
And make sure you have downloaded fresh data-files from the SimFin server
by setting `refresh_days=0` (see example below).

If you still cannot solve the problem and need our help, then please provide
the following.


## Description

Please write a brief description of the bug / error you have experienced.


## System Details

- Python version
- Simfin version
- Other relevant package versions
- Operation System and version
- Computer's CPU, RAM-size, free HD space, etc.
- Other relevant system information


## Code Example

Please write a minimal source-code example that reproduces the problem.
You can indent the code-block to get proper code-formatting, for example:

    import simfin as sf

    # Print SimFin version.
    print(sf.__version__)

    # Configure simfin.
    sf.set_data_dir('~/simfin_data/')
    sf.load_api_key(path='~/simfin_api_key.txt', default_key='free')

    # Download fresh data from the server by setting refresh_days=0
    df = sf.load_income(variant='annual', refresh_days=0)

    # Do something that causes an error.


## Result / Error

Please write the full output and error message you received. You can also
indent this text-block by pressing the tab-key to get proper formatting
of the error-message.
