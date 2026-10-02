from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPen
from PySide6.QtWidgets import QWidget


class ColorPicker(QWidget):
    colorChanged = Signal(QColor)

    def __init__(
        self,
        color: QColor,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self.setMinimumSize(300, 240)

        self.hue = color.hsvHue()

        self.hue = max(self.hue, 0)

        self.saturation = color.hsvSaturation()
        self.value = color.value()

        self.dragging_color = False
        self.dragging_hue = False

    def current_color(self) -> QColor:
        return QColor.fromHsv(
            self.hue,
            self.saturation,
            self.value,
        )

    def set_color(self, color: QColor) -> None:
        hue = color.hsvHue()

        self.hue = max(hue, 0)
        self.saturation = color.hsvSaturation()
        self.value = color.value()

        self.update()

    def color_area_rect(self):
        margin = 10
        hue_height = 25
        spacing = 10

        return self.rect().adjusted(
            margin,
            margin,
            -margin,
            -(margin + hue_height + spacing),
        )

    def hue_rect(self):
        margin = 10
        hue_height = 25

        return self.rect().adjusted(
            margin,
            self.height() - margin - hue_height,
            -margin,
            -margin,
        )

    def paintEvent(self, event) -> None:
        del event

        painter = QPainter(self)

        color_rect = self.color_area_rect()

        hue_color = QColor.fromHsv(
            self.hue,
            255,
            255,
        )

        white_gradient = QLinearGradient(
            color_rect.topLeft(),
            color_rect.topRight(),
        )

        white_gradient.setColorAt(
            0.0,
            QColor(255, 255, 255),
        )

        white_gradient.setColorAt(
            1.0,
            hue_color,
        )

        painter.fillRect(
            color_rect,
            white_gradient,
        )

        black_gradient = QLinearGradient(
            color_rect.topLeft(),
            color_rect.bottomLeft(),
        )

        black_gradient.setColorAt(
            0.0,
            QColor(0, 0, 0, 0),
        )

        black_gradient.setColorAt(
            1.0,
            QColor(0, 0, 0, 255),
        )

        painter.fillRect(
            color_rect,
            black_gradient,
        )

        hue_rect = self.hue_rect()

        hue_gradient = QLinearGradient(
            hue_rect.left(),
            0,
            hue_rect.right(),
            0,
        )

        hue_colors = [
            QColor.fromHsv(0, 255, 255),
            QColor.fromHsv(60, 255, 255),
            QColor.fromHsv(120, 255, 255),
            QColor.fromHsv(180, 255, 255),
            QColor.fromHsv(240, 255, 255),
            QColor.fromHsv(300, 255, 255),
            QColor.fromHsv(359, 255, 255),
        ]

        for index, color in enumerate(hue_colors):
            hue_gradient.setColorAt(
                index / (len(hue_colors) - 1),
                color,
            )

        painter.fillRect(
            hue_rect,
            hue_gradient,
        )

        x = color_rect.left() + (
            self.saturation / 255
        ) * color_rect.width()

        y = color_rect.bottom() - (
            self.value / 255
        ) * color_rect.height()

        marker_radius = 7

        painter.setPen(
            QPen(
                QColor(255, 255, 255),
                2,
            )
        )

        painter.drawEllipse(
            int(x - marker_radius),
            int(y - marker_radius),
            marker_radius * 2,
            marker_radius * 2,
        )

        hue_x = hue_rect.left() + (
            self.hue / 359
        ) * hue_rect.width()

        painter.drawLine(
            int(hue_x),
            hue_rect.top(),
            int(hue_x),
            hue_rect.bottom(),
        )

    def mousePressEvent(self, event) -> None:
        if event.button() != Qt.MouseButton.LeftButton:
            return

        position = event.position().toPoint()

        if self.color_area_rect().contains(position):
            self.dragging_color = True
            self.update_color_from_position(position)

        elif self.hue_rect().contains(position):
            self.dragging_hue = True
            self.update_hue_from_position(position)

    def mouseMoveEvent(self, event) -> None:
        position = event.position().toPoint()

        if self.dragging_color:
            self.update_color_from_position(position)

        elif self.dragging_hue:
            self.update_hue_from_position(position)

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging_color = False
            self.dragging_hue = False

    def update_color_from_position(self, position) -> None:
        rect = self.color_area_rect()

        x = max(
            rect.left(),
            min(position.x(), rect.right()),
        )

        y = max(
            rect.top(),
            min(position.y(), rect.bottom()),
        )

        saturation = int(
            ((x - rect.left()) / rect.width()) * 255
        )

        value = int(
            ((rect.bottom() - y) / rect.height()) * 255
        )

        self.saturation = saturation
        self.value = value

        self.update()
        self.colorChanged.emit(
            self.current_color()
        )

    def update_hue_from_position(self, position) -> None:
        rect = self.hue_rect()

        x = max(
            rect.left(),
            min(position.x(), rect.right()),
        )

        self.hue = int(
            ((x - rect.left()) / rect.width()) * 359
        )

        self.update()
        self.colorChanged.emit(
            self.current_color()
        )