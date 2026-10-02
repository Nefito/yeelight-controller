APP_STYLE = """
QWidget {
    background-color: #202124;
    color: #f1f3f4;
    font-size: 14px;
}

QLabel {
    background-color: transparent;
}

QLabel#windowTitle {
    font-size: 22px;
    font-weight: 600;
    color: #ffffff;
}

QLabel#windowSubtitle {
    font-size: 13px;
    color: #9aa0a6;
}

QLabel#statusLabel {
    font-size: 13px;
    color: #9aa0a6;
    padding: 4px 0;
}

QLabel#sectionTitle {
    font-size: 15px;
    font-weight: 600;
    color: #ffffff;
    padding-bottom: 2px;
}

QFrame#sectionCard {
    background-color: #292a2d;
    border: 1px solid #3c4043;
    border-radius: 10px;
}

QFrame#sectionCard QWidget#sectionHeader,
QFrame#sectionCard QWidget#sectionContent {
    background-color: transparent;
}

QFrame#sectionCard QWidget#sectionContent QWidget {
    background-color: transparent;
}

QToolButton#sectionToggleButton {
    background-color: transparent;
    border: none;
    padding: 2px;
}

QToolButton#sectionToggleButton:hover {
    background-color: #3a3b3f;
    border-radius: 4px;
}

QScrollArea#controlScrollArea {
    background-color: transparent;
    border: none;
}

QScrollArea#controlScrollArea > QWidget > QWidget {
    background-color: transparent;
}

QScrollBar:vertical {
    background-color: #202124;
    width: 10px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #4a4b4f;
    min-height: 30px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background-color: #5f6368;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background-color: transparent;
}

QWidget#colorInfo {
    background-color: #232427;
    border: 1px solid #3c4043;
    border-radius: 8px;
}

QLabel#colorPreview {
    border-radius: 6px;
}

QLabel#colorInfoTitle {
    font-size: 12px;
    color: #9aa0a6;
}

QLabel#colorHex {
    font-size: 17px;
    font-weight: 600;
    color: #ffffff;
}

QLabel#colorRgb {
    font-size: 12px;
    color: #9aa0a6;
}

QLabel#brightnessTitle {
    font-size: 13px;
    color: #9aa0a6;
}

QLabel#brightnessValue {
    font-size: 18px;
    font-weight: 600;
    color: #ffffff;
}

QLabel#effectLabel {
    font-size: 13px;
    color: #9aa0a6;
}

QLabel#effectStatus {
    font-size: 12px;
    color: #9aa0a6;
}

QLabel#effectSpeedValue {
    font-size: 14px;
    font-weight: 600;
    color: #ffffff;
}

QComboBox#effectSelector {
    background-color: #303134;
    color: #f1f3f4;
    border: 1px solid #4a4b4f;
    border-radius: 6px;
    padding: 7px 10px;
    min-height: 18px;
}

QComboBox#effectSelector:hover {
    border-color: #6b6d73;
}

QComboBox#effectSelector:disabled {
    background-color: #252629;
    color: #6f7378;
    border-color: #343538;
}

QComboBox#effectSelector::drop-down {
    border: none;
    width: 24px;
}

QComboBox#effectSelector:disabled::drop-down {
    background-color: transparent;
}

QComboBox#effectSelector QAbstractItemView {
    background-color: #303134;
    color: #f1f3f4;
    border: 1px solid #4a4b4f;
    selection-background-color: #3a3b3f;
}

QPushButton {
    background-color: #303134;
    color: #f1f3f4;
    border: 1px solid #4a4b4f;
    border-radius: 6px;
    padding: 8px 14px;
    min-height: 18px;
}

QPushButton:hover {
    background-color: #3a3b3f;
    border-color: #6b6d73;
}

QPushButton:pressed {
    background-color: #28292c;
}

QPushButton#powerButton {
    background-color: #8ab4f8;
    color: #202124;
    border: none;
    font-weight: 600;
    padding: 8px 18px;
}

QPushButton#powerButton:hover {
    background-color: #a8c7fa;
}

QPushButton#powerButton:pressed {
    background-color: #7aa7e8;
}

QPushButton#powerButton:disabled {
    background-color: #4a4b4f;
    color: #9aa0a6;
}

QPushButton#effectButton {
    min-width: 64px;
}

QSlider {
    background-color: transparent;
}

QSlider::groove:horizontal {
    height: 6px;
    background-color: #3a3b3f;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    width: 16px;
    height: 16px;
    margin: -5px 0;
    background-color: #f1f3f4;
    border: 1px solid #9aa0a6;
    border-radius: 8px;
}

QSlider::handle:horizontal:hover {
    background-color: #ffffff;
    border-color: #ffffff;
}

QSlider::handle:horizontal:pressed {
    background-color: #d7d9dc;
}

QSlider::handle:horizontal:disabled {
    background-color: #55575b;
    border-color: #45474b;
}

QSlider::groove:horizontal:disabled {
    background-color: #292a2d;
}

QSlider::sub-page:horizontal {
    background-color: #8ab4f8;
    border-radius: 3px;
}

QSlider::sub-page:horizontal:disabled {
    background-color: #45474b;
}

QSlider::add-page:horizontal {
    background-color: #3a3b3f;
    border-radius: 3px;
}

QSlider::add-page:horizontal:disabled {
    background-color: #292a2d;
}

QLabel#timerLabel {
    font-size: 13px;
    color: #9aa0a6;
}

QLabel#timerRemaining {
    font-size: 13px;
    color: #f1f3f4;
}

QSpinBox#timerInput,
QTimeEdit#timerTimeInput {
    background-color: #303134;
    color: #f1f3f4;
    border: 1px solid #4a4b4f;
    border-radius: 6px;
    padding: 6px 8px;
    min-width: 70px;
}

QSpinBox#timerInput:hover,
QTimeEdit#timerTimeInput:hover {
    border-color: #6b6d73;
}

QSpinBox#timerInput:focus,
QTimeEdit#timerTimeInput:focus {
    border-color: #8ab4f8;
}

QWidget#timerInputContainer {
    background-color: transparent;
}

QToolButton#timerArrowButton {
    background-color: #303134;
    border: 1px solid #4a4b4f;
    border-radius: 4px;
    padding: 0;
    min-width: 20px;
    min-height: 14px;
    max-width: 20px;
    max-height: 18px;
}

QToolButton#timerArrowButton:hover {
    background-color: #3a3b3f;
    border-color: #6b6d73;
}

QToolButton#timerArrowButton:pressed {
    background-color: #28292c;
}

QFrame#timerSeparator {
    background-color: #3c4043;
    border: none;
    max-height: 1px;
    min-height: 1px;
    margin: 4px 0;
}

QPushButton#timerButton {
    min-width: 90px;
}

QPushButton#timerCancelButton {
    min-width: 90px;
}
"""