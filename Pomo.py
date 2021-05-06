import time
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia
from PyQt5.QtCore import QTimer
from PomodoroTimerUI import Ui_PomodoroTimerUI

class PomodoroTimerWindow(QtWidgets.QWidget, Ui_PomodoroTimerUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Pomo')

        self.WorkCounter.setHidden(True)
        self.BreakCounter.setHidden(True)
        self.CurrentStep.setHidden(True)
        self.WorkOrBreakLabel.setHidden(True)
        self.TimerLabel.setHidden(True)
        self.CompletedIntervalsLabel.setHidden(True)
        self.StopButton.setHidden(True)
        self.SoundCheckbox.setChecked(True)
        self.StartButton.clicked.connect(self.onClickStartButton)
        self.StopButton.clicked.connect(self.onClickStopButton)

    def onClickStartButton(self):
        self.WorkTimeLabel.setHidden(True)
        self.WorkTimeSpinner.setHidden(True)
        self.BreakTimeLabel.setHidden(True)
        self.BreakTimeSpinner.setHidden(True)
        self.TotalIntervalsLabel.setHidden(True)
        self.TotalIntervalsSpinner.setHidden(True)
        self.StartButton.setHidden(True)

        self.WorkOrBreakLabel.setHidden(False)
        self.TimerLabel.setText('Loading...')
        self.TimerLabel.setHidden(False)
        self.CompletedIntervalsLabel.setHidden(False)
        self.StopButton.setHidden(False)
        self.CompletedIntervalsLabel.setText('Completed ' + str(self.CurrentStep.intValue()) + ' of ' + str(self.TotalIntervalsSpinner.value()) + ' work sessions')
        self.WorkOrBreakLabel.setText('Loading...')
        self.WorkCounter.display(self.WorkTimeSpinner.value() * 60)
        self.BreakCounter.display(self.BreakTimeSpinner.value() * 60)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.StartTimer)
        self.timer.start(1000)

    def onClickStopButton(self):
        self.WorkOrBreakLabel.setHidden(True)
        self.TimerLabel.setHidden(True)
        self.CompletedIntervalsLabel.setHidden(True)
        self.StopButton.setHidden(True)

        self.WorkTimeLabel.setHidden(False)
        self.WorkTimeSpinner.setHidden(False)
        self.BreakTimeLabel.setHidden(False)
        self.BreakTimeSpinner.setHidden(False)
        self.TotalIntervalsLabel.setHidden(False)
        self.TotalIntervalsSpinner.setHidden(False)
        self.StartButton.setHidden(False)

        self.timer.stop()
        self.CurrentStep.display(0)
        self.WorkOrBreakLabel.setText('')
        self.CompletedIntervalsLabel.setText('')

    def StartTimer(self):
        if self.CurrentStep.intValue() < self.TotalIntervalsSpinner.value():

            if self.WorkCounter.intValue() > 0 and self.BreakCounter.intValue() > 0:
                self.WorkOrBreakLabel.setText('Working...')
                self.WorkCounter.display(self.WorkCounter.intValue() - 1)
                work_remaining_subtracted = self.WorkCounter.intValue()
                work_remaining_converted = str(datetime.timedelta(seconds=work_remaining_subtracted))
                self.TimerLabel.setText(work_remaining_converted)
                if self.WorkCounter.intValue() <= 0:
                    self.CurrentStep.display(self.CurrentStep.intValue() + 1)
                    self.CompletedIntervalsLabel.setText('Completed ' + str(self.CurrentStep.intValue()) + ' of ' + str(self.TotalIntervalsSpinner.value()) + ' work sessions')
                    if self.SoundCheckbox.isChecked():
                        QtMultimedia.QSound.play('AlarmSounds/DoorChime.wav')

            elif self.WorkCounter.intValue() == 0 and self.BreakCounter.intValue() > 0:
                self.WorkOrBreakLabel.setText('Breaking...')
                self.BreakCounter.display(self.BreakCounter.intValue() - 1)
                break_remaining_subtracted = self.BreakCounter.intValue()
                break_remaining_converted = str(datetime.timedelta(seconds=break_remaining_subtracted))
                self.TimerLabel.setText(break_remaining_converted)
                if self.BreakCounter.intValue() <= 0:
                    if self.SoundCheckbox.isChecked():
                        QtMultimedia.QSound.play('AlarmSounds/DoorChime.wav')

            elif self.WorkCounter.intValue() == 0 and self.BreakCounter.intValue() == 0:
                self.WorkCounter.display(self.WorkTimeSpinner.value() * 60)
                self.BreakCounter.display(self.BreakTimeSpinner.value() * 60)
            
        else:
            self.timer.stop()
            self.TimerLabel.setText('All done! Great work!')
            self.WorkOrBreakLabel.setText('Finished')

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_app_window = PomodoroTimerWindow()
    main_app_window.show()
    sys.exit(app.exec_())