from aqt.utils import askUser, showCritical, tooltip, showInfo
from aqt import QProcess
import sys
import os
import platform

_pip_process = QProcess()
_pip_process.setProcessChannelMode(QProcess.ProcessChannelMode.ForwardedChannels)

def install(package_name: str):
    global _pip_process
    confirmed = askUser(
f"""This will install {package_name} into anki

You will need to install python or at least pip for this to work.
You may also need to install git if the package requires it.

It is recommended for you to run anki in administrator mode or else this might not work.

Proceed?""",
title="Install package?")

    if confirmed: 
        # Not everyone is going to have git installed but works for testing.

        if platform.system() in {"Windows", "Mac"}:
            anki_lib_path = sys.executable
            anki_lib_path = os.path.dirname(anki_lib_path)
            anki_lib_path = os.path.join(anki_lib_path, "lib") # .../anki/lib

            # https://stackoverflow.com/a/2916320
            _pip_process.start("pip", ["install", f'--target={anki_lib_path}', package_name])
        elif platform.system() == "Linux": # For linux
            _pip_process.start(sys.executable, ["-m", "pip", "install", package_name])
        else:
            # I dont think anki itself supports any different operating systems so this should never be reached
            showCritical(f"Not supported for operating system: '{platform.system()}'") 

        tooltip("Installing package {package_name}")
        def finished(exitCode,  exitStatus):
            if exitCode == 0:
                showInfo(f"Package \"{package_name}\" installed successfully, restart for it to take effect")
            else:
                showCritical(
f"""Package \"{package_name}\" wasn't installed. For more information, run anki in console mode. (on windows anki-console.bat)

Error code: '{exitCode}', Error status '{exitStatus}'
"""
)
        _pip_process.finished.connect(finished)

def dependencies():
    install("matplotlib")