import os
from PySide6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel,
                               QWidget, QGraphicsDropShadowEffect, QPushButton,
                               QLineEdit, QSizePolicy, QButtonGroup)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import (QFont, QColor, QPixmap, QPainter, QPainterPath,
                           QBrush, QPen, QLinearGradient, QIcon)

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
        body_lay.setContentsMargins(2 , 2 , 2 , 2)
        body_lay.setSpacing(10)

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

        c0   = COLOR_BANNER
        c80  = QColor(c0).darker(109).name()
        c100 = QColor(c0).darker(131).name()

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
        b_lay.setSpacing(12)

        # ── Icon 50x50 ──
        icon_box = AvatarBox(size=50)
        b_lay.addWidget(icon_box, alignment=Qt.AlignmentFlag.AlignVCenter)

        # ── Chữ "Hồ sơ người dùng" — ShadowLabel 25px Bold, canh giữa dọc icon ──
        class ShadowLabel(QLabel):
            def paintEvent(self, event):
                p = QPainter(self)
                p.setRenderHint(QPainter.RenderHint.Antialiasing)
                p.setFont(self.font())
                p.setPen(QColor(0, 0, 0, 130))
                p.drawText(self.rect().translated(0, 2),
                           Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                           self.text())
                p.setPen(QColor("white"))
                p.drawText(self.rect(),
                           Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                           self.text())

        lbl_t = ShadowLabel("Hồ sơ người dùng")
        ft = QFont("Roboto")
        ft.setPixelSize(25)
        ft.setWeight(QFont.Weight.Bold)
        lbl_t.setFont(ft)
        lbl_t.setStyleSheet("border: none; background: transparent;")

        b_lay.addWidget(lbl_t, alignment=Qt.AlignmentFlag.AlignVCenter)
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
        fn.setPixelSize(18)
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
        self.btn_google.setFixedHeight(45)
        fg = QFont("Roboto")
        fg.setPixelSize(14)
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
    # CỘT PHẢI — đã xây lại
    # ================================================================
    def _build_right(self, parent_lay):
        right = QFrame()
        right.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        right.setFixedSize(950, 550)
        right.setStyleSheet("""
            QFrame {
                background: transparent;
                border: 2px solid rgba(0, 77, 77, 0.15);
                border-radius: 18px;
            }
        """)
        # Cho phép QFrame nhận focus khi click vào vùng trống
        # → kéo focus ra khỏi QLineEdit → border xanh tự tắt
        right.setFocusPolicy(Qt.FocusPolicy.ClickFocus)


        # ── [BOX 1] HỌ VÀ TÊN — tọa độ tự do ──
        lbl_hoten = QLabel("HỌ VÀ TÊN CỦA BẠN", right)
        #NEW UPDATE FONT
        f_lbl = QFont("Roboto")
        f_lbl.setPixelSize(13)
        f_lbl.setWeight(QFont.Weight.Bold)
        f_lbl.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 2)
        lbl_hoten.setFont(f_lbl)

        lbl_hoten.setStyleSheet("color: #3A4A5A; background: transparent; border: none;")
        lbl_hoten.move(18, 16)
        lbl_hoten.adjustSize()

        self.input_name = QLineEdit(right)
        self.input_name.setPlaceholderText("Đăng nhập Google để đặt tên...")
        self.input_name.setGeometry(16, 40, 918, 44)  # x, y, w, h
        self.input_name.setEnabled(False)
        self.input_name.setFont(QFont("Roboto", 16))
        self.input_name.setStyleSheet("""
            QLineEdit {
                background-color: #F0F4F8;
                color: #8A9BAC;
                border-radius: 22px;
                border: 1.5px solid #C8D0D8;
                padding: 0 18px;
            }
            QLineEdit:enabled {
                background-color: white;
                color: #1A2A3A;
                border: 1.5px solid rgba(0,77,77,0.25);
            }
            QLineEdit:enabled:focus {
                border: 1.5px solid #3EE28C;
            }
        """)

        # -- [ROW 2.1] TUỔI -----------------------------------------------------------------------
        # QLabel đặt tọa độ tuyệt đối bằng .move(x, y) — không dùng layout
        # y=94: bắt đầu từ input_name kết thúc tại y=84 (40+44), cách 10px → 94
        lbl_age = QLabel("⌚ TUỔI", right)
        f_lbl2 = QFont("Roboto")
        f_lbl2.setPixelSize(13)
        f_lbl2.setWeight(QFont.Weight.Bold)
        lbl_age.setFont(f_lbl2)
        lbl_age.setStyleSheet("color: #3A4A5A; background: transparent; border: none;")
        lbl_age.move(16, 94)
        lbl_age.adjustSize()  # tự co giãn theo nội dung chữ, tránh bị cắt

        # Label GIỚI TÍNH — cùng hàng y=94 với TUỔI, đặt sau input_age (x=16+160+24=200)
        lbl_gender = QLabel("GIỚI TÍNH", right)
        lbl_gender.setFont(f_lbl2)  # dùng chung font với TUỔI cho đồng bộ
        lbl_gender.setStyleSheet("color: #3A4A5A; background: transparent; border: none;")
        lbl_gender.move(200, 94)
        lbl_gender.adjustSize()

        # QLineEdit: ô nhập tuổi — setGeometry(x, y, w, h) đặt vị trí + kích thước 1 lần
        self.input_age = QLineEdit(right)
        self.input_age.setPlaceholderText("VD: 22")
        self.input_age.setGeometry(16, 114, 160, 44)  # cùng hàng y với nút giới tính
        f_age = QFont("Roboto")
        f_age.setPixelSize(15)
        self.input_age.setFont(f_age)
        self.input_age.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: #1A2A3A;
                border-radius: 12px;
                border: 1.5px solid rgba(0,77,77,0.25);
                padding: 0 14px;
            }
            QLineEdit:focus    { border: 1.5px solid #3EE28C; }
            QLineEdit:!focus   { border: 1.5px solid rgba(0,77,77,0.25); }
        """)

        # -- [ROW 2.2] GIỚI TÍNH ------------------------------------------------------------------
        # Cơ chế: 2 QPushButton checkable — khi 1 ON thì hàm _update ép cái kia OFF
        # Dùng setIcon(QPixmap.scaled()) thay vì QIcon trực tiếp để ép đúng kích thước
        # dù PNG gốc lệch pixel do bevel/shadow từ PPTX export

        _ASSET = os.path.join("assets", "fooderai-userpage")

        BTN_W = 92
        BTN_H = int(BTN_W / 1.77)# CHỈNH TẠI ĐÂY nếu bất ổn — tỉ lệ 658:372 = 1.77:1
        # Hàm scale ảnh về đúng BTN_W x BTN_H — tránh lệch do PNG gốc khác pixel

        def _make_icon(filename):
            pix = QPixmap(os.path.join(_ASSET, filename)).scaled(
                BTN_W, BTN_H,
                Qt.AspectRatioMode.KeepAspectRatio,  # ép đúng kích thước, bỏ qua tỉ lệ
                Qt.TransformationMode.SmoothTransformation  # scale mượt, không bị răng cưa
            )
            return QIcon(pix)

        # Nút Nam — x=200 (sau input_age x=16+160+24=200), y=114 (cùng hàng input)
        # new change: nút nam và nữ có thể giảm xuống là x=196, y=110
        self.btn_male = QPushButton(right)
        self.btn_male.setGeometry(196, 110, BTN_W, BTN_H)
        self.btn_male.setCheckable(True)  # giữ trạng thái ON/OFF sau khi click
        self.btn_male.setStyleSheet("border: none; background: transparent;")
        self.btn_male.setCursor(Qt.CursorShape.PointingHandCursor)

        # Nút Nữ — x = 200 + BTN_W = cách nút Nam 0px (cũ)
        # new change: nút nam và nữ có thể giảm xuống là 196, 110
        self.btn_female = QPushButton(right)
        self.btn_female.setGeometry(196 + BTN_W, 110, BTN_W, BTN_H)
        self.btn_female.setCheckable(True)
        self.btn_female.setStyleSheet("border: none; background: transparent;")
        self.btn_female.setCursor(Qt.CursorShape.PointingHandCursor)

        # iconSize phải khớp BTN_W x BTN_H để Qt không thêm padding trắng
        self.btn_male.setIconSize(QSize(BTN_W, BTN_H))
        self.btn_female.setIconSize(QSize(BTN_W, BTN_H))

        def _update_gender():
            if self.btn_male.isChecked():
                # Nam ON → ảnh sáng, ép Nữ tắt → ảnh tối
                self.btn_male.setIcon(_make_icon("fdai-male-on.png"))
                self.btn_female.setIcon(_make_icon("fdai-female-off.png"))
                self.btn_female.setChecked(False)
            else:
                # Bấm Nam lần 2 (bỏ chọn) → trả về ảnh off
                self.btn_male.setIcon(_make_icon("fdai-male-off.png"))

        def _update_female():
            if self.btn_female.isChecked():
                # Nữ ON → ảnh sáng, ép Nam tắt → ảnh tối
                self.btn_female.setIcon(_make_icon("fdai-female-on.png"))
                self.btn_male.setIcon(_make_icon("fdai-male-off.png"))
                self.btn_male.setChecked(False)
            else:
                # Bấm Nữ lần 2 (bỏ chọn) → trả về ảnh off
                self.btn_female.setIcon(_make_icon("fdai-female-off.png"))

        # Mặc định khi mở app: Nam ON, Nữ OFF
        self.btn_male.setChecked(True)
        self.btn_male.setIcon(_make_icon("fdai-male-on.png"))
        self.btn_female.setIcon(_make_icon("fdai-female-off.png"))

        # clicked.connect: Qt tự gọi hàm mỗi khi nút được bấm
        self.btn_male.clicked.connect(_update_gender)
        self.btn_female.clicked.connect(_update_female)

        # -- [ROW 3] CHIỀU CAO + CÂN NẶNG --------------------------------------------------------
        # Cùng cấu trúc ROW 2.1: label trên, input dưới, tọa độ tuyệt đối
        # y=214: ROW 2 kết thúc tại y=114+90=204, cách 10px → 214
        # -- Chiều cao --
        lbl_height = QLabel("📏 CHIỀU CAO (CM)", right)
        lbl_height.setFont(f_lbl2)  # dùng chung font Bold 13px
        lbl_height.setStyleSheet("color: #3A4A5A; background: transparent; border: none;")
        lbl_height.move(16, 180) #<=== CHỈNH TẠI ĐÂY
        lbl_height.adjustSize()

        self.input_height = QLineEdit(right)
        self.input_height.setPlaceholderText("VD: 170")
        self.input_height.setGeometry(16, 200, 160, 44) #<=== CHỈNH TẠI ĐÂY
        self.input_height.setFont(f_age)  # dùng chung font 15px với ô tuổi
        self.input_height.setStyleSheet("""
                    QLineEdit {
                        background-color: white;
                        color: #1A2A3A;
                        border-radius: 12px;
                        border: 1.5px solid rgba(0,77,77,0.25);
                        padding: 0 14px;
                    }
                    QLineEdit:focus  { border: 1.5px solid #3EE28C; }
                    QLineEdit:!focus { border: 1.5px solid rgba(0,77,77,0.25); }
                """)

        # -- Cân nặng -- cách chiều cao 16px (x = 16+160+16 = 192)
        lbl_weight = QLabel("⚖ CÂN NẶNG (KG)", right)
        lbl_weight.setFont(f_lbl2)
        lbl_weight.setStyleSheet("color: #3A4A5A; background: transparent; border: none;")
        lbl_weight.move(200, 180) #<=== CHỈNH TẠI ĐÂY
        lbl_weight.adjustSize()

        self.input_weight = QLineEdit(right)
        self.input_weight.setPlaceholderText("VD: 60")
        self.input_weight.setGeometry(200, 200, 177, 44) #<=== CHỈNH TẠI ĐÂY
        self.input_weight.setFont(f_age)
        self.input_weight.setStyleSheet(self.input_height.styleSheet())  # dùng chung style

        # -- [ROW 4] MỤC TIÊU SỨC KHỎE ----------------------------------------------------------
        # 3 nút exclusive: chọn 1 thì 2 cái kia OFF — cơ chế giống giới tính
        # y=288: input_height/weight kết thúc y=234+44=278, cách 10px → 288

        lbl_goal = QLabel("🎯 MỤC TIÊU SỨC KHỎE", right)
        lbl_goal.setFont(f_lbl2)
        lbl_goal.setStyleSheet("color: #3A4A5A; background: transparent; border: none;")
        lbl_goal.move(16, 260)
        lbl_goal.adjustSize()

        # Hàm tạo style cho nút mục tiêu — selected: màu riêng, unselected: xám (và tăng đậm phông)
        #CHỖ CHỈNH SỬA SẼ NẰM Ở ĐÂY
        def _goal_style(color: str, selected: bool) -> str:
            if selected:
                return f"""QPushButton {{
                           background-color: {color};
                           border-radius: 18px; border: none;
                           color: white; font-weight: 750; font-size: 18px;
                       }}"""
            return """QPushButton {
                       background-color: #E8ECF0;
                       border-radius: 18px;
                       border: 1.5px solid #C8D0D8;
                       color: #708090; font-weight: 700; font-size: 16px;
                   }
                   QPushButton:hover { background-color: #D8E0E8; }"""

        # 3 nút: GIẢM CÂN / DUY TRÌ / TĂNG CÂN — đều dùng màu cam khi selected
        # Rộng mỗi nút: 120px, cao 40px, cách nhau 8px
        # Tổng chiều ngang: 16 + (110+8)×3 - 8 = 362px (nằm trong giới hạn cột trái 360px)
        # GOAL_Y=280: input_height/weight kết thúc y=200+44=244, cách 36px → 280
        GOAL_W, GOAL_H = 117, 40
        GOAL_Y = 280

        self.btn_lose = QPushButton("GIẢM CÂN", right)
        self.btn_maintain = QPushButton("DUY TRÌ", right)
        self.btn_gain = QPushButton("TĂNG CÂN", right)

        goals = [
            (self.btn_lose, "#FF7043", 16),
            (self.btn_maintain, "#FF7043", 16 + GOAL_W + 7),
            (self.btn_gain, "#FF7043", 16 + (GOAL_W + 7) * 2),
        ]

        for btn, color, x in goals:
            btn.setGeometry(x, GOAL_Y, GOAL_W, GOAL_H)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFont(f_lbl2)

        # Mặc định: GIẢM CÂN được chọn
        self.btn_lose.setChecked(True)

        def _update_goal(selected_btn, color):
            for btn, c, _ in goals:
                btn.setStyleSheet(_goal_style(c, btn is selected_btn))
                btn.setChecked(btn is selected_btn)

        # Khởi tạo style ban đầu
        _update_goal(self.btn_lose, "#FF7043")

        self.btn_lose.clicked.connect(lambda: _update_goal(self.btn_lose, "#FF7043"))
        self.btn_maintain.clicked.connect(lambda: _update_goal(self.btn_maintain, "#78909C"))
        self.btn_gain.clicked.connect(lambda: _update_goal(self.btn_gain, "#66BB6A"))

        # -- [ROW 5] MỨC ĐỘ VẬN ĐỘNG + NÚT LƯU ------------------------------------------------
        # TƯ DUY: Cột phải chia 2 vùng theo trục X:
        # - x=0→459: cột form (tuổi, giới tính, chiều cao, cân nặng, mục tiêu)
        # - x=460→934: cột vận động (5 nút xếp dọc liên tục)
        # Nút lưu nằm dưới cùng, full width — là điểm kết thúc hành trình nhập liệu

        ACT_X     = 430  # x bắt đầu cột vận động — ranh giới chia đôi khung right  # CHỈNH TẠI ĐÂY
        ACT_Y     = 114  # y bắt đầu — cùng hàng ROW 2 (tuổi/giới tính)             # CHỈNH TẠI ĐÂY (KHÔNG ĐỘNG)
        ACT_W     = 504  # rộng = 950(frame) - 430(ACT_X) - 16(margin phải)          # CHỈNH TẠI ĐÂY (KHÔNG ĐỘNG)
        BTN_ACT_H = 50   # cao mỗi nút — đủ chứa 2 dòng chữ (18px + 11px + padding) # CHỈNH TẠI ĐÂY
        GAP       = 6    # khoảng cách giữa các nút theo trục Y                      # CHỈNH TẠI ĐÂY

        # Label tiêu đề cột vận động — y=94 cùng hàng label TUỔI và GIỚI TÍNH
        # Dùng f_lbl2 (Bold 13px) đồng bộ toàn bộ label nhãn trong trang
        lbl_act = QLabel("🏃 MỨC ĐỘ VẬN ĐỘNG HÀNG TUẦN", right)
        lbl_act.setFont(f_lbl2)
        lbl_act.setStyleSheet("color: #3A4A5A; background: transparent; border: none;")
        lbl_act.move(ACT_X, 94)  # CHỈNH TẠI ĐÂY
        lbl_act.adjustSize()     # tự co theo chữ, không bị cắt

        # Dữ liệu 5 mức vận động dạng tuple (tên, mô tả, hệ_số_TDEE)
        # Hệ số TDEE (Total Daily Energy Expenditure) là nhân tố khoa học dinh dưỡng:
        # TDEE = BMR × hệ_số — càng vận động nhiều, cơ thể đốt calo càng cao
        acts = [
            ("Ít vận động", "Làm việc văn phòng", 1.2),
            ("Nhẹ nhàng",   "1-2 ngày/tuần",      1.375),
            ("Vừa phải",    "3-5 ngày/tuần",       1.55),
            ("Năng động",   "6-7 ngày/tuần",       1.725),
            ("Rất cao",     "Vận động viên",        1.9),
        ]
        self._activity_factors = {}  # dict {index → hệ_số} — _on_save dùng để tính TDEE
        self._act_buttons      = []  # list (btn, lbl_main, lbl_sub) — loop update style

        def _act_style(selected: bool) -> str:
            # TƯ DUY: stylesheet trả về dạng string → gán qua setStyleSheet()
            # selected=True : nền xanh lá #00C950, viền mint #00DD58 2px solid
            # selected=False: nền trắng thuần, viền xanh rêu nhạt rgba
            if selected:
                return """QPushButton {
                    background-color: #00C950;
                    border-radius: 12px;
                    border: 2px solid #00DD58;
                }"""
            return """QPushButton {
                background-color: white;
                border-radius: 12px;
                border: 1.5px solid rgba(0,77,77,0.15);
            }
            QPushButton:hover { background-color: #F0FFF8; }"""

        for i, (name, desc, factor) in enumerate(acts):
            # TƯ DUY: enumerate() cho index i → tính y tuyệt đối = ACT_Y + i*(H+GAP)
            # Mỗi vòng lặp tạo 1 nút + 2 QLabel con bên trong nút (parent=btn)
            # QLabel con dùng .move() tọa độ relative so với nút cha — không phải frame right

            btn   = QPushButton(right)
            btn_y = ACT_Y + i * (BTN_ACT_H + GAP)  # y tăng đều mỗi nút  # CHỈNH GAP TẠI ĐÂY
            btn.setGeometry(ACT_X, btn_y, ACT_W, BTN_ACT_H)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(_act_style(False))

            # Label chính — Roboto Bold 18px, đặt trong nút (parent=btn), tọa độ relative
            lbl_main = QLabel(name, btn)
            f_act_main = QFont("Roboto")
            f_act_main.setPixelSize(18)
            f_act_main.setWeight(QFont.Weight.Bold)
            lbl_main.setFont(f_act_main)
            lbl_main.setStyleSheet("background: transparent; border: none; color: #1A2A3A;")
            lbl_main.move(16, 8)   # padding trái 16px, cách top nút 8px
            lbl_main.adjustSize()

            # Label phụ — Roboto 11px, nằm dưới label chính 22px
            lbl_sub = QLabel(desc, btn)
            f_act_sub = QFont("Roboto")
            f_act_sub.setPixelSize(11)
            lbl_sub.setFont(f_act_sub)
            lbl_sub.setStyleSheet("background: transparent; border: none; color: #8A9BAC;")
            lbl_sub.move(16, 30)   # 8(top) + 18(font) ≈ 26, làm tròn 30px
            lbl_sub.adjustSize()

            self._activity_factors[i] = factor
            self._act_buttons.append((btn, lbl_main, lbl_sub))

        def _update_act(sel_idx: int):
            # TƯ DUY: loop toàn bộ nút, so sánh index → set style đúng/sai
            # Màu chữ cũng đổi: trắng khi ON (nền xanh), tối/xám khi OFF (nền trắng)
            for idx, (btn, lbl_m, lbl_s) in enumerate(self._act_buttons):
                selected = (idx == sel_idx)
                btn.setChecked(selected)
                btn.setStyleSheet(_act_style(selected))
                lbl_m.setStyleSheet(f"background: transparent; border: none; "
                                    f"color: {'white' if selected else '#1A2A3A'};")
                lbl_s.setStyleSheet(f"background: transparent; border: none; "
                                    f"color: {'rgba(255,255,255,0.8)' if selected else '#8A9BAC'};")

        _update_act(0)  # mặc định: "Ít vận động" (index 0) được chọn khi mở app

        # clicked.connect dùng lambda với idx=i để capture đúng giá trị i tại thời điểm loop
        # Nếu viết lambda: _update_act(i) mà không có idx=i → closure bug: tất cả dùng i cuối
        for i, (btn, _, __) in enumerate(self._act_buttons):
            btn.clicked.connect(lambda _, idx=i: _update_act(idx))

        # -- NÚT LƯU HỒ SƠ --------------------------------------------------------------------
        # TƯ DUY: SaveButton là local class override paintEvent để vẽ chữ thủ công
        # Lý do: Qt chỉ cho 1 setGraphicsEffect per widget → không stack shadow chữ + shadow nút
        # Giải pháp: shadow nút dùng setGraphicsEffect(sh_btn), shadow chữ vẽ bằng QPainter

        SAVE_Y = ACT_Y + 5 * (BTN_ACT_H + GAP) + 50  # dưới nút cuối + 50px margin  # CHỈNH TẠI ĐÂY

        class SaveButton(QPushButton):
            def paintEvent(self, event):
                super().paintEvent(event)  # Qt vẽ nền gradient + border trước
                p = QPainter(self)
                p.setRenderHint(QPainter.RenderHint.Antialiasing)
                p.setFont(self.font())
                rect = self.rect()
                text = self.text()
                # Shadow trung tâm: vẽ chữ đen mờ lệch 4 hướng chéo 1px → tạo halo đều
                p.setPen(QColor(0, 0, 0, 80))
                for dx, dy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
                    p.drawText(rect.translated(dx, dy), Qt.AlignmentFlag.AlignCenter, text)
                # Shadow 90° xuống 3px: đổ bóng xuống dưới tạo chiều sâu
                p.setPen(QColor(0, 80, 30, 130))
                p.drawText(rect.translated(0, 3), Qt.AlignmentFlag.AlignCenter, text)
                # Chữ thật trắng vẽ đè lên cùng — luôn nằm trên cùng
                p.setPen(QColor("white"))
                p.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)

        self.btn_save = SaveButton("Lưu hồ sơ & Bắt đầu tính toán", right)
        self.btn_save.setGeometry(16, SAVE_Y, 918, 52)  # full width khung, cao 52px  # CHỈNH TẠI ĐÂY
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)

        f_save = QFont("Roboto")
        f_save.setPixelSize(20)
        f_save.setWeight(QFont.Weight.Black)                                  # weight 900
        f_save.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 3)        # expand chữ 3px
        self.btn_save.setFont(f_save)

        self.btn_save.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0.0 #3EE28C,
                    stop:0.7 #3BD585,
                    stop:1.0 #2B9E61);
                border-radius: 26px;
                border: 3px solid #00E676;
                color: white;
            }
            QPushButton:hover   { background: #3EE28C; }
            QPushButton:pressed { background: #2B9E61; }
        """)

        # Shadow nút: offset(0,2) = 90° xuống, blur=8 → phát sáng xanh lá dưới nút
        sh_btn = QGraphicsDropShadowEffect()
        sh_btn.setBlurRadius(8)
        sh_btn.setOffset(0, 2)
        sh_btn.setColor(QColor(0, 180, 80, 140))
        self.btn_save.setGraphicsEffect(sh_btn)  # chỉ 1 effect — sh_txt đã bỏ

        self.btn_save.clicked.connect(self._on_save)

        parent_lay.addWidget(right, 1)

    def _on_google_login(self):
        print("[INFO] Google OAuth chưa được tích hợp.")

    def _on_logout(self):
        self.avatar.reset_default()
        self.lbl_name.setText("Chưa đăng nhập")
        self.lbl_email.setText("–")
        self.btn_google.setVisible(True)
        self.btn_logout.setVisible(False)

    def _on_save(self):
        # Đọc giá trị form — sau này kết nối DB/Firebase tại đây
        print("[SAVE] Họ tên:", self.input_name.text())
        print("[SAVE] Tuổi:", self.input_age.text())
        print("[SAVE] Chiều cao:", self.input_height.text())
        print("[SAVE] Cân nặng:", self.input_weight.text())

