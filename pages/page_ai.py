import os
import random
from datetime import datetime, timedelta

# QFrame: khung có viền, dùng làm container có thể style được
# QVBoxLayout: xếp widget theo chiều dọc (Vertical)
# QHBoxLayout: xếp widget theo chiều ngang (Horizontal)
# QLabel: hiển thị chữ hoặc ảnh
# QWidget: widget cơ bản nhất, không có viền
# QGraphicsDropShadowEffect: hiệu ứng đổ bóng cho bất kỳ widget nào
# QLineEdit: ô nhập liệu 1 dòng
# QPushButton: nút bấm
# QScrollArea: vùng cuộn, tự động thêm thanh scroll khi nội dung dài hơn khung
# QSizePolicy: quy tắc co giãn của widget (Expanding = tự mở rộng tối đa)
from PySide6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel,
                               QWidget, QGraphicsDropShadowEffect, QLineEdit,
                               QPushButton, QScrollArea, QSizePolicy)

# Qt: kho hằng số của Qt (căn lề, loại cửa sổ, kiểu con trỏ...)
# QTimer: bộ đếm giờ, gọi hàm theo chu kỳ (dùng cho đồng hồ đếm ngược)
# QTime: đối tượng thời gian HH:MM:SS
# QSize: lưu cặp (width, height) — dùng khi set kích thước icon
from PySide6.QtCore import Qt, QTimer, QTime, QSize

# QFont: đối tượng font chữ (tên font, cỡ, độ đậm)
# QColor: đối tượng màu sắc — nhận hex "#RRGGBB" hoặc RGBA (r, g, b, alpha)
# QPixmap: nạp và hiển thị ảnh PNG/JPG từ file
# QCursor: con trỏ chuột tùy chỉnh — nhận QPixmap hoặc CursorShape built-in
# QPainter: "cây bút vẽ" — dùng trong paintEvent để vẽ hình tự do
# QLinearGradient: gradient tuyến tính (màu chuyển dần từ điểm A → B)
# QBrush: "cái chổi tô màu" bên trong hình (fill)
# QPen: "cây bút vẽ đường viền" bên ngoài hình (stroke)
# QPainterPath: đường dẫn hình học phức tạp (dùng để vẽ hình đa giác)
from PySide6.QtGui import QFont, QColor, QPixmap, QCursor, QPainter, QLinearGradient, QBrush, QPen, QPainterPath, QIcon


# =====================================================================
# LỚP 1: NSFWGUARD — BỘ BẢO VỆ NỘI DUNG
# Nhiệm vụ: đếm tin nhắn, phát hiện vi phạm, phạt bịt mõm
# =====================================================================
class NSFWGuard:
    """
    Quản lý token chat và hệ thống phạt NSFW.

    Thuật ngữ:
    - msg_count  : số tin nhắn đã dùng hôm nay (tối đa 45)
    - nsfw_streak: chuỗi vi phạm NSFW liên tiếp (reset về 0 khi gõ câu sạch)
    - muted_until: thời điểm hết bị bịt mõm (None = không bị phạt)
    """

    # Hằng số — viết HOA để phân biệt với biến thường
    MAX_MSGS    = 45   # tổng tin nhắn tối đa mỗi phiên
    RESET_HOURS = 7    # sau 7 tiếng thì token tự reset về 0
    MUTE_HOURS  = 10   # vi phạm tới ngưỡng → bị khóa 10 tiếng

    # Danh sách 6 câu từ chối nhẹ nhàng — dùng cho vi phạm lần 1 đến 6
    # Cấp độ tăng dần: càng vi phạm nhiều lần, câu trả lời càng nghiêm túc hơn
    REPLIES_SOFT = [
        "Ủa? Gritalyst nghe không rõ, tai đang bị... rau củ nhét vào rồi 🥕 Bạn hỏi lại đi!",
        "Hmm bạn ơi, câu đó hơi lạ với Gritalyst quá — thử hỏi về protein hay calo không, vui hơn đó!",
        "Gritalyst chuyên về dinh dưỡng thôi nha, câu đó mình chịu thua rồi — đổi chủ đề đi bạn ơi!",
        "Bạn ơi, Gritalyst sinh ra để giúp bạn khỏe hơn mỗi ngày, không phải để trả lời câu đó đâu nha — mình vẫn ở đây nếu bạn cần hỏi về sức khỏe nhé!",
        "Câu hỏi này nằm ngoài vùng Gritalyst có thể giúp rồi bạn ơi. Mình hiểu đôi khi tò mò là chuyện bình thường, nhưng Gritalyst chỉ giỏi chuyện ăn uống và luyện tập thôi — quay lại nhé!",
        "Gritalyst muốn nói thật lòng: câu hỏi này mình không thể trả lời, không phải vì ghét bạn, mà vì Gritalyst được tạo ra với một mục đích duy nhất là đồng hành cùng bạn trên hành trình sống khỏe hơn mỗi ngày. Bạn xứng đáng được chăm sóc đúng cách — hỏi mình về dinh dưỡng nhé!",
    ]

    # Câu nghiêm hơn — dùng cho vi phạm lần 7 và 8, trừ 10 tin thay vì 5
    REPLIES_HARD = [
        "Gritalyst thấy bạn đang hỏi những điều ngoài vùng mình có thể giúp khá nhiều lần rồi đó... Mình vẫn ở đây, nhưng hãy cho Gritalyst cơ hội tư vấn đúng chuyên môn nhé! 🌿",
        "Bạn ơi, mình nhận ra cuộc trò chuyện đang đi hướng khác rồi. Gritalyst thực sự muốn giúp bạn — nhưng chỉ về dinh dưỡng và sức khỏe thôi. Thử hỏi về bữa ăn hôm nay đi?",
    ]

    def __init__(self):
        # Khởi tạo trạng thái ban đầu — tất cả đều sạch, chưa bị phạt
        self.msg_count   = 0     # đếm tổng tin đã gửi (kể cả tin bị phạt)
        self.nsfw_streak = 0     # đếm chuỗi vi phạm liên tiếp chưa bị reset
        self.muted_until = None  # None = chưa bị phạt; datetime = thời điểm hết phạt
        self.reset_at    = None  # None = chưa lên lịch reset; datetime = lúc token hết hạn

    def is_muted(self) -> bool:
        """Kiểm tra user có đang trong thời gian bị bịt mõm không."""
        if self.muted_until and datetime.now() < self.muted_until:
            # Vẫn còn trong thời gian phạt
            return True
        if self.muted_until and datetime.now() >= self.muted_until:
            # Hết giờ phạt → tự động mở khóa và xóa streak
            self.muted_until = None
            self.nsfw_streak = 0
        return False

    def mute_remaining(self) -> str:
        """
        Tính thời gian còn lại của hình phạt.
        Trả về chuỗi dạng "HH:MM" để hiển thị đồng hồ đếm ngược.
        """
        if not self.muted_until:
            return "00:00"  # không bị phạt → trả về 0
        delta     = self.muted_until - datetime.now()         # khoảng thời gian còn lại
        total_sec = max(0, int(delta.total_seconds()))        # đổi sang giây, không âm
        hh        = total_sec // 3600                         # lấy phần giờ (chia lấy nguyên)
        mm        = (total_sec % 3600) // 60                  # lấy phần phút (lấy dư rồi chia)
        return f"{hh:02d}:{mm:02d}"                           # format 2 chữ số: "09:05" thay vì "9:5"

    def can_send(self) -> tuple[bool, str]:
        """
        Cổng kiểm tra trước khi cho phép gửi tin.
        Trả về (True, "") nếu OK, hoặc (False, lý_do) nếu bị chặn.
        lý_do có 2 giá trị: "muted" = bị bịt mõm, "quota" = hết lượt
        """
        if self.is_muted():
            return False, "muted"

        # Kiểm tra xem đã đến giờ reset token chưa
        if self.reset_at and datetime.now() >= self.reset_at:
            self.msg_count = 0     # reset về 0
            self.reset_at  = None  # xóa lịch reset

        if self.msg_count >= self.MAX_MSGS:
            return False, "quota"  # hết 45 lượt

        return True, ""  # tất cả OK

    def record_clean(self):
        """
        Ghi nhận 1 tin nhắn sạch (không vi phạm).
        - Tăng đếm tin lên 1
        - Reset streak vi phạm về 0 (chuỗi bị phá vỡ)
        - Lên lịch reset token nếu chưa có
        """
        self.msg_count  += 1
        self.nsfw_streak = 0  # tin sạch → chuỗi vi phạm bị đứt
        if not self.reset_at:
            # Lần gửi đầu tiên trong phiên → bắt đầu đếm 7 tiếng
            self.reset_at = datetime.now() + timedelta(hours=self.RESET_HOURS)

    def record_nsfw(self) -> tuple[str, int]:
        """
        Ghi nhận 1 vi phạm NSFW.
        Trả về (câu_phản_hồi, số_tin_bị_trừ).
        Chuỗi "__muted__" nghĩa là đã đạt ngưỡng bịt mõm.
        """
        self.nsfw_streak += 1       # tăng chuỗi vi phạm lên 1
        streak = self.nsfw_streak   # lưu lại để dùng cho if/else bên dưới

        # Ngưỡng 8: bịt mõm 10 tiếng, không trừ tin nữa
        if streak >= 8:
            self.muted_until = datetime.now() + timedelta(hours=self.MUTE_HOURS)
            return "__muted__", 0

        # Vi phạm lần 7: nghiêm hơn, trừ 10 tin, random 1 trong 2 câu HARD
        if streak >= 7:
            cost  = 10
            reply = random.choice(self.REPLIES_HARD)
        else:
            # Vi phạm lần 1-6: trừ 5 tin, dùng câu theo đúng cấp độ
            # min(streak-1, 5) để không vượt quá index của list 6 phần tử
            cost  = 5
            reply = self.REPLIES_SOFT[min(streak - 1, 5)]

        self.msg_count += cost  # trừ tin (cộng vào đếm để mau hết quota)
        if not self.reset_at:
            self.reset_at = datetime.now() + timedelta(hours=self.RESET_HOURS)
        return reply, cost


# =====================================================================
# LỚP 2: CHATBUBBLE — 1 BONG BÓNG TIN NHẮN
# =====================================================================
class ChatBubble(QFrame):
    """
    Vẽ 1 bong bóng tin nhắn.
    - is_user=True  → căn phải, nền gradient xanh lá (tin của user)
    - is_user=False → căn trái, nền trắng viền nhạt (tin của Gritalyst)
    """
    def __init__(self, text: str, is_user: bool, parent=None):
        super().__init__(parent)
        self.is_user = is_user

        # Expanding theo ngang để chiếm hết chiều rộng có thể
        # Minimum theo dọc để chiều cao tự co theo nội dung text
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Layout ngang: dùng để đẩy bubble sang trái hoặc phải bằng addStretch()
        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 4, 0, 4)  # padding trên/dưới 4px, trái/phải 0

        # Label chứa nội dung tin nhắn
        lbl = QLabel(text)
        lbl.setWordWrap(True)  # tự xuống dòng khi chữ dài hơn MaximumWidth

        # Giới hạn chiều rộng tối đa của bubble:
        # User: 500px (~10 từ/dòng) — hẹp hơn để trông gọn gàng
        # Bot:  720px (~18 từ/dòng) — rộng hơn vì bot thường trả lời dài
        lbl.setMaximumWidth(500 if is_user else 720)

        # Font chữ nội dung tin nhắn
        font = QFont("Roboto")
        font.setPixelSize(16)  # 16px — đủ đọc thoải mái
        lbl.setFont(font)

        if is_user:
            # Bubble bên phải — gradient xanh lá chạy từ trên-phải → dưới-trái
            # x1:1, y1:0 = góc trên bên PHẢI (điểm bắt đầu)
            # x2:0, y2:1 = góc dưới bên TRÁI (điểm kết thúc)
            lbl.setStyleSheet("""
                QLabel {
                    background: qlineargradient(
                        x1:1, y1:0, x2:0, y2:1,
                        stop:0   #3DE365,
                        stop:0.75 #2FC455,
                        stop:1.0  #27A849
                    );
                    color: white;
                    border-radius: 18px;
                    padding: 10px 16px;
                    border: none;
                }
            """)
            outer.addStretch()   # đẩy bubble sang bên phải
            outer.addWidget(lbl)
        else:
            # Bubble bên trái — nền trắng, viền xanh nhạt
            lbl.setStyleSheet("""
                QLabel {
                    background-color: #FFFFFF;
                    color: #1A2A3A;
                    border-radius: 18px;
                    padding: 10px 16px;
                    border: 1.5px solid #D0EAD0;
                }
            """)
            outer.addWidget(lbl)
            outer.addStretch()   # đẩy bubble sang bên trái


# =====================================================================
# LỚP 3: MUTEOVERLAY — LỚP PHỦ KHI BỊ BỊT MÕM
# Hiện lên phủ toàn bộ vùng chat khi nsfw_streak >= 8
# =====================================================================
class MuteOverlay(QFrame):
    """
    Lớp phủ bán trong suốt phủ lên vùng chat.
    Hiển thị đồng hồ đếm ngược và tự ẩn khi hết giờ.
    """
    def __init__(self, guard: NSFWGuard, parent=None):
        super().__init__(parent)
        self.guard = guard  # giữ tham chiếu đến NSFWGuard để hỏi thời gian còn lại

        # Nền trắng xanh nhạt, gần như đục hoàn toàn (alpha 0.97)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(240, 250, 245, 0.97);
                border-radius: 16px;
                border: 2px solid #B8E0C8;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # căn giữa tất cả nội dung
        layout.setSpacing(12)

        # Tiêu đề overlay
        lbl_title = QLabel("Nhu cầu cao")
        font_title = QFont("Roboto")
        font_title.setPixelSize(22)
        font_title.setWeight(QFont.Weight.Bold)
        lbl_title.setFont(font_title)
        lbl_title.setStyleSheet("color: #1A6A3A; border: none; background: transparent;")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Mô tả lý do bị khóa — dùng \n để xuống dòng thủ công
        lbl_desc = QLabel(
            "Gritalyst hiện đang ghi nhận một số lượng lớn yêu cầu không phù hợp\n"
            "trong thời gian ngắn. Để đảm bảo chất lượng tư vấn cho tất cả mọi người,\n"
            "hệ thống tạm thời nghỉ ngơi một chút. Bạn có thể thử lại sau:"
        )
        font_desc = QFont("Roboto")
        font_desc.setPixelSize(15)
        lbl_desc.setFont(font_desc)
        lbl_desc.setStyleSheet("color: #4A6A5A; border: none; background: transparent;")
        lbl_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Đồng hồ đếm ngược — hiển thị HH:MM, cập nhật mỗi giây
        self.lbl_timer = QLabel("10:00")
        font_timer = QFont("Roboto")
        font_timer.setPixelSize(42)  # to hơn để dễ đọc
        font_timer.setWeight(QFont.Weight.Bold)
        self.lbl_timer.setFont(font_timer)
        self.lbl_timer.setStyleSheet("color: #2A7A4A; border: none; background: transparent;")
        self.lbl_timer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_desc)
        layout.addWidget(self.lbl_timer)

        # QTimer: gọi hàm _tick() mỗi 1000ms (1 giây)
        # Đây là "nhịp tim" của đồng hồ đếm ngược
        self._ticker = QTimer(self)
        self._ticker.timeout.connect(self._tick)  # mỗi lần timeout → gọi _tick
        self._ticker.start(1000)                  # bắt đầu đếm, chu kỳ 1000ms

    def _tick(self):
        """Chạy mỗi giây: cập nhật số đếm ngược, tắt overlay khi về 00:00."""
        remaining = self.guard.mute_remaining()  # hỏi NSFWGuard còn bao lâu
        self.lbl_timer.setText(remaining)        # cập nhật hiển thị
        if remaining == "00:00":
            self._ticker.stop()  # dừng timer để không gọi _tick vô ích nữa
            self.hide()          # ẩn overlay, trả lại vùng chat cho user


# =====================================================================
# LỚP 3B: SYSTEMNOTICECARD — THẺ THÔNG BÁO HỆ THỐNG (KHÔNG PHẢI AI)
# Hiển thị inline trong vùng chat khi user đạt 45 tin nhắn HOẶC bị mute
# Không có avatar — đây là thông báo của hệ thống, không phải Gritalyst
# =====================================================================
class SystemNoticeCard(QFrame):
    """
    Thẻ thông báo hệ thống — khác hoàn toàn với ChatBubble:
    - KHÔNG có avatar Gritalyst ở bên cạnh
    - Chiều rộng gần tràn hết vùng chat (~1200px), căn giữa
    - Gradient linear -60° (chéo xuống) từ #38D45F (100% sáng) → #2EAA4C (tối hơn 20%)
    - Dùng cho 2 trường hợp: hết 45 tin (quota) hoặc bị mute do NSFW
    - Sau khi xuất hiện: disable Enter + btn_send (logic nằm trong PageAIAssistant)

    Tại sao -60 độ trong Qt?
    Qt dùng hệ tọa độ x1,y1 → x2,y2 (không phải góc độ trực tiếp).
    -60° tương đương gradient chạy từ góc trên-trái xuống góc dưới-phải
    với độ dốc ~tan(60°) ≈ 1.73, ánh xạ thành:
        x1:0, y1:0 → x2:0.5, y2:0.87  (normalize về [0,1])
    Tạo hiệu ứng chéo xuống từ trái sang phải rất tự nhiên.
    """

    def __init__(self, notice_type: str, guard=None, parent=None):
        """
        notice_type: "quota" = hết 45 tin | "mute" = bị khóa NSFW
        guard: NSFWGuard — dùng để lấy thời gian mute còn lại (chỉ cần khi type="mute")
        """
        super().__init__(parent)

        # Kích thước: gần tràn hết chiều ngang vùng chat
        # NOTE: chỉnh kích thước tại 2 dòng dưới đây
        CARD_W = 1170   # ← sửa chiều rộng tại đây
        CARD_H = 210    # ← sửa chiều cao tại đây
        self.setFixedSize(CARD_W, CARD_H)

        # Gradient -60°: #38D45F (gốc) → #2EAA4C (tối hơn 20%)
        # Qt tọa độ: x1:0,y1:0 = góc trên-trái; x2:0.5,y2:0.87 = góc dưới-phải
        # Tỉ lệ 0.5:0.87 ≈ tan(60°)/2 — tạo góc nghiêng 60° thực tế
        #
        # LƯU Ý — Tại sao phải setAttribute(WA_StyledBackground) + dùng "QFrame"?
        # Qt stylesheet chỉ nhận selector tên class BUILT-IN (QFrame, QLabel...).
        # Tên class Python tùy chỉnh "SystemNoticeCard" bị bỏ qua silently → widget
        # render trong suốt, không hiện màu. setAttribute ép Qt vẽ nền từ stylesheet.
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
            QFrame {
                background-color: qlineargradient(
                    x1:0, y1:0,
                    x2:0.5, y2:0.87,
                    stop:0.0  #38D45F,
                    stop:1.0  #2EAA4C
                );
                border-radius: 3px;
                border: none;
            }
            QLabel { border: none; background: transparent; }
        """)

        # Shadow nhẹ để card nổi lên khỏi nền chat trắng
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(18)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(38, 212, 95, 120))   # glow xanh lá nhẹ
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # -------------------------------------------------------
        # DÒNG 1: TIÊU ĐỀ (23px, Roboto Bold)
        # NOTE: kích thước font tiêu đề tại setPixelSize bên dưới
        # -------------------------------------------------------
        if notice_type == "quota":
            title_text = "⛔  Đã đạt giới hạn phiên chat"
        else:
            title_text = "⚠️  Hệ thống tạm dừng — Nhu cầu cao"

        lbl_title = QLabel(title_text)
        font_title = QFont("Roboto")
        font_title.setPixelSize(23)         # ← sửa cỡ tiêu đề tại đây
        font_title.setWeight(QFont.Weight.Bold)
        lbl_title.setFont(font_title)
        lbl_title.setStyleSheet("color: white;")

        # -------------------------------------------------------
        # DÒNG 2: NỘI DUNG CHÍNH (16px, Roboto Regular)
        # NOTE: kích thước font nội dung tại setPixelSize bên dưới
        # -------------------------------------------------------
        if notice_type == "quota":
            body_text = (
                "Bạn đã sử dụng hết 45 lượt nhắn tin trong phiên này. "
                "Đây là giới hạn hệ thống nhằm đảm bảo chất lượng tư vấn cho tất cả người dùng.\n"
                f"Hệ thống sẽ tự động mở lại sau {guard.RESET_HOURS} tiếng kể từ tin nhắn đầu tiên của phiên. "
                "Cảm ơn bạn đã sử dụng GritalystAI! 🌿"
            )
        else:
            remaining = guard.mute_remaining() if guard else "10:00"
            body_text = (
                "GritalystAI ghi nhận phiên này có một số yêu cầu vượt ngoài phạm vi tư vấn sức khỏe.\n"
                "Hệ thống tạm dừng để lấy lại trạng thái phục vụ tốt nhất. "
                f"Vui lòng thử lại sau: {remaining}"
            )

        lbl_body = QLabel(body_text)
        font_body = QFont("Roboto")
        font_body.setPixelSize(16)          # ← sửa cỡ nội dung tại đây
        lbl_body.setFont(font_body)
        lbl_body.setStyleSheet("color: rgba(255, 255, 255, 0.92);")
        lbl_body.setWordWrap(True)

        layout.addWidget(lbl_title)
        layout.addWidget(lbl_body)


# =====================================================================
# HÀM NẠP FONT — đăng ký Orbitron + Roboto vào hệ thống Qt
# Phải gọi 1 lần trước khi dùng QFont("Orbitron")
# =====================================================================
def load_gritalyst_fonts():
    """
    Nạp 3 file Orbitron + toàn bộ Roboto từ thư mục assets/fooderai-fonts.
    QFontDatabase.addApplicationFont() đăng ký font vào Qt runtime —
    sau đó mới có thể gọi QFont("Orbitron") hay QFont("Roboto") đúng.
    """
    from PySide6.QtGui import QFontDatabase
    font_dir = os.path.join("assets", "fooderai-fonts")

    # Danh sách đầy đủ theo ảnh thư mục: Orbitron 3 file + Roboto các biến thể
    font_files = [
        "Orbitron-Bold.ttf",
        "Orbitron-Medium.ttf",
        "Orbitron-Regular.ttf",
        "Roboto_SemiCondensed-Light.ttf",
        "Roboto_SemiCondensed-Medium.ttf",
        "Roboto_SemiCondensed-Regular.ttf",
        "Roboto-Black.ttf",
        "Roboto-Bold.ttf",
        "Roboto-Light.ttf",
        "Roboto-Medium.ttf",
        "Roboto-Regular.ttf",
    ]
    for f in font_files:
        path = os.path.join(font_dir, f)
        if os.path.exists(path):
            QFontDatabase.addApplicationFont(path)


# Đường dẫn ảnh logo — dùng chung ở cả 3 chỗ: avatar bubble, avatar banner, logo widget
_LOGO_PATH = os.path.join("assets", "fooderai-chatbot", "gritalyst-ai-logo.png")


# =====================================================================
# LỚP 4: GRITALYSTAVATAR — LOAD ẢNH PNG THAY VÌ VẼ TAY
# =====================================================================
class GritalystAvatar(QLabel):
    """
    Avatar hình tròn dùng ảnh PNG logo thật.
    Kế thừa QLabel thay vì QWidget vì QLabel có sẵn setPixmap().
    Size mặc định 46px cho header banner, 36px cho bubble chat.
    """
    def __init__(self, size=46, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)  # khóa cứng, không cho co giãn
        self.setStyleSheet("border: none; background: transparent;")

        if os.path.exists(_LOGO_PATH):
            # scaledToWidth: scale giữ tỉ lệ theo chiều rộng
            # SmoothTransformation: dùng thuật toán nội suy mịn (chống răng cưa)
            pix = QPixmap(_LOGO_PATH).scaled(
                size, size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.setPixmap(pix)
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            # Fallback: hiện chữ "G" nếu không tìm thấy file
            self.setText("G")
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)


# =====================================================================
# LỚP 4B: LOGOWIDGET — LOGO 300px + TÊN + SLOGAN (dùng trong chat header)
# Widget này được đặt vào đầu chat_layout để cuộn cùng với tin nhắn
# =====================================================================
class LogoWidget(QWidget):
    """
    Khối logo trung tâm gồm:
    - Ảnh logo tròn 300x300
    - Tên "GritalystAI" font Orbitron Bold màu đen
    - Slogan font Roboto SemiCondensed màu xám

    Đặt vào đầu chat_layout → sẽ cuộn lên khi user nhắn tin.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # --- Ảnh logo 300x300 ---
        lbl_logo = QLabel()
        lbl_logo.setFixedSize(132, 132)
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_logo.setStyleSheet("border: none; background: transparent;")

        if os.path.exists(_LOGO_PATH):
            pix = QPixmap(_LOGO_PATH).scaled(
                132, 132, #kích thước mói: 3.5 cm x 3.5 cm
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            lbl_logo.setPixmap(pix)
        else:
            lbl_logo.setText("[ Logo ]")  # placeholder nếu file chưa có

        # --- Tên "GritalystAI" — Orbitron Bold, đen, to ---
        lbl_name = QLabel("GritalystAI")
        font_name = QFont("Orbitron")          # họ font đã nạp từ load_gritalyst_fonts()
        font_name.setPixelSize(28)
        font_name.setWeight(QFont.Weight.Bold) # Bold = 700
        lbl_name.setFont(font_name)
        lbl_name.setStyleSheet("color: #111111; border: none; background: transparent;")
        lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Slogan — Roboto SemiCondensed, xám nhạt ---
        lbl_slogan = QLabel("Đồng hành sức khỏe — Dinh dưỡng thông minh, mỗi ngày.")
        font_slogan = QFont("Roboto")
        font_slogan.setPixelSize(14)
        font_slogan.setStretch(QFont.Stretch.SemiCondensed)  # ép thành SemiCondensed
        lbl_slogan.setFont(font_slogan)
        lbl_slogan.setStyleSheet("color: #6A8A7A; border: none; background: transparent;")
        lbl_slogan.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(lbl_logo,    alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(lbl_name,    alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(lbl_slogan,  alignment=Qt.AlignmentFlag.AlignHCenter)


# =====================================================================
# LỚP 5: PAGEAIASSISTANT — TRANG CHÍNH GHÉP TẤT CẢ LẠI
# =====================================================================
class PageAIAssistant(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1240, 640)  # kích thước cố định khớp với feature_stack trong main

        # Khởi tạo bộ bảo vệ NSFW — dùng xuyên suốt phiên chat
        self.guard = NSFWGuard()

        # Style cho toàn bộ trang: nền trắng, viền teal mờ, góc bo 24px
        self.setStyleSheet("""
            PageAIAssistant {
                background-color: white;
                border: 3px solid rgba(0, 77, 77, 0.5);
                border-radius: 24px;
            }
        """)

        # Đổ bóng nhẹ cho cả trang để nổi lên trên nền app
        box_shadow = QGraphicsDropShadowEffect()
        box_shadow.setBlurRadius(5)
        box_shadow.setOffset(0, 3)               # bóng lệch xuống 3px
        box_shadow.setColor(QColor(150, 150, 150, 180))
        self.setGraphicsEffect(box_shadow)

        # Layout dọc chính: Banner → Vùng chat → Thanh nhập
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 10, 15, 10)
        main_layout.setSpacing(8)  # khoảng cách giữa 3 vùng

        # ===========================================================
        # PHẦN 1: BANNER GRITALYSTAI
        # ===========================================================
        self.banner = QFrame()
        self.banner.setFixedSize(1210, 70)  # rộng hết trang, cao 70px

        # Tính màu gradient động từ màu gốc #3DE365
        color_hex = "#3DE365"
        base_color = QColor(color_hex)
        color_80  = base_color.darker(108).name()  # tối hơn 8% → dùng cho stop giữa
        color_100 = base_color.darker(124).name()  # tối hơn 24% → dùng cho stop cuối

        # Gradient chạy từ trái-giữa (x1:0, y1:0.2) sang phải-dưới (x2:1, y2:1)
        # y1:0.2 thay vì 0 để gradient không bắt đầu từ góc trên-trái mà từ giữa-trái
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

        # Bóng nhẹ phía dưới banner
        banner_shadow = QGraphicsDropShadowEffect()
        banner_shadow.setBlurRadius(6)
        banner_shadow.setOffset(0, 2)
        banner_shadow.setColor(QColor(0, 0, 0, 160))
        self.banner.setGraphicsEffect(banner_shadow)

        # Layout ngang bên trong banner: [Avatar] [Tên + Subtitle] [---stretch---]
        banner_layout = QHBoxLayout(self.banner)
        banner_layout.setContentsMargins(8, 0, 8, 0)
        banner_layout.setSpacing(12)

        # Avatar hình tròn chữ G — size 46px cho header
        self.avatar_header = GritalystAvatar(size=46)

        # Cột dọc chứa 2 dòng chữ (tên + subtitle)
        name_col = QVBoxLayout()
        name_col.setSpacing(2)                                    # 2px giữa 2 dòng
        name_col.setContentsMargins(0, 0, 0, 0)
        name_col.setAlignment(Qt.AlignmentFlag.AlignVCenter)     # căn giữa theo chiều dọc

        # Dòng 1: Tên "GritalystAI" — to, đậm, trắng
        lbl_name = QLabel("GritalystAI")
        font_name = QFont("Orbitron")
        font_name.setPixelSize(17)
        font_name.setWeight(QFont.Weight.Bold)
        """
        Orbitron Bold 16px = font thương hiệu GritalystAI
        Nhỏ hơn 22px cũ nhưng đúng identity — Orbitron có
        nét dày nên 16px vẫn rõ trên nền gradient xanh lá
        """

        lbl_name.setFont(font_name)
        lbl_name.setStyleSheet("color: white; border: none; background: transparent;")

        # Shadow thẳng đứng (offset 0,3) → chữ nổi lên, không bị lẫn vào nền gradient
        shadow_name = QGraphicsDropShadowEffect()
        shadow_name.setBlurRadius(6)
        shadow_name.setOffset(0, 3)                   # bóng thẳng xuống dưới
        shadow_name.setColor(QColor(0, 60, 0, 200))   # xanh đậm, alpha 200/255
        lbl_name.setGraphicsEffect(shadow_name)

        # Dòng 2: Subtitle — nhỏ hơn, trắng mờ 80%
        lbl_sub = QLabel("Hệ thống AI hỗ trợ về dinh dưỡng và sức khỏe của bạn")
        font_sub = QFont("Roboto")
        font_sub.setPixelSize(12)
        lbl_sub.setFont(font_sub)
        lbl_sub.setStyleSheet("color: rgba(255,255,255,0.8); border: none; background: transparent;")

        # Shadow nhẹ hơn dòng tên (blur 4 thay vì 6, alpha 140 thay vì 200)
        shadow_sub = QGraphicsDropShadowEffect()
        shadow_sub.setBlurRadius(4)
        shadow_sub.setOffset(0, 2)
        shadow_sub.setColor(QColor(0, 60, 0, 140))
        lbl_sub.setGraphicsEffect(shadow_sub)

        name_col.addWidget(lbl_name)
        name_col.addWidget(lbl_sub)

        # Ghép vào banner: Avatar → cột tên → stretch (đẩy hết sang phải)
        banner_layout.addWidget(self.avatar_header, alignment=Qt.AlignmentFlag.AlignVCenter)
        banner_layout.addLayout(name_col)
        banner_layout.addStretch()

        main_layout.addWidget(self.banner, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # ===========================================================
        # PHẦN 2: VÙNG CHAT (ScrollArea + Overlay bịt mõm)
        # ===========================================================

        # Container trong suốt bao quanh scroll — dùng để overlay bịt mõm biết phủ vào đâu
        self.chat_container = QFrame()
        self.chat_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.chat_container.setStyleSheet("QFrame { background: transparent; border: none; }")

        container_layout = QVBoxLayout(self.chat_container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        # ScrollArea: tự thêm thanh scroll khi nội dung dài hơn khung
        # setWidgetResizable(True): widget bên trong co giãn theo khung scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical {
                width: 6px;                  /* thanh scroll mỏng 6px */
                background: #F0F0F0;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: #3DE365;         /* tay cầm màu xanh lá */
                border-radius: 3px;
                min-height: 20px;            /* tối thiểu 20px để dễ kéo */
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical { height: 0; }  /* ẩn nút mũi tên */
        """)

        # Widget thật chứa các bubble — nằm bên trong ScrollArea
        self.chat_widget = QWidget()
        self.chat_widget.setStyleSheet("background: transparent;")

        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.setContentsMargins(10, 10, 10, 10)
        self.chat_layout.setSpacing(6)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # LogoWidget nằm TRONG chat_layout → cuộn cùng với các bubble
        # Khi user nhắn tin nhiều, logo tự cuộn lên trên và biến mất như ChatGPT
        self.logo_widget = LogoWidget()
        self.chat_layout.addWidget(self.logo_widget,
                                   alignment=Qt.AlignmentFlag.AlignHCenter)  # ← vào đây

        self.scroll_area.setWidget(self.chat_widget)
        container_layout.addWidget(self.scroll_area)

        # BUG FIX: Đã XÓA dòng self.mute_overlay = MuteOverlay(...)
        # MuteOverlay (overlay phủ màn hình cũ) không còn dùng nữa —
        # đã thay bằng SystemNoticeCard inline trong chat_layout.
        # Nếu để lại: widget vô hình vẫn được tạo, chiếm memory,
        # và có thể intercept mouse event do nằm trên layer trên cùng.

        # Tham số "1" ở đây là stretch factor — vùng chat chiếm hết phần còn lại sau banner và input
        main_layout.addWidget(self.chat_container, 1)

        # ===========================================================
        # PHẦN 3: THANH NHẬP CHAT (Input + Nút gửi)
        # ===========================================================
        input_row = QHBoxLayout()
        input_row.setSpacing(10)         # khoảng cách giữa ô nhập và nút gửi
        input_row.setContentsMargins(0, 0, 0, 0)

        # Ô nhập liệu
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Nhắn gì đó với Gritalyst...")
        self.input_box.setFixedHeight(50)
        self.input_box.setMaxLength(450)  # giới hạn 450 ký tự, ngăn spam dài

        font_input = QFont("Roboto")
        font_input.setPixelSize(15)
        self.input_box.setFont(font_input)

        # Style capsule (bo tròn 2 đầu bằng border-radius bằng nửa chiều cao)
        self.input_box.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.92);
                color: #1A2A3A;
                border-radius: 25px;
                border: 2px solid rgba(61, 227, 101, 0.5);
                padding: 0px 20px;
            }
            QLineEdit:focus {
                border: 2px solid #3DE365;   /* viền sáng lên khi đang gõ */
                background-color: #FFFFFF;
            }
        """)

        # Glow xanh nhẹ cho ô nhập — QColor(61, 227, 101, 90) là màu RGBA
        # 61,227,101 = #3DE365 viết theo số thập phân; 90 = alpha (35% trong suốt)
        shadow_input = QGraphicsDropShadowEffect()
        shadow_input.setBlurRadius(18)
        shadow_input.setOffset(0, 4)
        shadow_input.setColor(QColor(61, 227, 101, 90))
        self.input_box.setGraphicsEffect(shadow_input)

        # Nút gửi — hình tròn 50x50, không có chữ, chỉ có icon mũi tên
        self.btn_send = QPushButton()
        self.btn_send.setFixedSize(50, 50)  # width = height → hình tròn khi border-radius = 25

        # Nạp icon từ file PNG — nếu không tìm thấy thì nút vẫn chạy, chỉ không có icon
        icon_path = os.path.join("assets", "fooderai-chatbot", "fooderai-ai-submit.png")
        if os.path.exists(icon_path):
            self.btn_send.setIcon(QIcon(icon_path))
            self.btn_send.setIconSize(QSize(28, 28))  # icon 28px nằm giữa nút 50px

        # Gradient chạy chéo 45° từ trên-trái → dưới-phải (x1:0,y1:0 → x2:1,y2:1)
        self.btn_send.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3DE365, stop:0.75 #2FC455, stop:1.0 #27A849);
                border-radius: 25px;   /* = nửa chiều cao → hình tròn hoàn hảo */
                border: none;
            }
            QPushButton:hover   { background: #4AEF70; }   /* sáng hơn khi hover */
            QPushButton:pressed { background: #27A849; }   /* tối hơn khi nhấn */
        """)

        # Bóng xanh cho nút gửi — màu lấy từ #27A849 viết dạng RGBA
        # BUG FIX: lưu vào self._shadow_btn thay vì local variable shadow_btn
        # Lý do: _lock_input() cần gọi setGraphicsEffect(None) để xóa shadow này
        # trước khi đổi stylesheet xám. Nếu chỉ là local var thì sau __init__
        # biến mất khỏi scope nhưng Qt vẫn giữ reference nội bộ — setGraphicsEffect(None)
        # trên widget vẫn hoạt động đúng. Lưu vào self để dễ debug sau này.
        self._shadow_btn = QGraphicsDropShadowEffect()
        self._shadow_btn.setBlurRadius(14)
        self._shadow_btn.setOffset(0, 4)
        self._shadow_btn.setColor(QColor(39, 168, 73, 160))
        self.btn_send.setGraphicsEffect(self._shadow_btn)

        # Khi chuột di vào nút → con trỏ đổi thành bàn tay 👆
        self.btn_send.setCursor(Qt.CursorShape.PointingHandCursor)

        input_row.addWidget(self.input_box, 1)  # stretch=1 → ô nhập chiếm hết phần còn lại
        input_row.addWidget(self.btn_send)       # nút gửi kích thước cố định, không co giãn
        main_layout.addLayout(input_row)

        # Kết nối signal → slot:
        # clicked = signal phát ra khi nhấn nút chuột
        # returnPressed = signal phát ra khi nhấn phím Enter trong QLineEdit
        # Cả 2 đều dẫn đến cùng 1 hàm _send_message — không cần viết 2 hàm riêng
        self.btn_send.clicked.connect(self._send_message)
        self.input_box.returnPressed.connect(self._send_message)

        # Tin nhắn chào mừng tự động khi mở trang
        self._add_bot_bubble("Chào bạn! Tôi là GritalystAI — trợ lý dinh dưỡng và thể dục của bạn. Tôi có thể giúp gì cho bạn hôm nay? 🌿")

    def resizeEvent(self, event):
        """
        Qt tự gọi hàm này mỗi khi widget thay đổi kích thước.
        BUG FIX: Đã xóa block check mute_overlay vì MuteOverlay (lớp overlay cũ)
        không còn được khởi tạo trong __init__ nữa — đã thay bằng SystemNoticeCard
        inline trong chat. Giữ lại resizeEvent nhưng chỉ gọi super() để tránh
        AttributeError khi Qt resize widget lần đầu.
        """
        super().resizeEvent(event)

    def _add_bot_bubble(self, text: str):
        """Thêm 1 tin nhắn của Gritalyst vào cuối danh sách chat (căn trái)."""
        row = QHBoxLayout()
        row.setSpacing(8)
        row.setContentsMargins(0, 0, 0, 0)

        avatar = GritalystAvatar(size=36)           # avatar nhỏ hơn header (36 thay vì 46)
        bubble = ChatBubble(text, is_user=False)    # is_user=False → bubble trắng bên trái

        # AlignTop: avatar luôn căn trên dù bubble có cao bao nhiêu
        row.addWidget(avatar, alignment=Qt.AlignmentFlag.AlignTop)
        row.addWidget(bubble)
        row.addStretch()  # đẩy bubble ôm bên trái

        # Bọc row vào 1 QWidget để có thể addWidget vào chat_layout
        wrapper = QWidget()
        wrapper.setStyleSheet("background: transparent;")
        wrapper.setLayout(row)
        self.chat_layout.addWidget(wrapper)
        self._scroll_to_bottom()

    def _add_user_bubble(self, text: str):
        """Thêm 1 tin nhắn của user vào cuối danh sách chat (căn phải)."""
        bubble = ChatBubble(text, is_user=True)  # is_user=True → bubble xanh bên phải
        self.chat_layout.addWidget(bubble)
        self._scroll_to_bottom()

    def _add_system_notice(self, notice_type: str):
        """
        Thêm thẻ thông báo hệ thống (SystemNoticeCard) vào giữa vùng chat.
        - Không có avatar — đây là thông báo của HỆ THỐNG, không phải Gritalyst
        - Card căn giữa theo chiều ngang bằng wrapper + AlignHCenter
        - Sau khi gọi xong → disable input + btn_send

        notice_type: 'quota' = hết 45 tin | 'mute' = bị khóa NSFW

        Tại sao scroll delay 200ms thay vì 50ms?
        Card cao 210px — Qt cần nhiều thời gian hơn bubble thông thường để
        tính lại toàn bộ chiều cao chat_widget trước khi scrollbar.maximum()
        phản ánh đúng vị trí cuối. 200ms đủ để layout pass hoàn tất.
        """
        card = SystemNoticeCard(notice_type, guard=self.guard)

        wrapper = QWidget()
        wrapper.setStyleSheet("background: transparent;")
        row = QHBoxLayout(wrapper)
        row.setContentsMargins(0, 12, 0, 12)
        row.addStretch()
        row.addWidget(card)
        row.addStretch()

        self.chat_layout.addWidget(wrapper)

        # 200ms: chờ Qt tính lại chiều cao layout trước khi scroll
        QTimer.singleShot(200, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))

        # Lock input sau khi card đã vào layout
        self._lock_input()

    def _scroll_to_bottom(self):
        """
        Cuộn ScrollArea xuống tin nhắn mới nhất.
        Dùng QTimer.singleShot(50ms) vì layout cần thêm 1 chút thời gian
        để tính toán chiều cao bubble mới trước khi biết vị trí maximum.
        """
        QTimer.singleShot(50, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))

    def _send_message(self):
        """
        Hàm xử lý chính khi user gửi tin — được gọi từ cả nút Gửi lẫn phím Enter.

        Luồng xử lý:
        1. Lấy text, bỏ qua nếu trống
        2. Xóa ô nhập + hiện bubble user ngay lập tức
        3. Hỏi NSFWGuard xem có được gửi không
        4. Nếu bị chặn (quota/mute): dùng QTimer.singleShot(0) để hiện
           SystemNoticeCard VÀ lock input SAU KHI hàm này return xong.
           → Tại sao phải singleShot(0)?
             _lock_input() gọi btn_send.clicked.disconnect() ngay trong lúc
             signal clicked đang kích hoạt hàm này → Qt phát warning và card
             không render kịp. singleShot(0) đẩy việc đó ra event loop tiếp theo,
             đảm bảo hàm hiện tại đã return hoàn toàn trước khi disconnect.
        5. Nếu OK: kiểm tra NSFW → phản hồi tương ứng → cập nhật nút
        """
        text = self.input_box.text().strip()  # strip() xóa khoảng trắng 2 đầu
        if not text:
            return  # không làm gì nếu ô trống

        # Xóa ô nhập + hiện bubble user ngay — trước khi kiểm tra bất kỳ thứ gì
        # BUG FIX: xóa dòng self.input_box.clear() thừa ở dưới (dòng cũ 789)
        # Trước đây có 2 lần clear(): 1 ở đây và 1 sau block "if not ok" →
        # nếu ok=False thì clear() chạy 2 lần (không hại nhưng thừa và confusing)
        self.input_box.clear()
        self._add_user_bubble(text)

        # Cổng kiểm tra — NSFWGuard quyết định có cho gửi không
        ok, reason = self.guard.can_send()

        if not ok:
            if reason == "muted":
                self._add_system_notice("mute")
            else:
                self._add_system_notice("quota")
            return

        # Kiểm tra NSFW bằng từ khóa đơn giản
        # any() trả về True nếu có ÍT NHẤT 1 từ trong list xuất hiện trong text
        # text.lower() để tìm không phân biệt hoa thường
        nsfw_words = [
            # Từ tục trực tiếp
            "cặc", "cu", "lồn", "địt", "đéo", "đĩ", "cave", "điếm",
            "dâm", "thủ dâm", "xuất tinh", "đụ",
            # Viết tắt
            "cc", "đcm", "đcmm", "đm", "clm", "vcl",
            # Cụm tục
            "địt con mẹ", "đụ má mày", "có cái lồn",
            "cái lồn mẹ mày", "con đĩ mẹ",
        ]
        is_nsfw = any(w in text.lower() for w in nsfw_words)

        if is_nsfw:
            reply, cost = self.guard.record_nsfw()  # ghi nhận vi phạm, lấy câu phản hồi
            if reply == "__muted__":
                self._add_system_notice("mute")
                return
            else:
                self._add_bot_bubble(reply)  # hiện câu cảnh báo tương ứng cấp độ
        else:
            self.guard.record_clean()  # ghi nhận tin sạch, reset streak
            # TODO: gọi Anthropic API tại đây, hiện tại phản hồi tĩnh
            self._add_bot_bubble("Gritalyst đã nhận câu hỏi của bạn! (Chức năng AI đang được kết nối...)")

        self._update_send_button()  # cập nhật trạng thái nút sau mỗi lần gửi

    def _show_mute_overlay(self):
        """
        Thay vì bubble AI, hiện SystemNoticeCard kiểu 'mute' trong chat.
        - Không có icon Gritalyst vì đây là thông báo hệ thống
        - _lock_input() được gọi bên trong _add_system_notice
        """
        self._add_system_notice("mute")

    def _lock_input(self):
        """
        Khóa hoàn toàn thanh nhập sau khi hiện SystemNoticeCard.
        - User vẫn gõ chữ trong ô input được (QLineEdit không bị disable)
        - Nhưng Enter bị ngắt → không gửi được
        - Nút gửi bị vô hiệu hóa + xám + cursor gạch chéo (ForbiddenCursor)

        Tại sao KHÔNG setEnabled(False) trên input_box?
        - Nếu disable input_box, ô sẽ xám xịt và user không gõ được gì,
          trông như app bị treo — trải nghiệm không tốt.
        - Thay vào đó: cho gõ thoải mái nhưng Enter/nút không phản hồi
          → user hiểu rõ "tôi vẫn ở đây, nhưng hệ thống đang chờ".

        Cursor ForbiddenCursor vs file .cur/.ico?
        - Qt.CursorShape.ForbiddenCursor = con trỏ ⊘ built-in của hệ điều hành
        - Ưu điểm: không cần file ngoài, hiển thị đúng trên Windows/macOS/Linux
        - Nếu muốn dùng file tùy chỉnh: dùng QCursor(QPixmap("path/prohibited.cur"))
          NOTE: Windows hỗ trợ cả .ico và .cur; macOS/Linux chỉ dùng QPixmap PNG
          → Khuyến nghị: dùng PNG 32x32 với điểm hotspot (16,16) cho đa nền tảng
          → assets/fooderai-chatbot/prohibited-cursor.png (nếu muốn customize sau)
        """
        # Ngắt Enter
        try:
            self.input_box.returnPressed.disconnect(self._send_message)
        except RuntimeError:
            pass

        # Ngắt click nút gửi
        try:
            self.btn_send.clicked.disconnect(self._send_message)
        except RuntimeError:
            pass

        # Xóa shadow để stylesheet xám hiển thị đúng (Qt 1 widget = 1 effect)
        self.btn_send.setGraphicsEffect(None)

        # Disable nút
        self.btn_send.setEnabled(False)

        # Cursor từ file — QPixmap KHÔNG đọc được .cur binary trực tiếp.
        # Qt trên Windows load .cur thông qua WinAPI, không qua QPixmap.
        # Giải pháp đúng: dùng file .png cùng thư mục (prohibited-cursor.cur.png)
        # vì QPixmap đọc PNG bình thường và QCursor nhận QPixmap.
        # Thứ tự ưu tiên: PNG → ForbiddenCursor built-in
        _png_path = os.path.join("assets", "fooderai-chatbot", "prohibited-cursor.cur.png")
        _cur_path = os.path.join("assets", "fooderai-chatbot", "prohibited-cursor.cur")
        if os.path.exists(_png_path):
            _pix = QPixmap(_png_path)
            # hotspot (0,0): điểm tác động góc trên-trái — phù hợp icon dạng gạch chéo
            # đổi thành (16,16) nếu muốn điểm tác động nằm chính giữa icon 32x32
            self.btn_send.setCursor(QCursor(_pix, 0, 0))
        elif os.path.exists(_cur_path):
            # Thử load .cur — hoạt động nếu Qt build với WinAPI cursor support
            _pix = QPixmap(_cur_path)
            if not _pix.isNull():
                self.btn_send.setCursor(QCursor(_pix, 0, 0))
            else:
                self.btn_send.setCursor(Qt.CursorShape.ForbiddenCursor)
        else:
            self.btn_send.setCursor(Qt.CursorShape.ForbiddenCursor)

        # Nút xám desaturate — giữ nguyên icon mũi tên, chỉ đổi nền
        self.btn_send.setStyleSheet("""
            QPushButton {
                background-color: #909090;
                border-radius: 25px;
                border: none;
            }
            QPushButton:disabled { background-color: #909090; }
        """)

    def _update_send_button(self):
        """
        Cập nhật trạng thái nút gửi + phím Enter sau mỗi lần gửi tin.
        Gọi sau mỗi _send_message() để đồng bộ UI với trạng thái NSFWGuard.

        Lưu ý: khi _lock_input() đã được gọi (quota/mute), hàm này chỉ
        đảm bảo trạng thái đúng chứ không unlock — unlock chỉ xảy ra
        khi quota được reset (sau RESET_HOURS) hoặc mute hết hạn.

        Tại sao KHÔNG dùng blockSignals(True) cho input_box?
        - blockSignals(True) tắt TẤT CẢ signal của widget đó,
          bao gồm cả textChanged, textEdited... có thể gây side effect
          nếu sau này ta cần lắng nghe các signal đó (ví dụ: đếm ký tự).
        - Thay vào đó, ta disconnect() ĐÚNG signal cần chặn (returnPressed)
          và connect() lại khi cần — phẫu thuật chính xác, không ảnh hưởng gì khác.

        Tại sao dùng try/except quanh disconnect()?
        - disconnect() trong Qt sẽ ném RuntimeError nếu signal đó
          chưa được connect hoặc đã bị disconnect trước đó.
        - Dùng try/except để bỏ qua lỗi đó một cách an toàn —
          vì ta chỉ cần "chắc chắn nó đã bị ngắt", không cần biết
          nó có đang kết nối hay không.

        Tại sao phải setGraphicsEffect(None) trước khi đổi stylesheet?
        - Qt chỉ cho mỗi widget giữ ĐÚNG 1 GraphicsEffect tại 1 thời điểm.
        - shadow_btn đang chiếm slot đó từ lúc khởi tạo.
        - Nếu không xóa shadow trước, stylesheet màu xám sẽ bị shadow
          override và không có tác dụng trực quan.
        - setGraphicsEffect(None) giải phóng slot → stylesheet mới
          được Qt render đúng.
        """
        # Nếu đang bị mute (NSFW) → giữ locked
        if self.guard.is_muted():
            self._lock_input()
            return

        quota_ok = self.guard.msg_count < self.guard.MAX_MSGS

        if quota_ok:
            # ===========================================================
            # CÒN LƯỢT — khôi phục toàn bộ về trạng thái hoạt động
            # ===========================================================

            # Bước 1: Kết nối lại phím Enter → _send_message.
            # disconnect() trước để tránh connect() bị gọi 2 lần
            # (nếu connect 2 lần thì 1 lần Enter sẽ gọi _send_message 2 lần!).
            # try/except để bỏ qua nếu chưa từng bị disconnect.
            try:
                self.input_box.returnPressed.disconnect(self._send_message)
            except RuntimeError:
                pass  # chưa bị disconnect → không cần làm gì
            self.input_box.returnPressed.connect(self._send_message)

            # Bước 2: Bật lại nút gửi — setEnabled(True) cho phép click
            self.btn_send.setEnabled(True)

            # Bước 3: Con trỏ bàn tay 👆 khi hover vào nút
            self.btn_send.setCursor(Qt.CursorShape.PointingHandCursor)

            # Bước 4: Khôi phục màu gradient xanh lá ban đầu
            self.btn_send.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #3DE365, stop:0.75 #2FC455, stop:1.0 #27A849);
                        border-radius: 25px;
                        border: none;
                    }
                    QPushButton:hover   { background: #4AEF70; }
                    QPushButton:pressed { background: #27A849; }
                """)

        else:
            # ===========================================================
            # HẾT LƯỢT hoặc bị MUTE — ủy quyền toàn bộ cho _lock_input()
            # ===========================================================
            self._lock_input()