import os
from PySide6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel,
                               QWidget, QGraphicsDropShadowEffect, QPushButton,
                               QLineEdit, QSizePolicy, QButtonGroup)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QPixmap, QPainter, QPainterPath, QBrush, QPen, QLinearGradient

# =====================================================================
# HẰNG SỐ MÀU — PALETTE TRANG HỒ SƠ
# =====================================================================
COLOR_BANNER  = "#3EE28C"   # xanh lá banner — đồng bộ các trang
COLOR_TEAL    = "#266066"   # tiêu đề chính
COLOR_TEXT    = "#1A2A3A"   # chữ tối
COLOR_MUTED   = "#8A9BAC"   # chữ nhạt placeholder
COLOR_BORDER  = "rgba(0, 77, 77, 0.18)"
COLOR_CARD_BG = "#F7FAFA"   # nền card

# Đường dẫn ảnh avatar mặc định khi chưa đăng nhập
_AVT_DEFAULT = os.path.join("assets", "fooderai-userpage", "fdai-userpage-unsignedin.png")


# =====================================================================
# HÀM TIỆN ÍCH: tạo gradient 45° tối dần 16% từ màu gốc
# =====================================================================
def _gradient_style(base_hex: str, radius: int = 12) -> str:
    """
    Trả về stylesheet gradient chéo 45° từ màu gốc (100%) → tối hơn 16%.

    darker(116) trong Qt = tối hơn 16% so với màu gốc.
    x1:0,y1:0 → x2:1,y2:1 = hướng chéo 45° từ trên-trái xuống dưới-phải.
    """
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
# LỚP 1: AVATARBOX — Hình vuông bo tròn 2/3 cạnh chứa ảnh avatar
#
# Theo yêu cầu: "bo tròn với bán kính mỗi cạnh chiếm 2 phần 3 của cạnh gốc"
# → border-radius = size * 2/3 ÷ 2 = size / 3
# Ví dụ size=180: border-radius = 60px
# =====================================================================
class AvatarBox(QLabel):
    """
    Hộp vuông 180x180 hiển thị ảnh avatar, bo góc radius = size/3.

    Tại sao dùng QPainter thay vì border-radius trong stylesheet?
    - Qt stylesheet border-radius KHÔNG clip ảnh bên trong QLabel.
    - QPainter dùng QPainterPath để cắt ảnh thật sự theo hình bo tròn.
    - setClipPath() đảm bảo pixel ngoài path bị ẩn hoàn toàn.

    API công khai:
    - set_pixmap(pixmap): đặt ảnh tùy chỉnh (dùng sau Google OAuth)
    - reset_default(): trả về ảnh mặc định chưa đăng nhập
    """
    def __init__(self, size: int = 180, parent=None):
        super().__init__(parent)
        self._size   = size
        self._radius = size // 3   # = 60px cho size=180 — bo 2/3 cạnh
        self.setFixedSize(size, size)
        self._pix = None
        self.reset_default()       # nạp ảnh mặc định ngay khi khởi tạo

    def reset_default(self):
        """Nạp ảnh placeholder chưa đăng nhập từ assets."""
        if os.path.exists(_AVT_DEFAULT):
            pix = QPixmap(_AVT_DEFAULT).scaled(
                self._size, self._size,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            self._pix = pix
        else:
            self._pix = None   # fallback: vẽ hình tròn gradient xanh
        self.update()

    def set_pixmap(self, pixmap: QPixmap):
        """[GOOGLE OAUTH] Nhận ảnh profile, scale khít hộp."""
        self._pix = pixmap.scaled(
            self._size, self._size,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Path bo góc theo radius = size/3
        path = QPainterPath()
        path.addRoundedRect(2, 2, self._size - 4, self._size - 4,
                            self._radius, self._radius)
        painter.setClipPath(path)

        if self._pix:
            # Vẽ ảnh avatar (cắt theo path bo tròn)
            painter.drawPixmap(0, 0, self._pix)
        else:
            # Fallback gradient xanh nếu không có file ảnh
            grad = QLinearGradient(0, 0, self._size, self._size)
            grad.setColorAt(0.0, QColor("#3EE28C"))
            grad.setColorAt(1.0, QColor("#2ABF73"))
            painter.fillPath(path, QBrush(grad))

        # Viền nhẹ
        painter.setClipping(False)
        painter.setPen(QPen(QColor(COLOR_BANNER), 2.5))
        painter.drawRoundedRect(2, 2, self._size - 4, self._size - 4,
                                self._radius, self._radius)


# =====================================================================
# LỚP 2: GENDERBUTTON — Nút chọn giới tính có màu riêng
#
# Nam = xanh da trời (#42A5F5), Nữ = hồng (#F48FB1)
# Khi chọn: màu nổi lên, có shadow. Khi không chọn: nền xám nhạt.
# =====================================================================
class GenderButton(QPushButton):
    """
    Nút radio giới tính với màu đặc trưng:
    - Nam: gradient xanh da trời  #42A5F5 → #1E88E5
    - Nữ : gradient hồng           #F48FB1 → #E91E8C

    Hoạt động theo nhóm QButtonGroup (chọn 1 bỏ 1) — xử lý ở PageUserProfile.
    Shadow tạo cảm giác "nổi lên" khi được chọn.
    """

    # Màu cho từng giới tính (base → dark)
    COLORS = {
        "male":   ("#42A5F5", "#1E88E5"),
        "female": ("#F48FB1", "#E91E8C"),
    }

    def __init__(self, gender: str, label: str, icon: str = "", parent=None):
        """
        gender: "male" hoặc "female" — dùng để lấy màu từ COLORS
        label : chữ hiển thị trên nút ("Nam" hoặc "Nữ")
        icon  : ký tự emoji/unicode đứng trước label (tuỳ chọn)
        """
        super().__init__(f"{icon}  {label}" if icon else label, parent)
        self._gender   = gender
        self._selected = False
        self.setFixedSize(80, 44)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)   # QButtonGroup dùng checkable để quản lý exclusive
        self._shadow = QGraphicsDropShadowEffect()
        self._shadow.setBlurRadius(10)
        self._shadow.setOffset(0, 3)
        self.setGraphicsEffect(self._shadow)
        self._apply_style(selected=False)

    def _apply_style(self, selected: bool):
        """Áp dụng stylesheet tương ứng trạng thái chọn / không chọn."""
        base, dark = self.COLORS[self._gender]
        if selected:
            # Nổi lên: gradient màu đặc trưng, shadow đậm, chữ trắng đậm
            self._shadow.setColor(QColor(base).darker(120))
            self._shadow.setBlurRadius(12)
            self.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                        stop:0 {base}, stop:1 {dark});
                    border-radius: 22px;
                    border: 2px solid {QColor(base).lighter(120).name()};
                    color: white;
                    font-weight: bold;
                }}
            """)
        else:
            # Chìm xuống: xám nhạt, shadow mờ
            self._shadow.setColor(QColor(0, 0, 0, 40))
            self._shadow.setBlurRadius(4)
            self.setStyleSheet("""
                QPushButton {
                    background-color: #E8ECF0;
                    border-radius: 22px;
                    border: 1.5px solid #C8D0D8;
                    color: #8A9BAC;
                }
                QPushButton:hover { background-color: #D8E0E8; }
            """)

    def setChecked(self, checked: bool):
        """Override để đồng thời cập nhật style khi trạng thái thay đổi."""
        super().setChecked(checked)
        self._apply_style(selected=checked)


# =====================================================================
# LỚP 3: ACTIVITYBUTTON — Nút chọn mức vận động (danh sách dọc)
# =====================================================================
class ActivityButton(QPushButton):
    """
    Nút chọn mức vận động — thiết kế dạng list item dọc.
    Hiển thị 2 dòng: tên chính (đậm) + mô tả phụ (nhỏ, xám).

    Khi được chọn: gradient xanh lá đồng bộ màu app.
    Khi không chọn: nền trắng, viền nhạt.
    """
    BASE_COLOR = "#3EE28C"   # xanh lá — đồng bộ theme app

    def __init__(self, main_text: str, sub_text: str, parent=None):
        super().__init__(parent)
        self.setFixedHeight(52)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)

        # Layout 2 dòng bên trong nút
        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 4, 14, 4)
        lay.setSpacing(1)

        self._lbl_main = QLabel(main_text)
        f_main = QFont("Roboto")
        f_main.setPixelSize(13)
        f_main.setWeight(QFont.Weight.Medium)
        self._lbl_main.setFont(f_main)

        self._lbl_sub = QLabel(sub_text)
        f_sub = QFont("Roboto")
        f_sub.setPixelSize(11)
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
# LỚP 4: GOALBUTTON — Nút chọn mục tiêu (Giảm cân / Duy trì / Tăng cân)
# =====================================================================
class GoalButton(QPushButton):
    """
    Nút chọn mục tiêu sức khỏe.
    Màu riêng cho từng mục tiêu để phân biệt trực quan.
    Hoạt động exclusive qua QButtonGroup giống GenderButton.
    """
    COLORS = {
        "lose":     ("#FF7043", "#E64A19"),   # cam đỏ — giảm cân
        "maintain": ("#78909C", "#546E7A"),   # xám xanh — duy trì
        "gain":     ("#66BB6A", "#388E3C"),   # xanh lá đậm — tăng cân
    }

    def __init__(self, goal_key: str, label: str, parent=None):
        super().__init__(label, parent)
        self._key = goal_key
        self.setFixedHeight(40)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)
        self._apply_style(False)

    def _apply_style(self, selected: bool):
        base, dark = self.COLORS[self._key]
        font = QFont("Roboto")
        font.setPixelSize(13)
        font.setWeight(QFont.Weight.Bold if selected else QFont.Weight.Normal)
        self.setFont(font)
        if selected:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                        stop:0 {base}, stop:1 {dark});
                    border-radius: 20px; border: none; color: white;
                }}
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #E8ECF0;
                    border-radius: 20px;
                    border: 1.5px solid #C8D0D8;
                    color: #8A9BAC;
                }
                QPushButton:hover { background-color: #D8E0E8; }
            """)

    def setChecked(self, checked: bool):
        super().setChecked(checked)
        self._apply_style(selected=checked)


# =====================================================================
# LỚP CHÍNH: PAGEUSERPROFILE
#
# LAYOUT (theo PowerPoint):
# ┌─────────────────────────────────────────────────────────────────┐
# │  BANNER xanh lá                                                 │
# ├────────────────────┬────────────────────────────────────────────┤
# │  CỘT TRÁI (240px)  │  CỘT PHẢI                                 │
# │  • AvatarBox 180px │  • Ô nhập họ tên (disabled khi chưa login)│
# │  • "Chưa đăng nhập"│  • Tuổi | Giới tính Nam/Nữ                │
# │  • Nút Google      │  • Chiều cao (cm) | Cân nặng (kg)         │
# │  • Ghi chú bảo mật │  • Mục tiêu sức khỏe (3 nút)             │
# │                    │  • Mức vận động (5 nút dọc)               │
# │                    │  • Nút "Lưu hồ sơ & Bắt đầu tính toán"   │
# └────────────────────┴────────────────────────────────────────────┘
# =====================================================================
class PageUserProfile(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1240, 640)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
            PageUserProfile {
                background-color: white;
                border: 3px solid rgba(0, 77, 77, 0.5);
                border-radius: 24px;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(5)
        shadow.setOffset(0, 3)
        shadow.setColor(QColor(150, 150, 150, 180))
        self.setGraphicsEffect(shadow)

        main = QVBoxLayout(self)
        main.setContentsMargins(15, 10, 15, 10)
        main.setSpacing(0)

        self._build_banner(main)

        # Body 2 cột
        body = QWidget()
        body.setStyleSheet("background: transparent;")
        body_lay = QHBoxLayout(body)
        body_lay.setContentsMargins(10, 12, 10, 10)
        body_lay.setSpacing(20)

        self._build_left(body_lay)
        self._build_right(body_lay)

        main.addWidget(body, 1)

    # ================================================================
    # BANNER — đồng bộ style với page_ai.py
    # ================================================================
    def _build_banner(self, parent_lay):
        banner = QFrame()
        banner.setFixedSize(1210, 60)

        c0  = COLOR_BANNER
        c80 = QColor(c0).darker(109).name()
        c100= QColor(c0).darker(131).name()

        banner.setStyleSheet(f"""
            QFrame {{
                background-color: qlineargradient(
                    x1:0,y1:0.2,x2:1,y2:1,
                    stop:0 {c0}, stop:0.8 {c80}, stop:1.0 {c100}
                );
                border-radius: 15px; border: none;
            }}
        """)

        sh = QGraphicsDropShadowEffect()
        sh.setBlurRadius(6); sh.setOffset(0, 2)
        sh.setColor(QColor(0, 0, 0, 160))
        banner.setGraphicsEffect(sh)

        b_lay = QHBoxLayout(banner)
        b_lay.setContentsMargins(20, 0, 20, 0)

        # Icon từ assets (dùng lại icon navbar)
        icon_path = os.path.join("assets", "fooderai-blockcomponent", "fooderai-userinfo.png")
        lbl_icon = QLabel()
        lbl_icon.setFixedSize(32, 32)
        lbl_icon.setStyleSheet("border: none; background: transparent;")
        if os.path.exists(icon_path):
            lbl_icon.setPixmap(QPixmap(icon_path).scaled(
                32, 32, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation))

        # 2 dòng chữ: tiêu đề + phụ đề
        name_col = QVBoxLayout()
        name_col.setSpacing(1)
        name_col.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        lbl_t = QLabel("Hồ sơ người dùng")
        ft = QFont("Roboto"); ft.setPixelSize(18); ft.setWeight(QFont.Weight.Bold)
        lbl_t.setFont(ft)
        lbl_t.setStyleSheet("color: white; border: none; background: transparent;")

        lbl_s = QLabel("Quản lý thông tin cá nhân và chỉ số sức khỏe")
        fs = QFont("Roboto"); fs.setPixelSize(12)
        lbl_s.setFont(fs)
        lbl_s.setStyleSheet("color: rgba(255,255,255,0.8); border: none; background: transparent;")

        name_col.addWidget(lbl_t)
        name_col.addWidget(lbl_s)

        b_lay.addWidget(lbl_icon, alignment=Qt.AlignmentFlag.AlignVCenter)
        b_lay.addSpacing(8)
        b_lay.addLayout(name_col)
        b_lay.addStretch()

        parent_lay.addWidget(banner,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        parent_lay.addSpacing(8)

    # ================================================================
    # CỘT TRÁI — AvatarBox + tên + nút Google
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

        # ── AvatarBox 180x180 ──
        self.avatar = AvatarBox(size=180)
        lay.addWidget(self.avatar, alignment=Qt.AlignmentFlag.AlignHCenter)
        lay.addSpacing(8)

        # ── Tên hiển thị ──
        self.lbl_name = QLabel("Chưa đăng nhập")
        fn = QFont("Roboto"); fn.setPixelSize(15); fn.setWeight(QFont.Weight.Bold)
        self.lbl_name.setFont(fn)
        self.lbl_name.setStyleSheet(f"color: {COLOR_TEAL};")
        self.lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_name.setWordWrap(True)
        lay.addWidget(self.lbl_name)

        # ── Dấu gạch "--" khi chưa có email ──
        self.lbl_email = QLabel("–")
        fe = QFont("Roboto"); fe.setPixelSize(11)
        self.lbl_email.setFont(fe)
        self.lbl_email.setStyleSheet(f"color: {COLOR_MUTED};")
        self.lbl_email.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.lbl_email)

        lay.addSpacing(10)

        # ── Đường kẻ ngăn cách ──
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background: rgba(0,77,77,0.12); border: none;")
        sep.setFixedHeight(1)
        lay.addWidget(sep)
        lay.addSpacing(10)

        # ── Nút đăng nhập Google ──
        # [GOOGLE OAUTH SLOT] — kết nối btn_google.clicked → _on_google_login()
        # Khi tích hợp: dùng google-auth-oauthlib để lấy token + profile
        self.btn_google = QPushButton("  Đăng nhập với Google")
        self.btn_google.setFixedHeight(40)
        fg = QFont("Roboto"); fg.setPixelSize(12)
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

        # ── Ghi chú bảo mật ──
        lbl_note = QLabel("Dữ liệu của bạn được bảo mật\nvà không chia sẻ với bên thứ ba")
        fnote = QFont("Roboto"); fnote.setPixelSize(10)
        lbl_note.setFont(fnote)
        lbl_note.setStyleSheet(f"color: {COLOR_MUTED};")
        lbl_note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_note.setWordWrap(True)
        lay.addWidget(lbl_note)

        lay.addStretch()

        # ── Nút đăng xuất (ẩn mặc định) ──
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
    # CỘT PHẢI — Form nhập thông tin + các nút chọn
    # ================================================================
    def _build_right(self, parent_lay):
        right = QWidget()
        right.setStyleSheet("background: transparent;")
        right.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        lay = QVBoxLayout(right)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        # ── Họ và tên ──────────────────────────────────────────────
        lbl_hoten = QLabel("HỌ VÀ TÊN CỦA BẠN")
        f_lbl = QFont("Roboto"); f_lbl.setPixelSize(11)
        f_lbl.setWeight(QFont.Weight.Medium)
        lbl_hoten.setFont(f_lbl)
        lbl_hoten.setStyleSheet(f"color: {COLOR_MUTED};")
        lay.addWidget(lbl_hoten)

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Đăng nhập Google để đặt tên...")
        self.input_name.setFixedHeight(44)
        self.input_name.setEnabled(False)   # disable khi chưa đăng nhập
        fn_inp = QFont("Roboto"); fn_inp.setPixelSize(13)
        self.input_name.setFont(fn_inp)
        self.input_name.setStyleSheet("""
            QLineEdit {
                background-color: #F0F4F8;
                color: #8A9BAC;
                border-radius: 12px;
                border: 1.5px solid #C8D0D8;
                padding: 0 16px;
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
        lay.addWidget(self.input_name)

        # ── Hàng 1: Tuổi + Giới tính ───────────────────────────────
        row1 = QHBoxLayout()
        row1.setSpacing(16)

        # -- Tuổi --
        col_age = QVBoxLayout()
        col_age.setSpacing(4)

        lbl_age = QLabel("🕐  TUỔI")
        lbl_age.setFont(f_lbl)
        lbl_age.setStyleSheet(f"color: {COLOR_MUTED};")

        self.input_age = QLineEdit()
        self.input_age.setFixedSize(160, 44)
        self.input_age.setPlaceholderText("VD: 22")
        fi = QFont("Roboto"); fi.setPixelSize(13)
        self.input_age.setFont(fi)
        self.input_age.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: #1A2A3A;
                border-radius: 12px;
                border: 1.5px solid rgba(0,77,77,0.25);
                padding: 0 14px;
            }
            QLineEdit:focus { border: 1.5px solid #3EE28C; }
        """)

        col_age.addWidget(lbl_age)
        col_age.addWidget(self.input_age)

        # -- Giới tính --
        col_gender = QVBoxLayout()
        col_gender.setSpacing(4)

        lbl_gender = QLabel("⚧  GIỚI TÍNH")
        lbl_gender.setFont(f_lbl)
        lbl_gender.setStyleSheet(f"color: {COLOR_MUTED};")

        # GenderButton Nam + Nữ trong QButtonGroup (exclusive)
        # QButtonGroup.setExclusive(True): chỉ 1 nút được chọn tại 1 thời điểm
        gender_row = QHBoxLayout()
        gender_row.setSpacing(10)
        self.btn_male   = GenderButton("male",   "Nam", "♂")
        self.btn_female = GenderButton("female", "Nữ",  "♀")
        self._gender_group = QButtonGroup(self)
        self._gender_group.setExclusive(True)
        self._gender_group.addButton(self.btn_male,   0)
        self._gender_group.addButton(self.btn_female, 1)
        self._gender_group.idToggled.connect(self._on_gender_changed)
        gender_row.addWidget(self.btn_male)
        gender_row.addWidget(self.btn_female)
        gender_row.addStretch()

        col_gender.addWidget(lbl_gender)
        col_gender.addLayout(gender_row)

        # -- Mức vận động (nhãn) --
        col_act_lbl = QVBoxLayout()
        col_act_lbl.setSpacing(4)
        lbl_act_hd = QLabel("🏃  MỨC ĐỘ VẬN ĐỘNG HÀNG TUẦN")
        lbl_act_hd.setFont(f_lbl)
        lbl_act_hd.setStyleSheet(f"color: {COLOR_MUTED};")
        col_act_lbl.addWidget(lbl_act_hd)
        col_act_lbl.addStretch()

        row1.addLayout(col_age)
        row1.addLayout(col_gender)
        row1.addLayout(col_act_lbl)

        lay.addLayout(row1)

        # ── Hàng 2: Chiều cao + Cân nặng + Cột vận động ───────────
        row2 = QHBoxLayout()
        row2.setSpacing(16)

        # -- Chiều cao --
        col_h = QVBoxLayout(); col_h.setSpacing(4)
        lbl_h = QLabel("📏  CHIỀU CAO (CM)")
        lbl_h.setFont(f_lbl); lbl_h.setStyleSheet(f"color: {COLOR_MUTED};")
        self.input_height = QLineEdit()
        self.input_height.setFixedSize(160, 44)
        self.input_height.setPlaceholderText("VD: 170")
        self.input_height.setFont(fi)
        self.input_height.setStyleSheet(self.input_age.styleSheet())
        col_h.addWidget(lbl_h); col_h.addWidget(self.input_height)

        # -- Cân nặng --
        col_w = QVBoxLayout(); col_w.setSpacing(4)
        lbl_w = QLabel("⚖  CÂN NẶNG (KG)")
        lbl_w.setFont(f_lbl); lbl_w.setStyleSheet(f"color: {COLOR_MUTED};")
        self.input_weight = QLineEdit()
        self.input_weight.setFixedSize(160, 44)
        self.input_weight.setPlaceholderText("VD: 60")
        self.input_weight.setFont(fi)
        self.input_weight.setStyleSheet(self.input_age.styleSheet())
        col_w.addWidget(lbl_w); col_w.addWidget(self.input_weight)

        # -- Cột vận động (5 nút dọc) --
        col_act = QVBoxLayout(); col_act.setSpacing(4)

        # ActivityButton: QButtonGroup exclusive tương tự gender
        self._act_group = QButtonGroup(self)
        self._act_group.setExclusive(True)

        acts = [
            ("Ít vận động",  "Làm việc văn phòng",  1.2),
            ("Nhẹ nhàng",    "1-2 ngày/tuần",        1.375),
            ("Vừa phải",     "3-5 ngày/tuần",        1.55),
            ("Năng động",    "6-7 ngày/tuần",        1.725),
            ("Rất cao",      "Vận động viên",         1.9),
        ]
        self._activity_factors = {}   # lưu factor để dùng khi tính TDEE
        self._act_buttons = []

        for i, (name, desc, factor) in enumerate(acts):
            btn = ActivityButton(name, desc)
            self._act_group.addButton(btn, i)
            self._activity_factors[i] = factor
            col_act.addWidget(btn)
            self._act_buttons.append(btn)

        # Mặc định chọn "Ít vận động"
        self._act_buttons[0].setChecked(True)
        self._act_group.idToggled.connect(self._on_activity_changed)

        row2.addLayout(col_h)
        row2.addLayout(col_w)
        row2.addLayout(col_act, 1)   # cột vận động chiếm phần còn lại

        lay.addLayout(row2)

        # ── Mục tiêu sức khỏe ──────────────────────────────────────
        goal_section = QVBoxLayout(); goal_section.setSpacing(6)

        lbl_goal_hd = QLabel("🎯  MỤC TIÊU SỨC KHỎE")
        lbl_goal_hd.setFont(f_lbl); lbl_goal_hd.setStyleSheet(f"color: {COLOR_MUTED};")
        goal_section.addWidget(lbl_goal_hd)

        goal_row = QHBoxLayout(); goal_row.setSpacing(10)
        self.btn_lose     = GoalButton("lose",     "GIẢM CÂN")
        self.btn_maintain = GoalButton("maintain", "DUY TRÌ")
        self.btn_gain     = GoalButton("gain",     "TĂNG CÂN")

        self._goal_group = QButtonGroup(self)
        self._goal_group.setExclusive(True)
        self._goal_group.addButton(self.btn_lose,     0)
        self._goal_group.addButton(self.btn_maintain, 1)
        self._goal_group.addButton(self.btn_gain,     2)
        # Mặc định: giảm cân
        self.btn_lose.setChecked(True)

        goal_row.addWidget(self.btn_lose)
        goal_row.addWidget(self.btn_maintain)
        goal_row.addWidget(self.btn_gain)
        goal_section.addLayout(goal_row)

        lay.addLayout(goal_section)

        # ── Nút "Lưu hồ sơ & Bắt đầu tính toán" ──────────────────
        # Roboto Bold 20px, gradient xanh lá 45° tối 16%
        self.btn_save = QPushButton("Lưu hồ sơ & Bắt đầu tính toán")
        self.btn_save.setFixedHeight(52)
        fb = QFont("Roboto"); fb.setPixelSize(20); fb.setWeight(QFont.Weight.Bold)
        self.btn_save.setFont(fb)
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_save.setStyleSheet(_gradient_style(COLOR_BANNER, radius=26))
        self.btn_save.clicked.connect(self._on_save)

        # Shadow cho nút lưu
        sh_save = QGraphicsDropShadowEffect()
        sh_save.setBlurRadius(16); sh_save.setOffset(0, 4)
        sh_save.setColor(QColor(62, 226, 140, 140))
        self.btn_save.setGraphicsEffect(sh_save)

        lay.addWidget(self.btn_save)

        parent_lay.addWidget(right, 1)

    # ================================================================
    # SLOT NỘI BỘ
    # ================================================================
    def _on_gender_changed(self, btn_id: int, checked: bool):
        """QButtonGroup.idToggled: cập nhật style khi chuyển giới tính."""
        if checked:
            # Đảm bảo nút KHÔNG được chọn cũng cập nhật style
            for btn in [self.btn_male, self.btn_female]:
                btn._apply_style(btn.isChecked())

    def _on_activity_changed(self, btn_id: int, checked: bool):
        """Cập nhật style khi chuyển mức vận động."""
        if checked:
            for btn in self._act_buttons:
                btn._apply_style(btn.isChecked())

    def _on_save(self):
        """
        Đọc giá trị từ form, tính BMI/BMR/TDEE, phát signal lên main window.

        [TODO - DATABASE] Khi có DBMS:
        Thay đoạn print() bằng:
            db.save_user_profile(user_id, profile_data)
            main_window.update_dashboard(bmi, bmr, tdee, goal)

        Các trường cần lưu vào bảng USER_PROFILES:
            weight_kg, height_cm, age, gender, activity_level, goal
        Các trường TÍNH TOÁN (không cần lưu riêng, tính lại khi cần):
            bmi, bmr, tdee, daily_goal_kcal
        """
        try:
            age    = int(self.input_age.text())
            height = int(self.input_height.text())
            weight = int(self.input_weight.text())
        except ValueError:
            # Chưa nhập đủ → không làm gì (sau này thêm QMessageBox)
            return

        gender = "male" if self.btn_male.isChecked() else "female"
        act_id = self._act_group.checkedId()
        factor = self._activity_factors.get(act_id, 1.2)

        # Tính toán qua fooder_widgetBack
        from fooder_widgetBack import NutritionLogic
        bmi  = NutritionLogic.calculate_bmi(weight, height)
        bmr  = NutritionLogic.calculate_bmr(weight, height, age, gender)
        tdee = NutritionLogic.calculate_tdee(bmr, factor)

        print(f"[SAVE] BMI={bmi}, BMR={bmr}, TDEE={tdee}")
        # TODO: gọi main_window.update_stat_cards(bmi, bmr, tdee)

    def _on_google_login(self):
        """[GOOGLE OAUTH SLOT] — chừa sẵn cho tích hợp sau."""
        print("[INFO] Google OAuth chưa được tích hợp.")

    def _on_logout(self):
        """Reset toàn bộ form về trạng thái chưa đăng nhập."""
        self.avatar.reset_default()
        self.lbl_name.setText("Chưa đăng nhập")
        self.lbl_email.setText("–")
        self.input_name.setEnabled(False)
        self.input_name.clear()
        self.btn_google.setVisible(True)
        self.btn_logout.setVisible(False)

    # ================================================================
    # API CÔNG KHAI — gọi từ main window
    # ================================================================
    def load_profile(self, user_data: dict):
        """
        Nạp thông tin từ Google OAuth hoặc database vào form.

        user_data = {
            "display_name": str,
            "email":        str,
            "avatar_pixmap": QPixmap | None,
            "age":           int,
            "gender":        "male" | "female",
            "height_cm":     int,
            "weight_kg":     int,
            "goal":          "lose" | "maintain" | "gain",
            "activity":      0-4  (index của acts list)
        }
        """
        self.lbl_name.setText(user_data.get("display_name", "Người dùng"))
        self.lbl_email.setText(user_data.get("email", "–"))

        if user_data.get("avatar_pixmap"):
            self.avatar.set_pixmap(user_data["avatar_pixmap"])

        # Mở khóa ô tên khi đã đăng nhập
        self.input_name.setEnabled(True)
        self.input_name.setText(user_data.get("display_name", ""))

        self.input_age.setText(str(user_data.get("age", "")))
        self.input_height.setText(str(user_data.get("height_cm", "")))
        self.input_weight.setText(str(user_data.get("weight_kg", "")))

        # Giới tính
        g = user_data.get("gender", "male")
        self.btn_male.setChecked(g == "male")
        self.btn_female.setChecked(g == "female")

        # Mục tiêu
        goal = user_data.get("goal", "lose")
        self.btn_lose.setChecked(goal == "lose")
        self.btn_maintain.setChecked(goal == "maintain")
        self.btn_gain.setChecked(goal == "gain")

        # Mức vận động
        act_idx = user_data.get("activity", 0)
        if 0 <= act_idx < len(self._act_buttons):
            self._act_buttons[act_idx].setChecked(True)

        self.btn_google.setVisible(False)
        self.btn_logout.setVisible(True)