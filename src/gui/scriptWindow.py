from PySide6.QtWidgets import QMainWindow, QWidget, QFileDialog
from PySide6.QtCore import QFile, QObject, Signal, QThread
from PySide6.QtUiTools import QUiLoader

import subprocess
import pty
import os

class ScriptRunner(QObject):
    outputUpdated = Signal(str)
    finished = Signal()
    error = Signal(Exception)

    def __init__(self, filepath: str) -> None:
        super().__init__()
        self.filepath = filepath

    def run(self):
        try:
            master_fd, slave_fd = pty.openpty()
            currentPath = f'{os.path.dirname(os.path.realpath(__file__))}'
            if 'FLATPAK_ID' in os.environ:
                pythonExecutable = "/usr/bin/python"
            else:
                pythonExecutable = os.path.join(os.getenv('VIRTUAL_ENV', ''), 'bin/python')

            process = subprocess.Popen([pythonExecutable, f'{currentPath}/../main.py', 'execute', '-fvy', self.filepath],
                                       stdout=slave_fd, stderr=subprocess.STDOUT, stdin=slave_fd, close_fds=True)
            os.close(slave_fd)

            while True:
                output = os.read(master_fd, 512)
                if not output:
                    break
                self.outputUpdated.emit(output.decode())

            process.wait() # Wait for the subprocess to finish

        except Exception as e:
            self.error.emit(e)
        finally:
            self.finished.emit()
            os.close(master_fd)

class ScriptWindow(QMainWindow):
    def __init__(self, parent: QWidget = None, filepath: str = None) -> None:
        super().__init__(parent)
        self.setObjectName("ScriptWindow")
        self.setWindowTitle("taskZen - Script")
        self.filepath = filepath
        self.running = False

        # Load the UI file
        loader = QUiLoader()
        ui_file = QFile("src/gui/scriptWindow.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Set the UI geometry
        self.setGeometry(self.ui.geometry())

        # Connect buttons
        self.ui.saveBtn.clicked.connect(self.saveScript)
        self.ui.runBtn.clicked.connect(self.runScript)

        self.show()

        # Fill with text
        if self.filepath is not None:
            with open(self.filepath, 'r') as f:
                self.ui.scriptInput.setPlainText(f.read())

    def saveScript(self) -> None:
        self.outputText = 'Saving script...\n'
        self.ui.sideText.setText(self.outputText)
        scriptData = self.ui.scriptInput.toPlainText()

        if self.filepath is None:
            if 'FLATPAK_ID' in os.environ:
                defaultPath = os.path.expanduser('/home/user/.var/app/io.github.nmstr.taskZen/config/taskZen/scripts/')
            else:
                defaultPath = os.path.expanduser('~/.config/taskZen/scripts/')

            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            self.filepath, _ = QFileDialog.getSaveFileName(self, "Save Script", defaultPath, "Yaml Files (*.yaml)", options=options)
            if self.filepath == '':
                return

        with open(self.filepath, 'w') as f:
            f.write(scriptData)

        self.outputText = 'Script saved\n'
        self.ui.sideText.setText(self.outputText)

    def runScript(self) -> None:
        if self.running:
            self.updateSideText('Stopping script...\n')
            self.ui.sideText.setText(self.outputText)
            subprocess.run(['taskZen', 'execute', '-kf', self.filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.updateSideText('Script stopped\n')
            self.ui.sideText.setText(self.outputText)
            self.setRunning(False)
            return
        self.setRunning(True)
        self.outputText = 'Running script...\n'
        self.ui.sideText.setText(self.outputText)

        self.thread = QThread()
        self.scriptRunner = ScriptRunner(self.filepath)
        self.scriptRunner.moveToThread(self.thread)

        # Connect signals
        self.scriptRunner.finished.connect(self.thread.quit)
        self.scriptRunner.finished.connect(self.scriptRunner.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.scriptRunner.outputUpdated.connect(self.updateSideText)

        # Start the thread
        self.thread.started.connect(self.scriptRunner.run)
        self.thread.start()

        self.scriptRunner.finished.connect(lambda: self.setRunning(False))

    def setRunning(self, value):
        self.running = value
        if self.running:
            self.ui.runBtn.setStyleSheet("""
                                        background-color: #202327;
                                        border: 1px solid #810000;
                                    """)
        else:
            self.ui.runBtn.setStyleSheet("")
                                        

    def updateSideText(self, text):
        self.outputText += text
        self.ui.sideText.setPlainText(self.outputText)
