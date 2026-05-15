import os
from PySide6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel,
                               QWidget, QGraphicsDropShadowEffect, QPushButton,
                               QLineEdit, QSizePolicy, QButtonGroup)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QPixmap, QPainter, QPainterPath, QBrush, QPen, QLinearGradient

# =====================================================================
# HẰNG SỐ MÀU — PALETTE TRANG HỒ SƠ
# =====================================================================
COLOR_BANNER = "#3EE28C"
COLOR_TEAL   = "#266066"
COLOR_TEXT   = "#1A2A3A"
COLOR_MUTED  = "#8A9BAC"
COLOR_BORDER = "rgba(0, 77, 77, 0.18)"
COLOR_CARD_BG = "#F7FAFA"

_AVT_DEFAULT = os.path.join("assets", "fooderai-userpage", "fdai-userpage-unsignedin.png")


# =====================================================================
# HÀM TIỆN ÍCH
# =====================================================================
def _gradient_style(base_hex: str, radius: int = 12) -> str:
    dark = QColor(base_hex).darker(116).name()
    return f"""
        QPushButton {{
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                stop:0 {base_hex}, stop:1 {dark});
            border-radius: {radius}px;
            border: none;
            color: white;
        }}
        QPushButton:hover   {{ background: {QColor(base_hex).lighter(108).name()}; }}
        QPushButton:pressed {{ background: {dark}; }}
        QPushButton:disabled {{
            background: #C8D0D8;
            color: rgba(255,255,255,0.5);
        }}
    """


# =====================================================================
# LỚP 1: AVATARBOX
# =====================================================================
class AvatarBox(QLabel):
    def __init__(self, size: int = 180, parent=None):
        super().__init__(parent)
        self._size = size
        self._radius = size // 3
        self.setFixedSize(size, size)
        self._pix = None
        self.reset_default()

    def reset_default(self):
        if os.path.exists(_AVT_DEFAULT):
            pix = QPixmap(_AVT_DEFAULT).scaled(
                self._size, self._size,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            self._pix = pix
        else:
            self._pix = None
        self.update()

    def set_pixmap(self, pixmap: QPixmap):
        self._pix = pixmap.scaled(
            self._size, self._size,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        path.addRoundedRect(2, 2, self._size - 4, self._size - 4,
                            self._radius, self._radius)
        painter.setClipPath(path)

        if self._pix:
            painter.drawPixmap(0, 0, self._pix)
        else:
            grad = QLinearGradient(0, 0, self._size, self._size)
            grad.setColorAt(0.0, QColor("#3EE28C"))
            grad.setColorAt(1.0, QColor("#2ABF73"))
            painter.fillPath(path, QBrush(grad))

        painter.setClipping(False)
        painter.setPen(QPen(QColor(COLOR_BANNER), 2.5))
        painter.drawRoundedRect(2, 2, self._size - 4, self._size - 4,
                                self._radius, self._radius)


# =====================================================================
# LỚP 2: GENDERBUTTON
# =====================================================================
class GenderButton(QPushButton):
    COLORS = {
        "male":   ("#42A5F5", "#1E88E5"),
        "female": ("#F48FB1", "#E91E8C"),
    }

    def __init__(self, gender: str, label: str, parent=None):
        super().__init__(label, parent)
        self._gender = gender
        self.setFixedSize(92, 44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)
        self._shadow = QGraphicsDropShadowEffect()
        self._shadow.setBlurRadius(10)
        self._shadow.setOffset(0, 3)
        self.setGraphicsEffect(self._shadow)
        self._apply_style(selected=False)

    def _apply_style(self, selected: bool):
        base, dark = self.COLORS[self._gender]
        if selected:
            self._shadow.setColor(QColor(base).darker(120))
            self._shadow.setBlurRadius(12)
            self.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                        stop:0 {base}, stop:1 {dark});
                    border-radius: 22px;
                    border: 2px solid {QColor(base).lighter(120).name()};
                    color: white;
                    font-family: 'Roboto';
                    font-size: 16px;
                    font-weight: 700;
                }}
            """)
        else:
            self._shadow.setColor(QColor(0, 0, 0, 40))
            self._shadow.setBlurRadius(4)
            self.setStyleSheet("""
                QPushButton {
                    background-color: #E8ECF0;
                    border-radius: 22px;
                    border: 1.5px solid #C8D0D8;
                    color: #5E6E7E;
                    font-family: 'Roboto';
                    font-size: 15px;
                    font-weight: 600;
                }
                QPushButton:hover { background-color: #D8E0E8; }
            """)

    def setChecked(self, checked: bool):
        super().setChecked(checked)
        self._apply_style(selected=checked)


# =====================================================================
# LỚP 3: ACTIVITYBUTTON
# =====================================================================
class ActivityButton(QPushButton):
    BASE_COLOR = "#3EE28C"

    def __init__(self, main_text: str, sub_text: str, parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 5, 16, 5)
        lay.setSpacing(1)

        self._lbl_main = QLabel(main_text)
        f_main = QFont("Roboto")
        f_main.setPixelSize(16)
        f_main.setWeight(QFont.Weight.Medium)
        self._lbl_main.setFont(f_main)

        self._lbl_sub = QLabel(sub_text)
        f_sub = QFont("Roboto")
        f_sub.setPixelSize(13)
        self._lbl_sub.setFont(f_sub)

        lay.addWidget(self._lbl_main)
        lay.addWidget(self._lbl_sub)

        self._apply_style(False)

    def _apply_style(self, selected: bool):
        dark = QColor(self.BASE_COLOR).darker(116).name()
        if selected:
            style = f"""
                QPushButton {{
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                        stop:0 {self.BASE_COLOR}, stop:1 {dark});
                    border-radius: 12px; border: none;
                }}
            """
            self._lbl_main.setStyleSheet("color: white; background: transparent;")
            self._lbl_sub.setStyleSheet("color: rgba(255,255,255,0.75); background: transparent;")
        else:
            style = """
                QPushButton {
                    background-color: white;
                    border-radius: 12px;
                    border: 1.5px solid rgba(0,77,77,0.15);
                }
                QPushButton:hover { background-color: #F0FFF8; }
            """
            self._lbl_main.setStyleSheet(f"color: {COLOR_TEXT}; background: transparent;")
            self._lbl_sub.setStyleSheet(f"color: {COLOR_MUTED}; background: transparent;")
        self.setStyleSheet(style)

    def setChecked(self, checked: bool):
        super().setChecked(checked)
        self._apply_style(selected=checked)


# =====================================================================
# LỚP 4: GOALBUTTON
# =====================================================================
class GoalButton(QPushButton):
    COLORS = {
        "lose":     ("#FF7043", "#E64A19"),
        "maintain": ("#78909C", "#546E7A"),
        "gain":     ("#66BB6A", "#388E3C"),
    }

    def __init__(self, goal_key: str, label: str, parent=None):
        super().__init__(label, parent)
        self._key = goal_key
        self.setFixedHeight(46)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)
        self._apply_style(False)

    def _apply_style(self, selected: bool):
        base, dark = self.COLORS[self._key]
        font = QFont("Roboto")
        font.setPixelSize(22)
        font.setWeight(QFont.Weight.Bold)
        self.setFont(font)
        if selected:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                        stop:0 {base}, stop:1 {dark});
                    border-radius: 22px; border: none; color: white;
                }}
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #E8ECF0;
                    border-radius: 22px;
                    border: 1.5px solid #C8D0D8;
                    color: #708090;
                    font-weight: 700;
                }
                QPushButton:hover { background-color: #D8E0E8; }
            """)

    def setChecked(self, checked: bool):
        super().setChecked(checked)
        self._apply_style(selected=checked)


# =====================================================================
# LỚP CHÍNH: PAGEUSERPROFILE
# =====================================================================
class PageUserProfile(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1240, 640)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
            PageUserProfile {
                background-color: white;
                border: 2px solid rgba(0, 77, 77, 0.25);
                border-radius: 24px;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setOffset(0, 3)
        shadow.setColor(QColor(150, 150, 150, 180))
        self.setGraphicsEffect(shadow)

        main = QVBoxLayout(self)
        main.setContentsMargins(6, 6, 6, 6)
        main.setSpacing(0)

        self._build_banner(main)

        body = QWidget()
        body.setStyleSheet("background: transparent;")
        body_lay = QHBoxLayout(body)
        body_lay.setContentsMargins(6, 6, 6, 6)
        body_lay.setSpacing(12)

        self._build_left(body_lay)
        self._build_right(body_lay)

        main.addWidget(body, 1)

    # ================================================================
    # BANNER
    # ================================================================
    def _build_banner(self, parent_lay):
        banner = QFrame()
        banner.setFixedHeight(64)
        banner.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        c0  = COLOR_BANNER
        c80 = QColor(c0).darker(109).name()
        c100= QColor(c0).darker(131).name()

        banner.setStyleSheet(f"""
            QFrame {{
                background-color: qlineargradient(
                    x1:0,y1:0.2,x2:1,y2:1,
                    stop:0 {c0}, stop:0.8 {c80}, stop:1.0 {c100}
                );
                border-radius: 18px; border: none;
            }}
        """)

        sh = QGraphicsDropShadowEffect()
        sh.setBlurRadius(6)
        sh.setOffset(0, 2)
        sh.setColor(QColor(0, 0, 0, 160))
        banner.setGraphicsEffect(sh)

        b_lay = QHBoxLayout(banner)
        b_lay.setContentsMargins(16, 0, 20, 0)

        # ── Icon: AvatarBox nhỏ 40x40 dùng ảnh avatar mặc định ──
        icon_box = AvatarBox(size=40)
        b_lay.addWidget(icon_box, alignment=Qt.AlignmentFlag.AlignVCenter)
        b_lay.addSpacing(10)

        # ── 2 dòng chữ ──
        name_col = QVBoxLayout()
        name_col.setSpacing(2)
        name_col.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        lbl_t = QLabel("Hồ sơ người dùng")
        ft = QFont("Roboto")
        ft.setPixelSize(20)          # +2px so với trước (18→20)
        ft.setWeight(QFont.Weight.Bold)
        lbl_t.setFont(ft)
        lbl_t.setStyleSheet("color: white; border: none; background: transparent;")

        # Shadow chữ tiêu đề
        sh_txt = QGraphicsDropShadowEffect()
        sh_txt.setBlurRadius(6)
        sh_txt.setOffset(1, 1)
        sh_txt.setColor(QColor(0, 0, 0, 120))
        lbl_t.setGraphicsEffect(sh_txt)

        lbl_s = QLabel("Quản lý thông tin cá nhân và chỉ số sức khỏe")
        fs = QFont("Roboto")
        fs.setPixelSize(13)          # +1px
        lbl_s.setFont(fs)
        lbl_s.setStyleSheet("color: rgba(255,255,255,0.85); border: none; background: transparent;")

        name_col.addWidget(lbl_t)
        name_col.addWidget(lbl_s)

        b_lay.addLayout(name_col)
        b_lay.addStretch()

        parent_lay.addWidget(banner)
        parent_lay.addSpacing(6)

    # ================================================================
    # CỘT TRÁI
    # ================================================================
    def _build_left(self, parent_lay):
        left = QFrame()
        left.setFixedWidth(240)
        left.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        left.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_CARD_BG};
                border-radius: 18px;
                border: 1.5px solid {COLOR_BORDER};
            }}
            QLabel {{ border: none; background: transparent; }}
        """)

        lay = QVBoxLayout(left)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(8)
        lay.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.avatar = AvatarBox(size=180)
        lay.addWidget(self.avatar, alignment=Qt.AlignmentFlag.AlignHCenter)
        lay.addSpacing(8)

        self.lbl_name = QLabel("Chưa đăng nhập")
        fn = QFont("Roboto")
        fn.setPixelSize(15)
        fn.setWeight(QFont.Weight.Bold)
        self.lbl_name.setFont(fn)
        self.lbl_name.setStyleSheet(f"color: {COLOR_TEAL};")
        self.lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_name.setWordWrap(True)
        lay.addWidget(self.lbl_name)

        self.lbl_email = QLabel("–")
        fe = QFont("Roboto")
        fe.setPixelSize(11)
        self.lbl_email.setFont(fe)
        self.lbl_email.setStyleSheet(f"color: {COLOR_MUTED};")
        self.lbl_email.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.lbl_email)

        lay.addSpacing(10)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background: rgba(0,77,77,0.12); border: none;")
        sep.setFixedHeight(1)
        lay.addWidget(sep)
        lay.addSpacing(10)

        self.btn_google = QPushButton("  Đăng nhập với Google")
        self.btn_google.setFixedHeight(40)
        fg = QFont("Roboto")
        fg.setPixelSize(12)
        self.btn_google.setFont(fg)
        self.btn_google.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_google.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #3C4043;
                border: 1.5px solid #DADCE0;
                border-radius: 20px;
                padding: 0 12px;
            }
            QPushButton:hover  { background-color: #F8F9FA; border-color: #3EE28C; }
            QPushButton:pressed{ background-color: #E8F5E9; }
        """)
        self.btn_google.clicked.connect(self._on_google_login)
        lay.addWidget(self.btn_google)

        lbl_note = QLabel("Dữ liệu của bạn được bảo mật\nvà không chia sẻ với bên thứ ba")
        fnote = QFont("Roboto")
        fnote.setPixelSize(10)
        lbl_note.setFont(fnote)
        lbl_note.setStyleSheet(f"color: {COLOR_MUTED};")
        lbl_note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_note.setWordWrap(True)
        lay.addWidget(lbl_note)

        lay.addStretch()

        self.btn_logout = QPushButton("Đăng xuất")
        self.btn_logout.setFixedHeight(34)
        self.btn_logout.setFont(QFont("Roboto", 10))
        self.btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_logout.setStyleSheet("""
            QPushButton {
                background: transparent; color: #E57373;
                border: 1px solid #E57373; border-radius: 17px;
            }
            QPushButton:hover { background: #FFEBEE; }
        """)
        self.btn_logout.setVisible(False)
        self.btn_logout.clicked.connect(self._on_logout)
        lay.addWidget(self.btn_logout)

        parent_lay.addWidget(left)

    # ================================================================
    # CỘT PHẢI — trống, sẽ xây dần
    # ================================================================
    def _build_right(self, parent_lay):
        right = QFrame()
        right.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        right.setStyleSheet("""
            QFrame {
                background: transparent;
                border: 2px solid rgba(0, 77, 77, 0.15);
                border-radius: 18px;
            }
        """)
        right.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        lay = QVBoxLayout(right)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(10)

        lay.addStretch()

        parent_lay.addWidget(right, 1)

    # ================================================================
    # SLOTS
    # ================================================================
    def _on_google_login(self):
        print("[INFO] Google OAuth chưa được tích hợp.")

    def _on_logout(self):
        self.avatar.reset_default()
        self.lbl_name.setText("Chưa đăng nhập")
        self.lbl_email.setText("–")
        self.btn_google.setVisible(True)
        self.btn_logout.setVisible(False)

    # ================================================================
    # API CÔNG KHAI
    # ================================================================
    def load_profile(self, user_data: dict):
        self.lbl_name.setText(user_data.get("display_name", "Người dùng"))
        self.lbl_email.setText(user_data.get("email", "–"))
        if user_data.get("avatar_pixmap"):
            self.avatar.set_pixmap(user_data["avatar_pixmap"])
        self.btn_google.setVisible(False)
        self.btn_logout.setVisible(True)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = PageUserProfile()
    w.show()
    sys.exit(app.exec())