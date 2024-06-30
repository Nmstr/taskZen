from PySide6.QtWidgets import QMainWindow, QWidget, QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import os
import pty
import subprocess

from PySide6.QtCore import QObject, Signal, QThread

class ScriptRunner(QObject):
    finished = Signal()
    error = Signal(Exception)
    outputUpdated = Signal(str)

    def __init__(self, filepath: str) -> None:
        super().__init__()
        self.filepath = filepath

    def run(self):
        try:
            # The master_fd is the file descriptor of the master end of the pty
            # The slave_fd is the file descriptor of the slave end of the pty
            master_fd, slave_fd = pty.openpty()

            # Start the subprocess with the slave end as its controlling terminal
            process = subprocess.Popen(['taskZen', 'execute', '-fv', self.filepath],
                                    stdout=slave_fd, stderr=subprocess.STDOUT, stdin=slave_fd, close_fds=True)

            # Close the slave FD to avoid keeping it open unnecessarily
            os.close(slave_fd)

            while True:
                # Read output from the master end of the pty
                output = os.read(master_fd, 512)
                if not output:
                    break
                #print(output.decode(), end='')
                self.outputUpdated.emit(output.decode())

            # Wait for the subprocess to finish
            process.wait()

        except Exception as e:
            self.error.emit(e)
        finally:
            self.finished.emit()
            # Make sure to close the master FD
            os.close(master_fd)

class ScriptWindow(QMainWindow):
    def __init__(self, parent: QWidget = None, filepath: str = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("taskZen - Script")
        self.filepath = filepath

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
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            self.filepath, _ = QFileDialog.getSaveFileName(self, "Save Script", os.path.expanduser("~/.config/taskZen/scripts"), "Yaml Files (*.yaml)", options=options)
            if self.filepath == '':
                return

        with open(self.filepath, 'w') as f:
            f.write(scriptData)

        self.outputText = 'Script saved\n'
        self.ui.sideText.setText(self.outputText)

    def runScript(self) -> None:
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

        # Start the worker when the thread starts
        self.thread.started.connect(self.scriptRunner.run)
        self.thread.start()

        self.ui.runBtn.setDisabled(True)
        self.scriptRunner.finished.connect(lambda: self.ui.runBtn.setDisabled(False))

    def updateSideText(self, text):
        # Update the GUI safely with the new text
        self.outputText += text
        self.ui.sideText.setPlainText(self.outputText)