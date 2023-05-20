from aqt.utils import askUser, showCritical, tooltip, showInfo
from aqt import QProcess
import sys
import os
import platform

pip_process = QProcess()
pip_process.setProcessChannelMode(QProcess.ProcessChannelMode.ForwardedChannels)

def install(package_name: str):
    global pip_process
    confirmed = askUser(
f"""This will install {package_name} into anki

You will need to install python or at least pip for this to work.
You may also need to install git if the package requires it.

It is recommended for you to run anki with command line (anki-console.bat on windows) as otherwise there is no progress bar.

Proceed?""",
title="Install package?")

    if confirmed: 
        # Not everyone is going to have git installed but works for testing.

        if platform.system() in {"Windows", "Mac"}:
            anki_lib_path = sys.executable
            anki_lib_path = os.path.dirname(anki_lib_path)
            anki_lib_path = os.path.join(anki_lib_path, "lib") # .../anki/lib

            # https://stackoverflow.com/a/2916320
            pip_process.start("pip", ["install", f'--target={anki_lib_path}', package_name])
        elif platform.system() == "Linux": # For linux
            pip_process.start(sys.executable, ["-m", "pip", "install", package_name])
        else:
            # I dont think anki itself supports any different operating systems so this should never be reached
            showCritical(f"Not supported for operating system: '{platform.system()}'") 

        tooltip("Installing optimizer")
        def finished(exitCode,  exitStatus):
            if exitCode == 0:
                showInfo("Optimizer installed successfully, restart for it to take effect")
            else:
                showCritical(
f"""Optimizer wasn't installed. For more information, run anki in console mode. (on windows anki-console.bat)

Error code: '{exitCode}', Error status '{exitStatus}'
"""
)
        pip_process.finished.connect(finished)