from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class SectionCard(QFrame):
    def __init__(
        self,
        title: str,
        parent: QWidget | None = None,
        collapsible: bool = False,
        collapsed: bool = False,
    ):
        super().__init__(parent)

        self.setObjectName("sectionCard")

        self.collapsible = collapsible
        self.collapsed = collapsed

        self.content_layout = QVBoxLayout(self)
        self.content_layout.setContentsMargins(
            16,
            12,
            16,
            16,
        )
        self.content_layout.setSpacing(8)

        self.create_header(title)

        self.content_widget = QWidget(self)
        self.content_widget.setObjectName(
            "sectionContent"
        )

        self.inner_layout = QVBoxLayout(
            self.content_widget
        )
        self.inner_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        self.inner_layout.setSpacing(8)

        self.content_layout.addWidget(
            self.content_widget
        )

        self.update_collapsed_state()

    def create_header(
        self,
        title: str,
    ) -> None:
        self.header_widget = QWidget(self)
        self.header_widget.setObjectName(
            "sectionHeader"
        )

        header_layout = QHBoxLayout(
            self.header_widget
        )
        header_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        header_layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setObjectName(
            "sectionTitle"
        )

        header_layout.addWidget(
            title_label
        )
        header_layout.addStretch()

        if self.collapsible:
            self.toggle_button = QToolButton(
                self
            )
            self.toggle_button.setObjectName(
                "sectionToggleButton"
            )
            self.toggle_button.setAutoRaise(True)
            self.toggle_button.setCursor(
                Qt.CursorShape.PointingHandCursor
            )
            self.toggle_button.clicked.connect(
                self.toggle_collapsed
            )

            header_layout.addWidget(
                self.toggle_button
            )
        else:
            self.toggle_button = None

        self.content_layout.addWidget(
            self.header_widget
        )

    def add_widget(
        self,
        widget: QWidget,
    ) -> None:
        self.inner_layout.addWidget(widget)

    def toggle_collapsed(self) -> None:
        self.collapsed = not self.collapsed
        self.update_collapsed_state()

    def update_collapsed_state(self) -> None:
        self.content_widget.setVisible(
            not self.collapsed
        )

        if self.collapsed:
            self.content_layout.setContentsMargins(
                16,
                10,
                16,
                10,
            )
            self.content_layout.setSpacing(0)

            collapsed_height = (
                self.header_widget.sizeHint().height()
                + 20
            )

            self.setFixedHeight(
                collapsed_height
            )

            self.setSizePolicy(
                QSizePolicy.Policy.Preferred,
                QSizePolicy.Policy.Fixed,
            )
        else:
            self.setMinimumHeight(0)
            self.setMaximumHeight(16_777_215)

            self.setSizePolicy(
                QSizePolicy.Policy.Preferred,
                QSizePolicy.Policy.Preferred,
            )

            self.content_layout.setContentsMargins(
                16,
                12,
                16,
                16,
            )
            self.content_layout.setSpacing(8)

        if self.toggle_button is None:
            return

        if self.collapsed:
            self.toggle_button.setArrowType(
                Qt.ArrowType.RightArrow
            )
            self.toggle_button.setToolTip(
                "Expand section"
            )
        else:
            self.toggle_button.setArrowType(
                Qt.ArrowType.DownArrow
            )
            self.toggle_button.setToolTip(
                "Collapse section"
            )

        self.updateGeometry()