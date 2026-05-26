# pages/page_gym.py
import os
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QWidget,
    QGraphicsDropShadowEffect, QLineEdit, QSizePolicy,
    QScrollArea, QScrollBar
)
from PySide6.QtCore import Qt, QEvent, QSize
from PySide6.QtGui import QFont, QColor, QPixmap, QPainter, QBrush, QPen

from pages.gym_exercise_map import EXERCISE_MAP, get_by_group, check_assets, FILE_FOUND

# PySide6 Multimedia — phát video .mp4 trực tiếp không cần thư viện ngoài
# QMediaPlayer: engine điều khiển play/pause/seek
# QVideoWidget: widget hiển thị frame video lên màn hình
# QAudioOutput: bắt buộc khai báo dù không chỉnh âm, nếu thiếu video câm
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl

# ── Màu sắc ───────────────────────────────────────────────────────────────────
C_PURPLE_MAIN   = "#C94CEB"
C_PURPLE_BORDER = "#F1C5FF"
C_HEADER_TEXT   = "#9B30C4"
C_TITLE_TEXT    = "#6A0DAD"
C_BODY_TEXT     = "#333333"
C_BADGE_BG      = "#F0C0FF"
C_BADGE_TEXT    = "#7A1FA0"
C_BORDER        = "#D357F5"
C_PLACEHOLDER   = "#C084E0"
C_PANEL_BG      = "rgba(242, 242, 242, 242)"
C_WARNING_TEXT  = "#CC2200"

# ── Asset paths ────────────────────────────────────────────────────────────────
# BASE_DIR: thư mục gốc D:\FooderAI — tính từ vị trí file này (pages/)
# Dùng path tuyệt đối để os.path.exists() luôn tìm đúng dù chạy từ đâu
BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_GYM    = os.path.join(BASE_DIR, "assets", "fooderai-gym")
ASSET_THUMB  = os.path.join(BASE_DIR, "assets", "fdai-gym-content", "thumbnail")
ASSET_VIDEO  = os.path.join(BASE_DIR, "assets", "fdai-gym-content", "video")
ICON_LOISICH = os.path.join(ASSET_GYM, "fdai-gym-advantagepoint.png")
ICON_LUUY    = os.path.join(ASSET_GYM, "fdai-gym-cautiouspoint.png")


# =====================================================================
# LỚP 1: GYMSEARCHBAR
# =====================================================================
class GymSearchBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedSize(272, 28)

        row = QHBoxLayout(self)
        row.setContentsMargins(10, 0, 10, 0)
        row.setSpacing(0)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("🔍     │     Tìm bài tập")
        f = QFont("Roboto")
        f.setPixelSize(12)
        self.input_box.setFont(f)
        self.input_box.setStyleSheet("""
            QLineEdit { background: transparent; border: none; color: #2A004A; }
            QLineEdit::placeholder { color: rgba(60, 0, 90, 0.55); }
        """)
        row.addWidget(self.input_box)

        self._style_normal = """
            GymSearchBar {
                background-color: rgba(255, 255, 255, 178);
                border-radius: 14px;
                border: 1px solid rgba(180, 80, 220, 0.45);
            }
        """
        self._style_focus = """
            GymSearchBar {
                background-color: rgba(255, 255, 255, 217);
                border-radius: 14px;
                border: 1.5px solid rgba(180, 80, 220, 0.75);
            }
        """
        self.setStyleSheet(self._style_normal)

        sh = QGraphicsDropShadowEffect()
        sh.setBlurRadius(6)
        sh.setOffset(0, 1)
        sh.setColor(QColor(100, 0, 150, 80))
        self.setGraphicsEffect(sh)
        self.input_box.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.input_box:
            if event.type() == QEvent.Type.FocusIn:
                self.setStyleSheet(self._style_focus)
            elif event.type() == QEvent.Type.FocusOut:
                self.setStyleSheet(self._style_normal)
        return super().eventFilter(obj, event)


# =====================================================================
# LỚP 2: EXERCISELISTITEM — 1 ô bài tập trong sidebar
# =====================================================================
class ExerciseListItem(QFrame):
    def __init__(self, exercise: dict, parent=None):
        super().__init__(parent)
        self.exercise = exercise
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFixedHeight(58)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._selected = False
        self._apply_style()

        row = QHBoxLayout(self)
        row.setContentsMargins(8, 4, 8, 4)
        row.setSpacing(8)

        # thumbnail nhỏ 44×44 trong sidebar
        self.thumb_lbl = QLabel()
        self.thumb_lbl.setFixedSize(44, 44)
        self.thumb_lbl.setStyleSheet("border-radius: 6px; background: #EDD5FF;")
        thumb_path = exercise.get("thumbnail", "")
        _st = check_assets(exercise)
        if _st["thumbnail"] == FILE_FOUND:
            self.thumb_lbl.setPixmap(
                QPixmap(thumb_path).scaled(
                    44, 44,
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        row.addWidget(self.thumb_lbl)

        # tên + badge nhóm tuổi
        text_col = QVBoxLayout()
        text_col.setSpacing(2)
        text_col.setContentsMargins(0, 0, 0, 0)

        self.lbl_name = QLabel(exercise["ten"])
        f_name = QFont("Roboto")
        f_name.setPixelSize(20)   # 20px theo yêu cầu
        f_name.setBold(True)
        self.lbl_name.setFont(f_name)
        self.lbl_name.setStyleSheet(
            "color: #5A0090; background: transparent; border: none;"
        )
        # shadow nhẹ trên tên bài
        sh_name = QGraphicsDropShadowEffect()
        sh_name.setBlurRadius(4)
        sh_name.setOffset(1, 1)
        sh_name.setColor(QColor(120, 0, 180, 100))
        self.lbl_name.setGraphicsEffect(sh_name)

        self.lbl_badge = QLabel(exercise["nhom_tuoi"])
        f_badge = QFont("Roboto")
        f_badge.setPixelSize(10)
        self.lbl_badge.setFont(f_badge)
        self.lbl_badge.setFixedWidth(72)
        self.lbl_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_badge.setStyleSheet(
            "background: #F0C0FF; color: #7A1FA0; border-radius: 6px; padding: 1px 4px; border: none;"
        )

        text_col.addWidget(self.lbl_name)
        text_col.addWidget(self.lbl_badge, alignment=Qt.AlignmentFlag.AlignLeft)
        row.addLayout(text_col)

    def set_selected(self, val: bool):
        self._selected = val
        self._apply_style()
        # chữ trắng khi selected, tím khi không
        self.lbl_name.setStyleSheet(
            f"color: {'#FFFFFF' if val else '#5A0090'}; background: transparent; border: none;"
        )

    def _apply_style(self):
        if self._selected:
            self.setStyleSheet("""
                ExerciseListItem {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #C94CEB, stop:1 #9B1FBF);
                    border-radius: 10px;
                    border: none;
                }
            """)
        else:
            self.setStyleSheet("""
                ExerciseListItem {
                    background: transparent;
                    border-radius: 10px;
                    border: none;
                }
                ExerciseListItem:hover {
                    background: rgba(201, 76, 235, 0.12);
                }
            """)


# =====================================================================
# LỚP 3: STEPNUMBER — ô số bước bo góc dùng QPainter
# =====================================================================
class StepNumber(QWidget):
    def __init__(self, number: int, parent=None):
        super().__init__(parent)
        self.number = number
        self.setFixedSize(44, 44)

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        # nền tím bo góc 4px theo spec
        p.setBrush(QBrush(QColor(C_PURPLE_MAIN)))
        p.setPen(QPen(QColor(C_PURPLE_BORDER), 2))
        p.drawRoundedRect(2, 2, 40, 40, 4, 4)
        # số trắng
        p.setPen(QColor("#FFFFFF"))
        f = QFont("Roboto")
        f.setPixelSize(20)
        f.setBold(True)
        p.setFont(f)
        p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, str(self.number))
        p.end()


# =====================================================================
# LỚP 4: EXERCISECONTENTPANEL — panel phải cuộn dọc
# =====================================================================
class ExerciseContentPanel(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical {
                background: #F5E6FF;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #C94CEB;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

        self._inner = QWidget()
        self._inner.setStyleSheet("background: transparent;")
        self.setWidget(self._inner)
        self._layout = QVBoxLayout(self._inner)
        self._layout.setContentsMargins(20, 20, 20, 30)
        self._layout.setSpacing(0)

        self._show_placeholder()

    # ── public API ────────────────────────────────────────────────────
    def load(self, exercise: dict):
        # Disconnect player cũ trước khi clear widget
        # Nếu không, positionChanged vẫn fire vào seek_slider đã bị deleteLater → RuntimeError loop
        if hasattr(self, "_player") and self._player is not None:
            try:
                self._player.stop()
                self._player.positionChanged.disconnect()
                self._player.durationChanged.disconnect()
                self._player.playbackStateChanged.disconnect()
                self._player = None
            except RuntimeError:
                pass  # signal đã disconnect trước đó
        self._clear()
        self.verticalScrollBar().setValue(0)
        self._render(exercise)

    def show_placeholder(self):
        self._clear()
        self._show_placeholder()

    # ── placeholder ───────────────────────────────────────────────────
    def _show_placeholder(self):
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._layout.addWidget(spacer)

        lbl_icon = QLabel("💪")
        lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_icon.setStyleSheet("font-size: 28px; background: transparent; border: none;")

        lbl_text = QLabel("Chọn một bài tập để bắt đầu\nhành trình rèn luyện của bạn")
        lbl_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f = QFont("Roboto")
        f.setPixelSize(16)
        lbl_text.setFont(f)
        lbl_text.setStyleSheet(
            f"color: {C_PLACEHOLDER}; background: transparent; border: none;"
        )

        center = QVBoxLayout()
        center.setSpacing(10)
        center.addWidget(lbl_icon)
        center.addWidget(lbl_text)

        wrapper = QWidget()
        wrapper.setStyleSheet("background: transparent;")
        wrapper.setLayout(center)
        self._layout.addWidget(wrapper, alignment=Qt.AlignmentFlag.AlignCenter)

        spacer2 = QWidget()
        spacer2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._layout.addWidget(spacer2)

    # ── render full content ────────────────────────────────────────────
    def _render(self, d: dict):
        # 1. Tiêu đề + badge nhóm tuổi
        hdr = QHBoxLayout()
        hdr.setContentsMargins(0, 0, 0, 6)

        lbl_title = QLabel(d["ten"])
        f_title = QFont("Roboto")
        f_title.setPixelSize(40)   # 40px theo yêu cầu
        f_title.setBold(True)
        lbl_title.setFont(f_title)
        lbl_title.setStyleSheet(
            f"color: {C_TITLE_TEXT}; background: transparent; border: none;"
        )
        hdr.addWidget(lbl_title)

        badge = QLabel(d["nhom_tuoi"])
        f_b = QFont("Roboto")
        f_b.setPixelSize(11)
        badge.setFont(f_b)
        badge.setFixedHeight(22)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(
            f"background: {C_BADGE_BG}; color: {C_BADGE_TEXT}; "
            "border-radius: 8px; padding: 0 10px; border: none;"
        )
        hdr.addWidget(badge, alignment=Qt.AlignmentFlag.AlignBottom)
        hdr.addStretch()

        self._add_layout(hdr)
        self._add_divider()

        # 2. Media (thumbnail → video khi nhấn play)
        self._render_media(d)

        # 3. Tổng quan
        self._add_section_header("Tổng quan về bài tập")
        self._add_divider(thin=True)
        self._add_body(d["tong_quan"], wrap=820)
        self._add_spacer(17) #chỉnh tại đây nếu chưa hợp
        self._add_divider(thin=True)

        # 4. Các bước thực hiện
        self._add_section_header("Các bước thực hiện:")
        for step in d["cac_buoc"]:
            self._render_step(step)
        self._add_spacer(17) #chỉnh tại đây nếu chưa hợp
        self._add_divider(thin=True)

        # 5. Lợi ích
        self._render_icon_section(
            ICON_LOISICH, "⭐",
            "Lợi ích khi tập luyện bài này:",
            d["loi_ich"],
        )
        self._add_divider(thin=True)

        # 6. Lưu ý
        self._render_icon_section(
            ICON_LUUY, "⚠️",
            "Lưu ý khi tập bài tập này:",
            d["luu_y"],
            warning=True,
        )

        self._layout.addStretch()

    # ── media pipeline ─────────────────────────────────────────────────
    def _render_media(self, d: dict):
        """
        Pipeline media dùng QGraphicsView + QGraphicsVideoItem thay QVideoWidget.

        Lý do đổi:
        - QVideoWidget dùng native HWND handle riêng trên Windows
        - Khi nằm trong QScrollArea, Qt không thể composite native handle
          vào scroll surface → màn hình đen, event bị chặn
        - QGraphicsVideoItem render qua QPainter (software/OpenGL)
          → hoạt động đúng trong mọi container kể cả QScrollArea

        Layout:
        ┌─ media_wrap (QFrame border hồng, +50px = 870px) ───────┐
        │  ┌─ QStackedWidget 870×350 ──────────────────────────┐  │
        │  │  [0] QLabel          — thumbnail PNG khi chờ      │  │
        │  │  [1] QGraphicsView   — render video qua painter   │  │
        │  └───────────────────────────────────────────────────┘  │
        │  ctrl_bar — ▶/⏸  QSlider  0:00/0:00                    │
        └────────────────────────────────────────────────────────-┘

        Luồng:
        1. Load bài  → stack index 0 (thumbnail)
        2. Nhấn ▶    → stack index 1 + player.play()
        3. Nhấn ⏸    → player.pause(), giữ stack index 1
        4. Nhấn ▶    → player.play() tiếp
        5. Hết video → StoppedState → stack index 0
        """
        from PySide6.QtWidgets import QStackedWidget, QSlider, QPushButton
        from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
        from PySide6.QtMultimediaWidgets import QGraphicsVideoItem
        from PySide6.QtCore import QRectF

        # VIDEO_H: chiều cao khung video — +50px theo yêu cầu (300 → 350)
        VIDEO_H  = 350
        # VIDEO_W: chiều rộng — căn theo right_panel 892px trừ margin 20px mỗi bên
        VIDEO_W  = 840

        # ── outer frame: border hồng + shadow 3px right-bottom ────────
        media_wrap = QFrame()
        media_wrap.setStyleSheet(f"""
            QFrame {{
                background: #1A1A2E;
                border: 2px solid {C_BORDER};
                border-radius: 10px;
            }}
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(0)
        shadow.setOffset(3, 3)
        shadow.setColor(QColor(C_BORDER))
        media_wrap.setGraphicsEffect(shadow)

        media_layout = QVBoxLayout(media_wrap)
        media_layout.setContentsMargins(0, 0, 0, 0)
        media_layout.setSpacing(0)

        # ── display stack ─────────────────────────────────────────────
        stack = QStackedWidget()
        stack.setFixedSize(VIDEO_W, VIDEO_H)

        # [0] thumbnail PNG — QLabel + QPixmap, không cần multimedia
        thumb_lbl = QLabel()
        thumb_lbl.setFixedSize(VIDEO_W, VIDEO_H)
        thumb_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thumb_lbl.setStyleSheet("background: #2A1A3E; border: none;")

        thumb_path = d.get("thumbnail", "")
        _asset_status = check_assets(d)
        if _asset_status["thumbnail"] == FILE_FOUND:
            thumb_lbl.setPixmap(
                QPixmap(thumb_path).scaled(
                    VIDEO_W, VIDEO_H,
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            thumb_lbl.setText(f"[ {os.path.basename(thumb_path)} ]")
            thumb_lbl.setStyleSheet(
                "background: #EEE0FF; color: #9B30C4; border: none; font-size: 13px;"
            )
        stack.addWidget(thumb_lbl)   # index 0

        # [1] QGraphicsView chứa QGraphicsVideoItem
        # QGraphicsView: widget Qt thuần, render qua QPainter → không bị lỗi scroll
        # QGraphicsScene: scene graph chứa các item
        # QGraphicsVideoItem: item nhận frame từ QMediaPlayer và vẽ qua scene
        scene = QGraphicsScene()
        scene.setBackgroundBrush(QColor("#000000"))

        video_item = QGraphicsVideoItem()
        # setSize: kích thước item trong scene, phải khớp với view
        video_item.setSize(QRectF(0, 0, VIDEO_W, VIDEO_H).size())
        scene.addItem(video_item)

        gfx_view = QGraphicsView(scene)
        gfx_view.setFixedSize(VIDEO_W, VIDEO_H)
        gfx_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        gfx_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        gfx_view.setStyleSheet("background: #000000; border: none;")
        # fitInView đảm bảo video luôn vừa khung khi resize
        gfx_view.fitInView(video_item, Qt.AspectRatioMode.KeepAspectRatio)
        stack.addWidget(gfx_view)    # index 1

        stack.setCurrentIndex(0)
        media_layout.addWidget(stack)

        # ── QMediaPlayer ──────────────────────────────────────────────
        # setVideoOutput nhận QGraphicsVideoItem thay vì QVideoWidget
        # Engine vẫn là FFmpeg (đã confirm), chỉ đổi surface render
        player = QMediaPlayer()
        audio_out = QAudioOutput()
        player.setAudioOutput(audio_out)
        player.setVideoOutput(video_item)   # ← QGraphicsVideoItem, không phải QVideoWidget

        video_path = d.get("video", "")
        if _asset_status["video"] == FILE_FOUND:
            player.setSource(QUrl.fromLocalFile(os.path.abspath(video_path)))

        # giữ reference tránh GC thu hồi
        self._player     = player
        self._audio_out  = audio_out
        self._video_item = video_item
        self._scene      = scene

        # ── control bar ───────────────────────────────────────────────
        ctrl = QFrame()
        ctrl.setFixedHeight(36)
        ctrl.setStyleSheet(
            "background: #1A1A2E; border: none; border-radius: 0 0 8px 8px;"
        )
        ctrl_row = QHBoxLayout(ctrl)
        ctrl_row.setContentsMargins(10, 0, 10, 0)
        ctrl_row.setSpacing(8)

        # QPushButton thay QLabel để nhận click đáng tin cậy hơn trong scroll
        # QLabel.mousePressEvent dễ bị scroll container chặn trên Windows
        self._playing  = False
        self._play_btn = QPushButton("▶")
        self._play_btn.setFixedSize(28, 28)
        self._play_btn.setStyleSheet("""
            QPushButton {
                color: white; font-size: 14px;
                background: transparent; border: none;
            }
            QPushButton:hover { color: #C94CEB; }
        """)
        self._play_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        def toggle_play():
            """
            Play/Pause toggle:
            - Chưa play  → stack index 1 (QGraphicsView) + player.play()
            - Đang play  → player.pause(), giữ stack index 1
            - Đang pause → player.play() tiếp
            """
            if not self._playing:
                stack.setCurrentIndex(1)
                player.play()
                self._play_btn.setText("⏸")
                self._playing = True
            else:
                player.pause()
                self._play_btn.setText("▶")
                self._playing = False

        # clicked signal của QPushButton — không bị scroll chặn
        self._play_btn.clicked.connect(toggle_play)
        ctrl_row.addWidget(self._play_btn)

        # QSlider seekbar
        seek_slider = QSlider(Qt.Orientation.Horizontal)
        seek_slider.setRange(0, 0)
        seek_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px; background: #5A3A6E; border-radius: 2px;
            }
            QSlider::handle:horizontal {
                width: 12px; height: 12px; margin: -4px 0;
                background: #C94CEB; border-radius: 6px;
            }
            QSlider::sub-page:horizontal {
                background: #C94CEB; border-radius: 2px;
            }
        """)
        ctrl_row.addWidget(seek_slider, stretch=1)

        lbl_time = QLabel("0:00 / 0:00")
        lbl_time.setStyleSheet(
            "color: #CCCCCC; font-size: 10px; background: transparent; border: none;"
        )
        ctrl_row.addWidget(lbl_time)

        media_layout.addWidget(ctrl)
        self._layout.addWidget(media_wrap)
        self._add_spacer(17) #chỉnh tại đây nếu chưa hợp

        # ── signals ───────────────────────────────────────────────────
        def fmt_time(ms: int) -> str:
            """ms → chuỗi m:ss"""
            s = ms // 1000
            return f"{s // 60}:{s % 60:02d}"

        def on_duration(dur: int):
            """
            durationChanged(dur) — fired khi FFmpeg đọc xong metadata
            Cập nhật range slider để kéo đúng tỉ lệ thời gian
            """
            seek_slider.setRange(0, dur)

        self._last_ui_update = 0

        def on_position(pos: int):
            """
            positionChanged(pos) — fired ~30fps
            Throttle 500ms tránh update UI quá nhiều lần làm lag
            blockSignals tránh vòng lặp signal↔slot
            """
            if pos - self._last_ui_update < 500 and pos != 0:
                return
            self._last_ui_update = pos
            seek_slider.blockSignals(True)
            seek_slider.setValue(pos)
            seek_slider.blockSignals(False)
            lbl_time.setText(f"{fmt_time(pos)} / {fmt_time(player.duration())}")

        def on_seek(val: int):
            """
            valueChanged(int val) từ seek_slider — fired khi người dùng kéo thanh
            val: vị trí mới (ms) → setPosition nhảy tới vị trí đó ngay lập tức
            Reset _last_ui_update = 0 để on_position update label thời gian ngay,
            không bị throttle 500ms che mất giá trị vừa seek tới
            """
            self._last_ui_update = 0  # ← thêm dòng này
            player.setPosition(val)

        def on_state_changed(state):
            """
            playbackStateChanged — fired khi stop/pause/play
            StoppedState (video kết thúc) → reset về thumbnail
            """
            from PySide6.QtMultimedia import QMediaPlayer as QMP
            if state == QMP.PlaybackState.StoppedState:
                stack.setCurrentIndex(0)
                self._play_btn.setText("▶")
                self._playing = False
                seek_slider.setValue(0)
                lbl_time.setText("0:00 / 0:00")

        player.durationChanged.connect(on_duration)
        player.positionChanged.connect(on_position)
        seek_slider.valueChanged.connect(on_seek)
        player.playbackStateChanged.connect(on_state_changed)

    def _toggle_play(self, _event=None):
        # legacy stub
        pass

    # ── step block ─────────────────────────────────────────────────────
    def _render_step(self, step: dict):
        row = QHBoxLayout()
        row.setContentsMargins(0, 15, 0, 0) #update, edit tại đây
        row.setSpacing(12)
        row.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ô số bước vuông tím bo 4px
        num = StepNumber(step["so"])
        row.addWidget(num, alignment=Qt.AlignmentFlag.AlignTop)

        lbl = QLabel(step["noi_dung"])
        lbl.setWordWrap(True)
        f = QFont("Roboto")
        f.setPixelSize(17)   # +4px theo yêu cầu
        lbl.setFont(f)
        lbl.setStyleSheet(
            f"color: {C_BODY_TEXT}; background: transparent; border: none;"
        )
        lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        row.addWidget(lbl)

        self._add_layout(row)

    # ── icon section (lợi ích / lưu ý) ────────────────────────────────
    def _render_icon_section(self, icon_path, fallback_emoji, title, items, warning=False):
        hdr_row = QHBoxLayout()
        hdr_row.setContentsMargins(0, 20, 0, 8) #UPDATED HERE, EDIT IN HERE
        hdr_row.setSpacing(10)

        icon_lbl = QLabel()
        icon_lbl.setFixedSize(36, 36)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet("background: transparent; border: none;")
        if os.path.exists(icon_path):
            icon_lbl.setPixmap(
                QPixmap(icon_path).scaled(
                    36, 36,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            icon_lbl.setText(fallback_emoji)
            icon_lbl.setStyleSheet(
                "font-size: 22px; background: transparent; border: none;"
            )
        hdr_row.addWidget(icon_lbl)

        lbl_title = QLabel(title)
        f_h = QFont("Roboto")
        f_h.setPixelSize(20)   # +4px theo yêu cầu
        f_h.setBold(True)
        lbl_title.setFont(f_h)
        color = C_WARNING_TEXT if warning else C_HEADER_TEXT
        lbl_title.setStyleSheet(
            f"color: {color}; background: transparent; border: none;"
        )
        hdr_row.addWidget(lbl_title)
        hdr_row.addStretch()
        self._add_layout(hdr_row)

        for item in items:
            item_row = QHBoxLayout()
            item_row.setContentsMargins(8, 10, 0, 0) #update, chỉnh sửa tại đây
            item_row.setSpacing(8)
            item_row.setAlignment(Qt.AlignmentFlag.AlignTop)

            dash = QLabel("–")
            dash.setFixedWidth(12)
            dash.setStyleSheet(
                f"color: {C_BODY_TEXT}; background: transparent; border: none;"
            )
            item_row.addWidget(dash, alignment=Qt.AlignmentFlag.AlignTop)

            lbl = QLabel(item)
            lbl.setWordWrap(True)
            f_b = QFont("Roboto")
            f_b.setPixelSize(17)   # +4px theo yêu cầu
            lbl.setFont(f_b)
            lbl.setStyleSheet(
                f"color: {C_BODY_TEXT}; background: transparent; border: none;"
            )
            lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            item_row.addWidget(lbl)
            self._add_layout(item_row)

    # ── helpers ────────────────────────────────────────────────────────
    def _clear(self):
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _add_widget(self, w: QWidget, **kwargs):
        self._layout.addWidget(w, **kwargs)

    def _add_layout(self, lay):
        wrapper = QWidget()
        wrapper.setStyleSheet("background: transparent;")
        wrapper.setLayout(lay)
        self._layout.addWidget(wrapper)

    def _add_divider(self, thin=False):
        # Dày 4px theo yêu cầu (từ 1pt lên 4pt ≈ 4px ở 96dpi)
        # thin=True : vạch nhạt #EDD5FF giữa các section
        # thin=False: vạch đậm C_BORDER ngăn cách khối lớn
        line = QFrame()
        line.setFixedHeight(4)
        color = "#EDD5FF" if thin else C_BORDER
        line.setStyleSheet(
            f"background: {color}; border: none; border-radius: 2px;"
        )
        self._layout.addWidget(line)
        # 3px spacing sau divider = 2pt breathing room giữa các paragraph
        sp = QWidget()
        sp.setFixedHeight(3)
        sp.setStyleSheet("background: transparent;")
        self._layout.addWidget(sp)

    def _add_spacer(self, h=8):
        sp = QWidget()
        sp.setFixedHeight(h)
        sp.setStyleSheet("background: transparent;")
        self._layout.addWidget(sp)

    def _add_section_header(self, text: str):
        lbl = QLabel(text)
        f = QFont("Roboto")
        f.setPixelSize(20)   # +4px theo yêu cầu
        f.setBold(True)
        lbl.setFont(f)
        lbl.setStyleSheet(
            f"color: {C_HEADER_TEXT}; background: transparent; border: none;"
        )
        self._layout.addWidget(lbl)

    def _add_body(self, text: str, wrap=820):
        lbl = QLabel(text)
        lbl.setWordWrap(True)
        lbl.setMaximumWidth(wrap)
        f = QFont("Roboto")
        f.setPixelSize(17)   # +4px theo yêu cầu
        lbl.setFont(f)
        lbl.setStyleSheet(
            f"color: {C_BODY_TEXT}; background: transparent; border: none;"
        )
        self._layout.addWidget(lbl)


# =====================================================================
# LỚP 5: PAGEEXERCISE — trang chính
# =====================================================================
class PageExercise(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1240, 640)
        self.setStyleSheet("""
            PageExercise {
                background-color: white;
                border: 3px solid rgba(0, 77, 77, 0.5);
                border-radius: 24px;
            }
        """)

        box_shadow = QGraphicsDropShadowEffect()
        box_shadow.setBlurRadius(5)
        box_shadow.setOffset(0, 3)
        box_shadow.setColor(QColor(150, 150, 150, 180))
        self.setGraphicsEffect(box_shadow)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 10, 15, 15)
        main_layout.setSpacing(0)

        # ── BANNER ────────────────────────────────────────────────────
        self.banner = QFrame()
        self.banner.setFixedSize(1210, 60)

        color_hex = "#D250F6"
        base_color = QColor(color_hex)
        color_80  = base_color.darker(109).name()
        color_100 = base_color.darker(131).name()

        self.banner.setStyleSheet(f"""
            QFrame {{
                background-color: qlineargradient(
                    x1:0, y1:0.2, x2:1, y2:1,
                    stop:0 {color_hex}, stop:0.8 {color_80}, stop:1.0 {color_100}
                );
                border-radius: 15px;
                border: none;
            }}
        """)

        banner_layout = QHBoxLayout(self.banner)
        banner_layout.setContentsMargins(8, 0, 8, 0)
        banner_layout.setSpacing(0)

        title_group = QWidget()
        title_group.setStyleSheet("background: transparent;")
        title_layout = QHBoxLayout(title_group)
        title_layout.setContentsMargins(7, 0, 3, 0)
        title_layout.setSpacing(5)

        title_icon = QLabel()
        icon_path = os.path.join(BASE_DIR, "assets", "fooderai-gym", "fooderai-gym-logo.png")
        if os.path.exists(icon_path):
            title_icon.setPixmap(
                QPixmap(icon_path).scaledToHeight(
                    45, Qt.TransformationMode.SmoothTransformation
                )
            )
        title_icon.setStyleSheet("border: none; background: transparent;")

        title_text = QLabel("Chế độ thể dục")
        title_text.setStyleSheet("""
            color: white; border: none;
            font-family: 'Roboto'; font-size: 25px; font-weight: 800;
        """)

        title_layout.addWidget(title_icon)
        title_layout.addWidget(title_text)
        banner_layout.addWidget(
            title_group,
            alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
        )
        banner_layout.addStretch()

        banner_shadow = QGraphicsDropShadowEffect()
        banner_shadow.setBlurRadius(2)
        banner_shadow.setOffset(0, 0)
        banner_shadow.setColor(QColor(0, 0, 0, 204))
        self.banner.setGraphicsEffect(banner_shadow)
        main_layout.addWidget(
            self.banner,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter,
        )

        # ── BODY ──────────────────────────────────────────────────────
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 5, 0, 0)
        body_layout.setSpacing(8)

        # ── SIDEBAR TRÁI ──────────────────────────────────────────────
        self.sidebar = QLabel()
        self.sidebar.setFixedSize(310, 550)
        nav_path = os.path.join(BASE_DIR, "assets", "fooderai-gym", "fdai-gym-nav.png")
        if os.path.exists(nav_path):
            self.sidebar.setPixmap(
                QPixmap(nav_path).scaled(
                    310, 550,
                    Qt.AspectRatioMode.IgnoreAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )

        # tiêu đề "Thư viện bài tập"
        self.lbl_lib_title = QLabel("Thư viện bài tập", self.sidebar)
        f_lib = QFont("Roboto")
        f_lib.setPixelSize(22)
        f_lib.setWeight(QFont.Weight.ExtraBold)
        self.lbl_lib_title.setFont(f_lib)
        self.lbl_lib_title.setStyleSheet(
            "color: white; border: none; background: transparent;"
        )
        self.lbl_lib_title.adjustSize()
        sh_title = QGraphicsDropShadowEffect()
        sh_title.setBlurRadius(3)
        sh_title.setOffset(0, 1)
        sh_title.setColor(QColor(80, 0, 120, 180))
        self.lbl_lib_title.setGraphicsEffect(sh_title)
        self.lbl_lib_title.move(18, 18)

        self.search_bar = GymSearchBar(self.sidebar)
        self.search_bar.move(18, 56)
        self.search_bar.input_box.textChanged.connect(self._on_search)

        # ── tab filter ─────────────────────────────────────────────────
        self._current_tab = "Tất cả"
        tab_labels      = ["Tất cả", "Trẻ em", "Thanh niên", "Người già"]

        # ── TỌA ĐỘ TAB — CHỈNH Ở ĐÂY ────────────────────────────────
        # ── TỌA ĐỘ TAB — 4 ô bằng nhau chia đều sidebar ────────────────
        # TAB_Y      : tọa độ Y chung — chỉnh 1 số để hạ/nâng cả 4 tab
        # TAB_H      : chiều cao mỗi ô
        # TAB_START_X: lề trái
        # TAB_W      : chiều rộng mỗi ô = tổng / 4, tự chia đều
        TAB_Y = 103  # ← hạ/nâng cả hàng tab
        TAB_H = 18  # ← tăng nếu muốn ô cao hơn
        TAB_TEXT_Y = TAB_Y  # ← CHỈNH SỐ TẠI ĐÂY, LẤY TAB_Y làm gốc để chỉnh
        TAB_START_X = 8  # ← lề trái
        TAB_TOTAL_W = 294  # ← tổng chiều rộng 4 ô
        TAB_W = TAB_TOTAL_W // 4  # = 73px mỗi ô, tự chia đều

        self._tab_labels_widgets = []
        self._tab_highlights = []

        for i, text in enumerate(tab_labels):
            x = TAB_START_X + i * TAB_W  # X tự tính đều nhau

            # ô highlight — frame vô hình, hiện màu khi tab được chọn
            hl = QFrame(self.sidebar)
            hl.setGeometry(x, TAB_Y, TAB_W, TAB_H)
            hl.setStyleSheet("""
                        QFrame {
                            background-color: rgba(242, 242, 242, 220);
                            border-radius: 4px;
                            border: none;
                        }
                    """)
            hl.hide()
            hl.lower()  # nằm dưới chữ
            self._tab_highlights.append((text, hl))

            # chữ tab — cùng kích thước ô, căn giữa
            lbl = QLabel(text, self.sidebar)
            f_tab = QFont("Roboto")
            f_tab.setPixelSize(11)
            f_tab.setWeight(QFont.Weight.Medium)
            lbl.setFont(f_tab)
            lbl.setStyleSheet(
                "color: #2A004A; background: transparent; border: none;"
            )
            lbl.setFixedSize(TAB_W, TAB_H)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.move(x, TAB_TEXT_Y)
            lbl.setCursor(Qt.CursorShape.PointingHandCursor)
            lbl.raise_()
            lbl.mousePressEvent = lambda e, t=text: self._on_tab_click(t)
            self._tab_labels_widgets.append((text, lbl))

        self._update_tab_highlight("Tất cả")

        # ── list bài tập (scroll khi > 6) ─────────────────────────────
        self._list_container = QWidget(self.sidebar)
        self._list_container.setGeometry(8, 126, 294, 420)
        self._list_container.setStyleSheet("background: transparent;")

        self._list_scroll = QScrollArea(self._list_container)
        self._list_scroll.setGeometry(0, 0, 294, 420)
        self._list_scroll.setWidgetResizable(True)
        self._list_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._list_scroll.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical {
                background: rgba(255,255,255,60);
                width: 6px; border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: rgba(201,76,235,180);
                border-radius: 3px; min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

        self._list_inner = QWidget()
        self._list_inner.setStyleSheet("background: transparent;")
        self._list_layout = QVBoxLayout(self._list_inner)
        self._list_layout.setContentsMargins(0, 0, 0, 0)
        self._list_layout.setSpacing(4)
        self._list_layout.addStretch()
        self._list_scroll.setWidget(self._list_inner)

        body_layout.addWidget(self.sidebar, alignment=Qt.AlignmentFlag.AlignTop)

        # ── RIGHT PANEL 892×550 ────────────────────────────────────────
        self.right_panel = QFrame()
        self.right_panel.setFixedSize(892, 550)
        self.right_panel.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.right_panel.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(242, 242, 242, 242);
                border-radius: 16px;
                border: 2px solid {C_BORDER};
            }}
        """)
        rp_shadow = QGraphicsDropShadowEffect()
        rp_shadow.setBlurRadius(8)
        rp_shadow.setOffset(0, 2)
        rp_shadow.setColor(QColor(211, 87, 245, 60))
        self.right_panel.setGraphicsEffect(rp_shadow)

        rp_layout = QVBoxLayout(self.right_panel)
        rp_layout.setContentsMargins(0, 0, 0, 0)
        rp_layout.setSpacing(0)

        self.content_panel = ExerciseContentPanel()
        rp_layout.addWidget(self.content_panel)

        body_layout.addWidget(self.right_panel, alignment=Qt.AlignmentFlag.AlignTop)
        main_layout.addLayout(body_layout)

        self._selected_item = None
        self._render_list(list(EXERCISE_MAP.values()))

    # ── event handlers ─────────────────────────────────────────────────
    def _update_tab_highlight(self, active_tab: str):
        for text, hl in self._tab_highlights:
            hl.show() if text == active_tab else hl.hide()

    def _on_tab_click(self, tab_text: str):
        self._current_tab = tab_text
        self._update_tab_highlight(tab_text)
        self._refresh_list(self.search_bar.input_box.text().strip())

    def _on_search(self, text: str):
        self._refresh_list(text.strip())

    def _refresh_list(self, query=""):
        group = "" if self._current_tab == "Tất cả" else self._current_tab
        items = get_by_group(group)
        if query:
            items = [i for i in items if query.lower() in i["ten"].lower()]
        self._render_list(items)

    def _render_list(self, items: list):
        # reset pointer trước khi deleteLater tránh RuntimeError C++ deleted object
        self._selected_item = None
        while self._list_layout.count() > 1:
            item = self._list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for ex in items:
            widget = ExerciseListItem(ex)
            widget.mousePressEvent = lambda e, w=widget, d=ex: self._on_item_click(w, d)
            self._list_layout.insertWidget(self._list_layout.count() - 1, widget)

        # scrollbar chỉ hiện khi list > 6 bài
        self._list_scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded if len(items) > 6
            else Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

    def _on_item_click(self, widget: ExerciseListItem, exercise: dict):
        # bỏ highlight bài cũ — guard tránh C++ deleted object khi re-render list
        if self._selected_item and self._selected_item is not widget:
            try:
                self._selected_item.set_selected(False)
            except RuntimeError:
                pass
        widget.set_selected(True)
        self._selected_item = widget
        self.content_panel.load(exercise)