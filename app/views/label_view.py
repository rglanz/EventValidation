from PyQt5.QtCore import QStringListModel, Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import (
    QCompleter,
    QDialog,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        hotkeys = {
            Qt.Key_Tab: self.parent.toggle_rocker,
            Qt.Key_Escape: self.parent.reject,
            Qt.Key_Return: self.handle_enter,
            Qt.Key_Enter: self.handle_enter,
        }

        if key in hotkeys:
            hotkeys[key]()
        else:
            super().keyPressEvent(event)

    def handle_enter(self):
        self.complete_text()
        self.parent.accept()

    def complete_text(self):
        completer = self.completer()
        if completer and completer.popup().isVisible():
            completer.setCurrentRow(0)
            index = completer.currentIndex()
            if index.isValid():
                self.setText(completer.currentCompletion())
                completer.popup().hide()  # Hide the popup after completion


class LabelView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.suggestions = [
            "arm",
            "hand",
            "fingers",
            "leg",
            "foot",
            "toes",
            "head",
            "neck",
        ]

        # Components
        self.rocker = QPushButton("R")
        self.rocker.setCheckable(True)

        self.text_edit = CustomLineEdit(self)
        self.completer = QCompleter()
        model = QStringListModel(self.suggestions)
        self.completer.setModel(model)
        self.completer.setFilterMode(Qt.MatchContains)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.text_edit.setCompleter(self.completer)

        self.confirm_button = QPushButton("Confirm")

        # Layout
        layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.rocker)
        top_layout.addWidget(self.text_edit)

        layout.addLayout(top_layout)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)
        self.setWindowTitle("Custom Message Box")
        self.setFixedSize(300, 150)

        # Signals
        self.rocker.clicked.connect(self.toggle_rocker)
        self.confirm_button.clicked.connect(self.accept)

    def toggle_rocker(self):
        self.rocker.setChecked(not self.rocker.isChecked())
        if self.rocker.isChecked():
            self.rocker.setText("L")
        else:
            self.rocker.setText("R")

    def accept(self):
        self.completer.popup().hide()
        super().accept()

    def reject(self):
        self.completer.popup().hide()
        super().reject()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)

    def parse_label(self):
        side = "L" if self.rocker.isChecked() else "R"
        label = self.text_edit.text().lower()
        clean_label = "_".join(label.lower().split()) or ""

        return f"{side}_{clean_label}"
