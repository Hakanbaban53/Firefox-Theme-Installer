# Firefox Theme Installer Test Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Setup](#setup)
3. [Running Tests](#running-tests)
4. [Test Cases](#test-cases)
5. [Build App](#build-app)

## Introduction
This document provides an overview of the tests for the Firefox Theme Installer project. It includes instructions on setting up the test environment, running tests, and details of individual test cases.

## Setup
To set up the test environment, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/Firefox-Theme-Installer.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Firefox-Theme-Installer/test
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running Tests
To run the tests, use the following command:
```bash
pytest # Not implemented yet
```

## Test Cases (Not implemented yet)
### Test Case 1: Detect OS
**Description:** Verify that the `detect_os` method correctly identifies the operating system.

**Steps:**
1. Initialize the `OSProperties` class.
2. Call the `detect_os` method.
3. Assert that the returned value matches the expected OS.

**Expected Result:** The method should return 'windows', 'macos', or 'linux' based on the current OS.

### Test Case 2: Load OS Data
**Description:** Verify that the `load_os_data` method loads the correct OS-specific data.

**Steps:**
1. Initialize the `OSProperties` class.
2. Call the `load_os_data` method.
3. Assert that the returned dictionary matches the expected OS data.

**Expected Result:** The method should return the correct dictionary for the current OS.

### Test Case 3: Get Theme Preview Location
**Description:** Verify that the `get_theme_preview_location` method returns the correct path.

**Steps:**
1. Initialize the `OSProperties` class.
2. Call the `get_theme_preview_location` method.
3. Assert that the returned path matches the expected preview location.

**Expected Result:** The method should return the correct path for the theme preview location.

## Build App
To build the app, follow these steps:

To clone and run this application, you'll need [Git](https://git-scm.com), Python and some python libraries installed on your computer. From your command line:

1. Clone the repository:
    ```bash
    $ git clone https://github.com/Hakanbaban53/Firefox-Theme-Installer
    ```
2. Go into the repository:
    ```bash
    $ cd Firefox-Theme-Installer
    ```
3. Install dependencies:
    ```bash
    pip install -r test/requirements.txt
    ```
4. Build the app in Windows (If you are using Windows):
    ```bash
    pyinstaller --onefile .\src\app.py --icon=../Firefox-Theme-Installer/src/assets/firefox.ico --add-data "..\Firefox-Theme-Installer\src\assets;assets" --add-data "..\Firefox-Theme-Installer\src\data\language;data\language"
    ```
5. Build the app in Linux (If you are using Linux):
    ```bash
    pyinstaller --onefile ./src/app.py --hidden-import='PIL._tkinter_finder' --add-data="../Firefox-Theme-Installer/src/assets:assets" --add-data="../Firefox-Theme-Installer/src/data/language:data/language"
    ```
> **Note 1 🔩**
> If you want to launch with no console add the '--noconsole' argument.

> **Note 2 🔩**
> If you encounter the externally-managed-environment error while downloading with pip3 on Linux, add the `--break-system-packages` argument (Warning ⚠️: this argument may cause conflicts between system packages and pip packages. If your Linux distribution has the necessary packages, please use the Linux package manager).


## Conclusion
This document provides a comprehensive guide to setting up and running tests for the Firefox Theme Installer project. By following the steps outlined in this document, you can ensure that the application functions correctly across different operating systems and scenarios. If you encounter any issues or have questions about the testing process, please refer to the project's documentation or reach out to the project maintainers for assistance. Thank you for your interest in the Firefox Theme Installer project!
