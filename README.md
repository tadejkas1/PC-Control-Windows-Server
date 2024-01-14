# PC Control Web Application

## Overview
This Python Flask web application provides a web interface for controlling various PC functionalities, such as monitor control and system status updates. It's designed for ease of use and can be accessed through a web browser.

## Features
- Web-based control interface for your PC.
- Options to turn the monitor on or off.
  
## HomeKit Integration
Apple users can integrate this application with HomeKit using the [PcControl Homebridge plugin](https://github.com/tadejkas1/PcControl). This plugin extends the capabilities of this application, allowing you to control your PC using Apple's Home app and Siri.

## Installation
Before running the application, you need to set up Python and install the necessary dependencies.

1. **Install Python**: If you haven't already, download and install Python from [python.org](https://www.python.org/downloads/).

2. **Install Dependencies**: To install the necessary dependencies, use the provided batch script `run.bat`. This script will automatically install the packages listed in `requirements.txt`. To execute the script, double-click on `run.bat` in the application directory.

4. **Setup Application**: Download all the application files (`PcControl.py`, HTML templates, etc.) to your system.


## Start the Web Server:
   After installing the dependencies, you can start the web server by running the following command in the application directory:

```bash
python PcControl.py
```
**Optional** - Create a Custom Start Script:
   If you prefer a one-click solution to start the server, you can create a custom script:
   - **Batch File (.bat)**: Create a batch file with the command `python PcControl.py`. Running this file will start the server. Here’s an example of what the batch file could contain:

     ```bat
     @echo off
     python PcControl.py
     ```

   - **VBScript File (.vbs)**: For a silent start (no command prompt window), create a VBScript file with the following content:

     ```vbscript
     Set WshShell = CreateObject("WScript.Shell")
     Return = WSHShell.Run("CMD /C python PcControl.py", 0, True)
     Set WshShell = Nothing
     ```

     Save this script with a `.vbs` extension. Double-clicking it will start the server without opening a command prompt window.

Whichever method you choose, these scripts provide an easy and efficient way to start your PC Control web application.

This will start the server, and you can access it through your web browser at the specified address (usually `http://localhost:90` unless you configured otherwise).

## Web Interface
The application provides several web pages for different functionalities:

- **Control Page**: Interface to control monitor settings and view system status.

## Customization
Feel free to modify the files

## Security
Since this application provides control over your PC, ensure it's running in a secure environment. Avoid exposing it to the public internet.

## Troubleshooting
If you encounter issues while running the application, check the following:

- Ensure Python and all dependencies are correctly installed.
- Verify the IP address and port settings if the application is not accessible.
- Check the console logs for any errors during startup or operation.

## Contribution
Contributions to improve the application or add new features are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Author:** [TaDejKas](https://github.com/tadejkas1)
**Version:** 1.5
