import os
# [MỚI] Thêm QHBoxLayout (Dàn hàng ngang), QLineEdit (Ô nhập chữ), QEvent (Bắt sự kiện click chuột)
# [MỚI v2] Thêm QScrollArea, QScrollBar, QGridLayout để tạo lưới 2 cột + cuộn
from PySide6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel,
                               QWidget, QGraphicsDropShadowEffect, QLineEdit,
                               QScrollArea, QScrollBar, QGridLayout, QSizePolicy)
from PySide6.QtCore import Qt, QEvent, QRect, QPoint, QSize
from PySide6.QtGui import QFont, QColor, QPixmap, QPainter, QPainterPath, QLinearGradient, QBrush, QPen, QRadialGradient


# =====================================================================
# THANH TÌM KIẾM THÔNG MINH (GIỮ NGUYÊN TỪ PHIÊN TRƯỚC)
# =====================================================================
class CustomSearchBar(QFrame):
     def __init__(self, parent=None):
          super().__init__(parent)
          self.setFixedSize(425, 50)
          self.layout = QHBoxLayout(self)
          self.layout.setContentsMargins(5, 0, 5, 0)
          self.layout.setSpacing(5)

          self.icon_lbl = QLabel()
          self.icon_lbl.setStyleSheet("border: none; background: transparent;")
          icon_path = os.path.join("assets", "fooderai-almanacfood", "mgfy-search-icon.png")
          if os.path.exists(icon_path):
               self.icon_lbl.setPixmap(
                    QPixmap(icon_path).scaledToHeight(24, Qt.TransformationMode.SmoothTransformation))
          else:
               self.icon_lbl.setText("🔍")

          self.input_box = QLineEdit()
          self.input_box.setPlaceholderText("Tìm kiếm món ăn, thức uống, và nhiều thứ khác...")
          font_search = QFont("Roboto", QFont.Weight.Normal)
          font_search.setPixelSize(16)
          self.input_box.setFont(font_search)

          self.layout.addWidget(self.icon_lbl)
          self.layout.addWidget(self.input_box)

          self.style_normal = """
                      QFrame {
                          background-color: white;
                          border-radius: 12px;
                          border-top: 2px solid #888888;
                          border-left: 2px solid #888888;
                          border-bottom: 3px solid #e0e0e0;
                          border-right: 3px solid #e0e0e0;
                      }
                      QLineEdit { background: transparent; border: none; color: #333333; }
                      QLineEdit::placeholder { color: #999999; }
                  """
          self.style_focus = """
                      QFrame {
                          background-color: white;
                          border-radius: 12px;
                          border: 2px solid #31D5E7;
                      }
                      QLineEdit { background: transparent; border: none; color: #333333; }
                  """
          self.setStyleSheet(self.style_normal)
          self.input_box.installEventFilter(self)

          self.glow_effect = QGraphicsDropShadowEffect()
          self.glow_effect.setBlurRadius(20)
          self.glow_effect.setOffset(0, 0)
          self.glow_effect.setColor(QColor(49, 213, 231, 150))
          self.setGraphicsEffect(self.glow_effect)
          self.glow_effect.setEnabled(False)

     def eventFilter(self, obj, event):
          if obj == self.input_box:
               if event.type() == QEvent.Type.FocusIn:
                    self.setStyleSheet(self.style_focus)
                    self.glow_effect.setEnabled(True)
               elif event.type() == QEvent.Type.FocusOut:
                    self.setStyleSheet(self.style_normal)
                    self.glow_effect.setEnabled(False)
          return super().eventFilter(obj, event)


# =====================================================================
# LINH KIỆN MỚI: THẺ MÓN ĂN (FOOD CARD)
# Mỗi ô trong lưới 2 cột là 1 FoodCard
# =====================================================================
class FoodCard(QFrame):
     """
     [GIẢI THÍCH CẤU TRÚC FOOD CARD]
     Mỗi thẻ gồm 3 phần xếp ngang (QHBoxLayout):
     - Bên trái: Ảnh món ăn (80x80px, bo góc)
     - Bên phải: 3 dòng chữ xếp dọc
         + Tên món (font Bold 20px)
         + Số calo (font Medium 14px)
         + Mô tả ngắn (font Regular 14px)
     Hiệu ứng: nền trắng, viền nhạt, hover đổi màu nền nhẹ
     """
     def __init__(self, name, kcal, description, nutrients, pixmap=None, parent=None):
          super().__init__(parent)
          self.food_name = name
          self.food_kcal = kcal
          self.food_description = description
          self.food_nutrients = nutrients
          self.food_pixmap = pixmap

          # Kích thước mỗi thẻ: Chiều rộng tự co theo grid, cao cố định 115px
          self.setFixedHeight(160)      # chỉnh sửa tại đây
          self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
          self.setCursor(Qt.CursorShape.PointingHandCursor)

          # Style bình thường
          self.STYLE_NORMAL = """
               FoodCard {
                    background-color: #EBF4FF;
                    border: 1.5px solid #B8D4F0;
                    border-radius: 14px;
               }
          """
          # Style khi di chuột vào (Hover)
          self.STYLE_HOVER = """
               FoodCard {
                    background-color: #D6EAFF;
                    border: 2px solid #5C94FA;
                    border-radius: 14px;
               }
          """
          self.setStyleSheet(self.STYLE_NORMAL)

          # Drop shadow nhẹ cho thẻ
          card_shadow = QGraphicsDropShadowEffect()
          card_shadow.setBlurRadius(14)
          card_shadow.setOffset(0, 2)
          card_shadow.setColor(QColor(0, 0, 0, 60))
          self.setGraphicsEffect(card_shadow)

          # === BỐ CỤC NỘI DUNG ===
          outer_layout = QHBoxLayout(self)
          outer_layout.setContentsMargins(10, 10, 15, 10)
          outer_layout.setSpacing(12)

          # --- ẢNH MÓN ĂN (Bên trái) ---
          self.lbl_img = QLabel()
          self.lbl_img.setFixedSize(90, 90)
          self.lbl_img.setStyleSheet("""
               QLabel {
                    background-color: #C8DFF8;
                    border-radius: 10px;
                    border: 1px solid #A0C4F0;
               }
          """)
          self.lbl_img.setAlignment(Qt.AlignmentFlag.AlignCenter)

          if pixmap:
               # Scale ảnh khít 90x90, bo góc bằng cách dùng mask
               scaled = pixmap.scaled(90, 90,
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation)
               self.lbl_img.setPixmap(scaled)
          else:
               # Placeholder: hiện chữ "?" khi chưa có ảnh
               self.lbl_img.setText("🍽")
               self.lbl_img.setFont(QFont("Segoe UI Emoji", 28))

          # --- PHẦN TEXT (Bên phải) ---
          text_col = QVBoxLayout()
          text_col.setSpacing(1)
          text_col.setContentsMargins(0, 4, 0, 4)

          # Hàng 1: Tên + Calo (xếp ngang)
          name_row = QHBoxLayout()
          name_row.setSpacing(6)

          lbl_name = QLabel(name)
          name_font = QFont("Roboto")
          name_font.setPixelSize(19)
          name_font.setWeight(QFont.Weight.Bold)
          lbl_name.setFont(name_font)
          lbl_name.setStyleSheet("color: #1A2A4A; border: none; background: transparent;")

          # Badge calo (xanh dương nhỏ)
          lbl_kcal = QLabel(f"{kcal} kcal")
          kcal_font = QFont("Roboto")
          kcal_font.setPixelSize(13)
          kcal_font.setWeight(QFont.Weight.Bold)
          lbl_kcal.setFont(kcal_font)
          lbl_kcal.setStyleSheet("""
               QLabel {
                    background-color: #5C94FA;
                    color: white;
                    border-radius: 8px;
                    padding: 2px 7px;
                    border: none;
               }
          """)
          lbl_kcal.setAlignment(Qt.AlignmentFlag.AlignVCenter)

          name_row.addWidget(lbl_name)
          name_row.addWidget(lbl_kcal)
          name_row.addStretch()

          # Hàng 2: Mô tả ngắn (elide nếu quá dài)
          lbl_desc = QLabel(description)
          desc_font = QFont("Roboto")
          desc_font.setPixelSize(13)
          lbl_desc.setFont(desc_font)
          lbl_desc.setStyleSheet("color: #4A5568; border: none; background: transparent;")
          lbl_desc.setWordWrap(True)


          # Hàng 3: Nhãn dinh dưỡng
          nutrients_str = ", ".join(nutrients[:5]) if nutrients else ""
          lbl_nutrients = QLabel(f"⊕ DINH DƯỠNG: {nutrients_str.upper()}")
          nut_font = QFont("Roboto")
          nut_font.setPixelSize(11)
          nut_font.setWeight(QFont.Weight.Bold)
          lbl_nutrients.setFont(nut_font)
          lbl_nutrients.setStyleSheet("color: #2A7ADB; border: none; background: transparent;")
          lbl_nutrients.setWordWrap(True)

          text_col.addLayout(name_row)
          text_col.addWidget(lbl_desc)
          text_col.addStretch()
          text_col.addWidget(lbl_nutrients)

          outer_layout.addWidget(self.lbl_img)
          outer_layout.addLayout(text_col)

     def enterEvent(self, event):
          """Chuột vào: đổi màu nền sáng hơn"""
          self.setStyleSheet(self.STYLE_HOVER)
          super().enterEvent(event)

     def leaveEvent(self, event):
          """Chuột ra: trả lại màu nền gốc"""
          self.setStyleSheet(self.STYLE_NORMAL)
          super().leaveEvent(event)


# =====================================================================
# LINH KIỆN MỚI: SCROLLBAR TÙNG CHỈNH (BEVEL CUT + QUẢ CẦU)
# Thiết kế theo hình tham khảo: rãnh lõm (bevel inset), quả cầu 3D xanh
# =====================================================================
class BevelScrollBar(QWidget):
     """
     [GIẢI THÍCH KỸ THUẬT VẼ THỦ CÔNG]
     Qt không cho phép style scrollbar phức tạp bằng CSS.
     Giải pháp: Tạo 1 QWidget tùy chỉnh và vẽ toàn bộ bằng QPainter.

     Cấu trúc:
     - Rãnh (Track): Hình chữ nhật bo góc, màu xanh teal đậm, hiệu ứng lõm
       bằng cách vẽ viền sáng ở dưới/phải và viền tối ở trên/trái.
     - Quả cầu (Thumb): Hình tròn, gradient radial 3D, màu xanh #5C94FA
       với điểm sáng lệch góc trên-trái để tạo chiều sâu.

     Kết nối: Khi người dùng kéo quả cầu, phát tín hiệu valueChanged
     để QScrollArea cuộn theo.
     """
     def __init__(self, scroll_area, parent=None):
          super().__init__(parent)
          self.scroll_area = scroll_area   # Tham chiếu đến vùng cuộn cần điều khiển
          self.setFixedWidth(22)           # Thanh cuộn rộng 22px
          self._dragging = False
          self._drag_start_y = 0
          self._drag_start_val = 0

     def paintEvent(self, event):
          """
          [HÀM VẼ CHÍNH - CHẠY MỖI KHI CẦN RENDER LẠI]
          Thứ tự vẽ: Rãnh nền → Bevel inset → Quả cầu 3D
          """
          painter = QPainter(self)
          painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # Bật khử răng cưa

          w = self.width()
          h = self.height()
          track_x = (w - 12) // 2   # Rãnh rộng 12px, căn giữa theo chiều ngang

          # -----------------------------------------------
          # BƯỚC 1: VẼ RÃNH NỀN (TRACK)
          # Màu teal đậm, bo góc 6px
          # -----------------------------------------------
          track_rect = QRect(track_x, 4, 12, h - 8)
          track_path = QPainterPath()
          track_path.addRoundedRect(track_rect, 6, 6)

          # Màu nền rãnh: gradient từ #1A4A5A (đậm) xuống #2A6A7A (nhạt hơn)
          track_grad = QLinearGradient(track_x, 0, track_x + 12, 0)
          track_grad.setColorAt(0.0, QColor("#1A4A5A"))
          track_grad.setColorAt(1.0, QColor("#2E7A8A"))
          painter.fillPath(track_path, QBrush(track_grad))

          # -----------------------------------------------
          # BƯỚC 2: VẼ VIỀN BEVEL (GIẢ LÕM)
          # Viền trên/trái tối hơn → tạo cảm giác rãnh bị lõm xuống
          # Viền dưới/phải sáng hơn → phản sáng
          # -----------------------------------------------
          # Viền lõm phía trong: màu tối #0A2A35
          painter.setPen(QPen(QColor("#0A2A35"), 1))
          painter.drawPath(track_path)

          # Viền highlight phía dưới (phản sáng): vẽ thêm nét sáng ở cạnh phải và dưới
          highlight_path = QPainterPath()
          highlight_path.addRoundedRect(QRect(track_x + 1, 5, 11, h - 10), 5, 5)
          painter.setPen(QPen(QColor(255, 255, 255, 35), 1))
          painter.drawPath(highlight_path)

          # -----------------------------------------------
          # BƯỚC 3: TÍNH VỊ TRÍ QUẢ CẦU DỰA TRÊN GIÁ TRỊ SCROLLBAR
          # -----------------------------------------------
          sb = self.scroll_area.verticalScrollBar()
          sb_min = sb.minimum()
          sb_max = sb.maximum()
          sb_val = sb.value()

          # Chiều cao vùng di chuyển của quả cầu
          ball_d = 18          # Đường kính quả cầu 18px
          travel_h = h - 8 - ball_d   # Khoảng di chuyển thực tế
          if travel_h <= 0:
               travel_h = 1

          # Tỉ lệ vị trí (0.0 → 1.0)
          ratio = (sb_val - sb_min) / max(1, sb_max - sb_min)
          ball_y = 4 + int(ratio * travel_h)     # Tọa độ Y trên cùng của quả cầu
          ball_cx = w // 2                        # Tâm X (căn giữa thanh cuộn)
          ball_cy = ball_y + ball_d // 2          # Tâm Y

          # -----------------------------------------------
          # BƯỚC 4: VẼ QUẢ CẦU 3D (RADIAL GRADIENT)
          # Điểm sáng lệch góc trên-trái tạo cảm giác cầu phình ra
          # -----------------------------------------------
          ball_rect = QRect(ball_cx - ball_d // 2, ball_y, ball_d, ball_d)

          # Gradient radial: tâm sáng (trắng xanh) → viền tối (xanh đậm)
          ball_grad = QRadialGradient(
               ball_cx - ball_d * 0.2,   # Tiêu điểm X lệch trái 20%
               ball_cy - ball_d * 0.25,  # Tiêu điểm Y lệch lên 25%
               ball_d * 0.75             # Bán kính gradient
          )
          ball_grad.setColorAt(0.0, QColor("#AADEFF"))   # Điểm sáng nhất (trắng xanh nhạt)
          ball_grad.setColorAt(0.35, QColor("#5C94FA"))  # Màu xanh chính
          ball_grad.setColorAt(0.7, QColor("#2A5BBF"))   # Xanh trung
          ball_grad.setColorAt(1.0, QColor("#0D2A6A"))   # Viền tối nhất

          painter.setBrush(QBrush(ball_grad))
          painter.setPen(QPen(QColor("#0A2050"), 1))     # Viền ngoài quả cầu rất tối
          painter.drawEllipse(ball_rect)

          # Vệt sáng nhỏ bổ sung (specular highlight) - nét trắng cong nhỏ góc trên trái
          spec_x = ball_cx - ball_d * 0.18
          spec_y = ball_cy - ball_d * 0.28
          spec_r = ball_d * 0.18
          painter.setBrush(QBrush(QColor(255, 255, 255, 180)))
          painter.setPen(Qt.PenStyle.NoPen)
          painter.drawEllipse(
               int(spec_x - spec_r), int(spec_y - spec_r),
               int(spec_r * 2), int(spec_r * 1.2)
          )

     def _get_ball_y_from_event(self, y_pos):
          """Chuyển tọa độ chuột → giá trị scrollbar tương ứng"""
          sb = self.scroll_area.verticalScrollBar()
          ball_d = 18
          travel_h = self.height() - 8 - ball_d
          if travel_h <= 0: return sb.minimum()
          ratio = max(0.0, min(1.0, (y_pos - 4 - ball_d // 2) / travel_h))
          return int(sb.minimum() + ratio * (sb.maximum() - sb.minimum()))

     def mousePressEvent(self, event):
          """Bắt đầu kéo quả cầu"""
          if event.button() == Qt.MouseButton.LeftButton:
               self._dragging = True
               self._drag_start_y = event.position().y()
               self._drag_start_val = self.scroll_area.verticalScrollBar().value()

     def mouseMoveEvent(self, event):
          """Kéo quả cầu → cuộn QScrollArea"""
          if self._dragging:
               new_val = self._get_ball_y_from_event(event.position().y())
               self.scroll_area.verticalScrollBar().setValue(new_val)
               self.update()   # Vẽ lại thanh cuộn

     def mouseReleaseEvent(self, event):
          self._dragging = False

     def wheelEvent(self, event):
          """Cuộn bằng bánh xe chuột trên thanh cuộn"""
          sb = self.scroll_area.verticalScrollBar()
          delta = -event.angleDelta().y() // 3
          sb.setValue(sb.value() + delta)
          self.update()


# =====================================================================
# DỮ LIỆU MẪU — sau này sẽ kết nối DB SQL Server
# Cấu trúc: (tên, kcal, mô_tả_ngắn, [dinh_dưỡng], tên_file_ảnh)
# =====================================================================
FOOD_DATA = {
    # --- Tab 1: Món Ăn (food) — 50 món ---
    "food": [
        ("Phở bò", 150, "Phở bò là biểu tượng của tinh hoa ẩm thực Việt Nam, sự kết hợp tinh tế giữa sợi phở mềm mại và nước dùng xương bò ninh lâu.", ["Protein", "Sắt", "Kẽm", "Vitamin B12", "Canxi"], "fooderai_phobotaichin.png"),
        ("Bún bò Huế", 180, "Bún bò Huế nổi tiếng với nước dùng đậm đà, cay nồng, sợi bún to tròn và miếng thịt bò thơm lừng.", ["Protein", "Sắt", "Phốt pho", "Vitamin B", "Kẽm"], "fooderai_bunboHue.png"),
        ("Cao lầu Hội An", 160, "Đặc sản vùng đất di sản, sợi mì vàng dai đặc trưng chỉ có tại Hội An, ăn kèm thịt xá xíu và rau sống.", ["Tinh bột", "Protein", "Chất xơ", "Vitamin C", "Sắt"], "fooderai_caolauhoian.png"),
        ("Mì Quảng tôm thịt", 290, "Sợi mì Quảng vàng mượt, nước dùng sệt đậm đà, ăn kèm bánh tráng nướng giòn tan.", ["Tinh bột", "Protein", "Chất xơ", "Canxi", "Sắt"], "fooderai_miquangtomthit.png"),
        ("Bánh mì thịt nguội", 220, "Ổ bánh mì giòn tan kẹp thịt nguội, chả lụa, rau thơm — biểu tượng ẩm thực đường phố Việt Nam.", ["Tinh bột", "Protein", "Chất béo", "Vitamin B", "Natri"], "fooderai_banhmithitnguoi.png"),
        ("Cơm tấm sườn bì chả", 580, "Cơm tấm là linh hồn bữa sáng Sài Gòn, kết hợp sườn nướng thơm, bì giòn, chả hấp mềm.", ["Protein", "Tinh bột", "Chất béo", "Vitamin B", "Sắt"], "fooderai_comtamsuonbicha.png"),
        ("Bánh xèo miền Trung", 320, "Bánh xèo giòn rụm với nhân tôm thịt, giá đỗ, cuốn cùng rau sống và chấm nước mắm chua ngọt.", ["Tinh bột", "Protein", "Chất xơ", "Vitamin C", "Canxi"], "fooderai_banhxeo.png"),
        ("Bánh cuốn Hà Nội", 210, "Lớp bánh cuốn mỏng như lụa bao bọc nhân thịt nấm mộc nhĩ thơm lừng.", ["Tinh bột", "Protein", "Chất xơ", "Vitamin B", "Sắt"], "fooderai_banhcuon.png"),
        ("Bún chả Hà Nội", 350, "Bún chả đặc trưng Hà Nội: chả viên và chả miếng nướng thơm, chấm nước mắm pha đúng vị.", ["Protein", "Tinh bột", "Chất xơ", "Vitamin C", "Sắt"], "fooderai_bunchaHaNoi.png"),
        ("Nem lụi Huế", 280, "Nem lụi xào lăn thơm nức mũi, cuốn với bánh tráng và rau sống chấm mắm nêm.", ["Protein", "Chất béo", "Vitamin C", "Chất xơ", "Sắt"], "fooderai_nemluinuong.png"),
        ("Gỏi cuốn tôm thịt", 150, "Gỏi cuốn tươi ngon với tôm, thịt heo, cuộn kèm rau sống, bún tươi và chấm nước tương đậu phộng đậm đà.", ["Protein", "Carbohydrate", "Chất béo", "Vitamin A", "Chất xơ", "Canxi"], "fooderai_goicuon.png"),
        ("Bún đậu mắm tôm", 700, "Mẹt bún đậu đầy đủ với đậu hũ chiên giòn, chả cốm, dồi sụn, thịt luộc ăn kèm rau sống và mắm tôm đánh bông.", ["Protein", "Tinh bột", "Chất béo", "Canxi", "Vitamin A", "Chất xơ"], "fooderai_bundaumamtom.png"),
        ("Chả cá Lã Vọng", 450, "Đặc sản Hà thành với cá lăng ướp nghệ nướng vàng, áp chảo cùng hành lá, thì là, ăn kèm lạc rang và bún tươi.", ["Protein", "Omega-3", "Chất béo", "Tinh bột", "Vitamin C", "Sắt"], "fooderai_chacalavong.png"),
        ("Bánh khọt Vũng Tàu", 460, "Đặc sản biển Vũng Tàu với lớp vỏ bột gạo giòn rụm béo vị nước cốt dừa, nhân tôm tươi, ăn kèm nước mắm chua ngọt.", ["Tinh bột", "Protein", "Chất béo", "Canxi", "Chất xơ", "Kali"], "fooderai_banhkhot.png"),
        ("Bò lá lốt", 350, "Thịt bò băm cuốn lá lốt nướng xém thơm nức mũi, ăn kèm bánh tráng, rau sống, bún tươi và mắm nêm.", ["Protein", "Chất béo", "Sắt", "Chất xơ", "Vitamin C", "Kali"], "fooderai_bolalot.png"),
        ("Bánh bèo Huế", 45, "Chén bánh bèo mướt mịn rắc tôm cháy vàng ươm, tóp mỡ giòn rụm ăn kèm nước mắm ngọt loãng đặc trưng ẩm thực miền Trung.", ["Tinh bột", "Protein", "Chất béo", "Canxi", "Sodium", "Kali"], "fooderai_banhbeoHue.png"),
        ("Bánh căn Phan Rang", 420, "Đặc sản bánh căn hải sản thơm nức với tôm mực tươi rói, trứng cút béo ngậy, ăn kèm xíu mại và nước chấm đậm đà.", ["Protein", "Tinh bột", "Chất béo", "Canxi", "Chất xơ", "Vitamin C"], "fooderai_banhcanPhanRang.png"),
        ("Bún riêu cua", 450, "Tô bún riêu cua đậm đà với mảng riêu béo bùi, đậu hũ chiên giòn, cà chua thanh mát ăn kèm rau sống tươi.", ["Protein", "Canxi", "Tinh bột", "Chất béo", "Chất xơ", "Vitamin C"], "fooderai_bunrieucua.png"),
        ("Hủ tiếu Nam Vang", 400, "Tô hủ tiếu Nam Vang nước dùng thanh ngọt thơm nức tỏi phi, đầy ắp tôm tươi, thịt băm, trứng cút cùng gan heo bổ dưỡng.", ["Protein", "Chất béo", "Tinh bột", "Sắt", "Vitamin A", "Chất xơ"], "fooderai_hutieunamvang.png"),
        ("Cháo lòng truyền thống", 412, "Tô cháo lòng sánh đặc nấu từ nước xương ngọt thanh, đầy ắp dồi huyết, tim gan thơm nồng hạt tiêu hành lá.", ["Protein", "Sắt", "Tinh bột", "Chất béo", "Vitamin B", "Chất xơ"], "fooderai_chaolong.png"),
        ("Bánh tráng trộn Sài Gòn", 280, "Món ăn vặt đường phố Sài Gòn đặc trưng với bánh tráng cắt sợi, tôm khô, trứng cút, xoài xanh và sa tế cay nồng.", ["Tinh bột", "Protein", "Chất xơ", "Vitamin C", "Canxi"], "fooderai_banhtrangtronsg.png"),
        ("Cơm hến Huế", 180, "Cơm hến là món đặc sản cung đình Huế với hến xào thơm lừng, cơm nguội, rau sống đa dạng và nước hến ngọt đậm đà.", ["Canxi", "Sắt", "Tinh bột", "Protein", "Chất xơ", "Vitamin B12"], "fooderai_comhenhue.png"),
        ("Bún mắm miền Tây", 520, "Bún mắm đặc sản miền Tây Nam Bộ với nước lèo từ mắm cá linh đậm đà, thịt heo, tôm cua và rau sống phong phú.", ["Protein", "Tinh bột", "Chất béo", "Sắt", "Vitamin C", "Chất xơ"], "fooderai_bunmammientay.png"),
        ("Cơm cuộn rong biển", 190, "Cơm cuộn rong biển nhiều màu sắc, dễ ăn và phù hợp cho trẻ em lẫn người lớn.", ["Protein", "Canxi", "Vitamin B", "Chất xơ", "I-ốt"], "fooderai_comcuonrongbien.png"),
        ("Sandwich trứng rau", 240, "Sandwich trứng rau mềm nhẹ, cân bằng dinh dưỡng và phù hợp cho bữa ăn nhanh lành mạnh.", ["Protein", "Chất xơ", "Vitamin B", "Canxi", "Kali"], "fooderai_sandwichtrungrau.png"),
        ("Cơm thịt viên rau củ", 340, "Cơm thịt viên rau củ cân bằng dinh dưỡng, mềm dễ ăn và phù hợp cho nhiều độ tuổi.", ["Protein", "Tinh bột", "Vitamin A", "Chất xơ", "Kali", "Vitamin B"], "fooderai_comthitvienraucu.png"),
        ("Thịt kho tàu heo trứng", 480, "Món thịt kho tàu truyền thống với thịt ba chỉ mềm tan, trứng thấm vị nước dừa ngọt đậm đà.", ["Protein", "Chất béo", "Tinh bột", "Vitamin B12", "Sắt", "Kẽm"], "fooderai_thitkhotau.png"),
        ("Rau muống xào tỏi", 85, "Rau muống xào tỏi phi thơm — món ăn quen thuộc của mọi bữa cơm gia đình Việt.", ["Sắt", "Canxi", "Vitamin C", "Chất xơ", "Beta-carotene", "Kali"], "fooderai_raumuongxaotoi.png"),
        ("Trứng chiên hành", 180, "Trứng gà chiên vàng ươm với hành lá thơm — món ăn nhanh gọn, bổ dưỡng cho bữa sáng.", ["Protein", "Chất béo", "Vitamin A", "Vitamin D", "Choline", "Kali"], "fooderai_trungchienhanh.png"),
        ("Canh khổ qua nhồi thịt", 120, "Canh khổ qua nhồi thịt heo băm thanh mát, vị đắng nhẹ thanh nhiệt, đặc trưng bữa cơm miền Nam.", ["Protein", "Vitamin C", "Chất xơ", "Kali", "Sắt", "Canxi"], "fooderai_canhkhoquanhoithit.png"),
        ("Cơm trứng cuộn", 260, "Cơm trứng cuộn mềm thơm với lớp trứng vàng óng, dễ ăn, cân bằng dinh dưỡng và phù hợp cho nhiều độ tuổi.", ["Protein", "Tinh bột", "Vitamin B", "Canxi", "Kali"], "fooderai_comtrungcuon.png"),
        ("Đậu phụ sốt cà chua", 140, "Đậu phụ non mềm mịn sốt cà chua ngọt chua, ăn kèm cơm trắng — món chay thanh đạm dễ làm.", ["Protein", "Canxi", "Lycopene", "Vitamin C", "Sắt", "Magie"], "fooderai_dauphusotcachua.png"),
        ("Súp gà ngô nấm", 165, "Súp gà ngô nấm sánh nhẹ với thịt gà mềm, ngô ngọt tự nhiên và nấm thơm bổ dưỡng dễ ăn.", ["Protein", "Vitamin B", "Chất xơ", "Kali", "Kẽm", "Selenium"], "fooderai_supgangonam.png"),
        ("Cơm trứng xúc xích", 320, "Cơm trứng xúc xích thơm ngon, dễ ăn với hương vị quen thuộc phù hợp cho trẻ em và nhiều độ tuổi.", ["Protein", "Tinh bột", "Vitamin B", "Canxi", "Kali", "Chất béo"], "fooderai_comtrungxucxich.png"),
        ("Xôi gà xé", 380, "Xôi nếp dẻo thơm ăn kèm gà xé phay mềm, hành phi giòn và nước mắm gừng đặc trưng.", ["Tinh bột", "Protein", "Chất béo", "Vitamin B", "Kali", "Sắt"], "fooderai_xoiga.png"),
        ("Cơm rang dương châu", 420, "Cơm rang dương châu đầy màu sắc với trứng, tôm, xúc xích, rau củ thơm bơ — món ăn nhanh ngon miệng.", ["Tinh bột", "Protein", "Chất béo", "Vitamin A", "Kali", "Sắt"], "fooderai_comrangduongchau.png"),
        ("Sườn xào chua ngọt", 350, "Sườn non xào chua ngọt giòn tan, sốt đỏ bóng đẹp mắt, cân bằng vị chua ngọt mặn hoàn hảo.", ["Protein", "Chất béo", "Vitamin C", "Kali", "Sắt", "Kẽm"], "fooderai_suonxao.png"),
        ("Gà nướng muối ớt", 290, "Gà nướng muối ớt da giòn thơm lừng, thịt mềm ngọt, gia vị sả ớt thấm đều từng thớ thịt.", ["Protein", "Chất béo", "Vitamin B6", "Kali", "Selenium", "Kẽm"], "fooderai_ganuong.png"),
        ("Trứng hấp thịt bằm", 210, "Trứng hấp thịt bằm mềm mịn thơm nhẹ, giàu đạm và dễ ăn, phù hợp cho trẻ em lẫn bữa cơm gia đình.", ["Protein", "Chất béo", "Vitamin B12", "Sắt", "Kẽm", "Canxi"], "fooderai_trunghapthitbam.png"),
        ("Canh bí đỏ", 68, "Canh bí đỏ mềm bùi thanh ngọt tự nhiên, dễ ăn và phù hợp cho bữa cơm gia đình hằng ngày.", ["Beta-carotene", "Vitamin A", "Vitamin C", "Kali", "Chất xơ", "Magie"], "fooderai_canhbido.png"),
        # --- CẬP NHẬT 5 món giữ nguyên ---
        ("Mì tôm lẩu Thái", 360, "Mì tôm lẩu Thái cay nồng, nước dùng chua cay đặc trưng, rau nấm phong phú.", ["Tinh bột", "Protein", "Natri", "Kali", "Vitamin C", "Chất xơ"], "fooderai_mitomlauthai.png"),
        ("Mì spaghetti bò bằm cà chua", 480, "Spaghetti sốt bò bằm cà chua đậm đà, thơm lừng hành tỏi và rau thơm kiểu Ý.",["Tinh bột", "Protein", "Lycopene", "Sắt", "Vitamin C", "Kẽm"], "fooderai_spaghettibolognese.png"),
        ("Mì udon xào bò", 450, "Udon dày dai xào thịt bò mỏng, rau củ và sốt teriyaki đậm vị Nhật Bản.", ["Tinh bột", "Protein", "Sắt", "Kali", "Vitamin B", "Kẽm"], "fooderai_udonxaobo.png"),
        ("Bánh flan trứng sữa", 160, "Bánh flan mềm mịn béo ngậy từ trứng và sữa tươi — tráng miệng nhẹ, giàu canxi và đạm.", ["Protein", "Canxi", "Vitamin D", "Vitamin A", "Chất béo", "Vitamin B12"], "fooderai_banhflan.png"),
        ("Bún gạo xào hải sản", 400, "Bún gạo xào tôm mực tươi rói, rau củ giòn và sốt oyster thơm đậm đà.", ["Tinh bột", "Protein", "Omega-3", "Kali", "Vitamin C", "Sắt"], "fooderai_bungaoxaohaisan.png"),

        # --- CẬP NHẬT 5 món thay mới (thay thế mì ăn liền và carbonara, ramen, kem nấm) ---
        ("Cháo yến mạch trứng gà", 280, "Cháo yến mạch sánh mịn, trứng gà luộc mềm — bữa sáng dinh dưỡng cao, dễ tiêu.", ["Chất xơ", "Protein", "Beta-glucan", "Vitamin B", "Canxi", "Magie"], "fooderai_chaoyenmachtrungga.png"),
        ("Salad ức gà rau củ", 220, "Ức gà hấp xé mềm, rau củ tươi giòn, sốt chanh dầu ô liu — đạm cao, ít calo.", ["Protein", "Chất xơ", "Vitamin C", "Kali", "Sắt", "Vitamin A"], "fooderai_saladga.png"),
        ("Xôi đậu phộng", 320, "Xôi nếp dẻo thơm rắc đậu phộng rang giòn béo — bữa sáng no lâu, giàu tinh bột và đạm thực vật.", ["Tinh bột", "Protein", "Magie", "Kali", "Vitamin B1", "Chất béo lành mạnh"], "fooderai_xoidauphong.png"),
        ("Súp bí đỏ kem tươi", 165, "Súp bí đỏ sánh mịn, béo nhẹ từ kem tươi — vitamin A dồi dào, phù hợp mọi lứa tuổi.", ["Beta-carotene", "Vitamin A", "Canxi", "Kali", "Chất xơ", "Vitamin C"], "fooderai_supbidokemtuoi.png"),
        ("Khoai lang nướng phô mai", 210, "Khoai lang nướng vàng rắc phô mai tan chảy — bữa phụ ngọt tự nhiên, giàu beta-carotene.", ["Beta-carotene", "Canxi", "Chất xơ", "Kali", "Vitamin C", "Protein"], "fooderai_khoailangphomai.png"),
    ],

    # --- Tab 2: Thực Phẩm (ingredient) — 50 món ---
    "ingredient": [
        ("Thịt heo ba chỉ", 260, "Thịt ba chỉ tươi ngon có lớp nạc mỡ đan xen đều đặn, là nguyên liệu giàu đạm cho các món kho, luộc hoặc nướng.", ["Protein", "Chất béo", "Vitamin B12", "Kẽm", "Sắt", "Phốt pho"], "fooderai_thitheobachi.png"),
        ("Thịt bò thăn", 142, "Thịt thăn bò tươi sống rất nạc và mềm, cung cấp nguồn đạm chất lượng cho món xào, áp chảo hoặc bít tết.", ["Protein", "Sắt", "Kẽm", "Kali", "Vitamin B6", "Vitamin B12"], "fooderai_thitbothan.png"),
        ("Ức gà", 120, "Ức gà tươi sống đã lọc da xương, cung cấp đạm dồi dào ít béo cho chế độ ăn kiêng, tập cơ.", ["Protein", "Vitamin B6", "Phốt pho", "Selenium", "Kali", "Kẽm"], "fooderai_ucga.png"),
        ("Cá tra phi lê", 95, "Miếng cá tra phi lê tươi ngon mềm mại, giàu đạm và axit béo omega-3 có lợi cho hệ tim mạch.", ["Protein", "Omega-3", "Vitamin B12", "Natri", "Kali", "Phốt pho"], "fooderai_catraphile.png"),
        ("Tôm sú", 95, "Tôm sú tươi sống thịt săn chắc ngọt đậm, cung cấp lượng đạm cao và canxi bổ dưỡng cho mọi lứa tuổi.", ["Protein", "Canxi", "Vitamin B12", "Sắt", "Kali", "Kẽm"], "fooderai_tomsu.png"),
        ("Trứng gà", 72, "Trứng gà ta tươi sống chứa nguồn đạm hoàn chỉnh lý tưởng, dễ dàng chế biến thành nhiều món bổ dưỡng.", ["Protein", "Chất béo", "Vitamin A", "Vitamin D", "Vitamin B12", "Canxi"], "fooderai_trungga.png"),
        ("Cá hồi", 208, "Lát cá hồi tươi sống nguyên chất với các vân mỡ đan xen đều đặn, nguồn đạm cùng chất béo lành mạnh tuyệt vời.", ["Protein", "Omega-3", "Vitamin B12", "Vitamin D", "Kali", "Selenium"], "fooderai_cahoi.png"),
        ("Mực ống", 92, "Mực ống tươi sống trắng ngần, thớ thịt dày giòn sần sật cùng vị ngọt tự nhiên cô đọng.", ["Protein", "Chất béo", "Đồng", "Selenium", "Vitamin B12", "Phốt pho"], "fooderai_mucong.png"),
        ("Thịt vịt", 211, "Thịt vịt tươi sống có kết cấu săn chắc cùng lớp da béo ngậy đặc trưng.", ["Protein", "Chất béo", "Sắt", "Kẽm", "Selenium", "Vitamin B3"], "fooderai_thitvit.png"),
        ("Cua đồng", 89, "Cua đồng tươi sống nguyên con thịt săn chắc, nguồn canxi dồi dào cho các món canh riêu.", ["Canxi", "Protein", "Chất béo", "Phốt pho", "Sắt", "Vitamin B1"], "fooderai_cuadong.png"),
        ("Gạo tẻ sống", 365, "Gạo trắng là nguồn tinh bột chính của người Việt, cung cấp năng lượng dồi dào.", ["Tinh bột", "Protein", "Vitamin B1", "Kẽm", "Magie"], "fooderai_gaote.png"),
        ("Khoai lang", 86, "Khoai lang vàng giàu beta-carotene, chất xơ và vitamin C, thấp calo.", ["Beta-carotene", "Chất xơ", "Vitamin C", "Kali", "Mangan"], "fooderai_khoailang.png"),
        ("Khoai tây", 77, "Khoai tây nguồn kali và vitamin B6 tốt, tinh bột dễ tiêu.", ["Tinh bột", "Kali", "Vitamin B6", "Vitamin C", "Chất xơ"], "fooderai_khoaitay.png"),
        ("Bắp ngô", 96, "Bắp ngô cung cấp tinh bột, chất xơ, và các vitamin nhóm B.", ["Tinh bột", "Chất xơ", "Vitamin B", "Magie", "Kali"], "fooderai_bapngo.png"),
        ("Yến mạch", 389, "Yến mạch giàu beta-glucan — chất xơ hòa tan giúp kiểm soát đường huyết và cholesterol hiệu quả.", ["Chất xơ", "Protein", "Magie", "Phốt pho", "Vitamin B1", "Kẽm"], "fooderai_yenmach.png"),
        ("Đậu xanh", 347, "Đậu xanh giàu protein thực vật, chất xơ và folate, tốt cho tim mạch và hệ tiêu hóa.", ["Protein", "Chất xơ", "Folate", "Kali", "Magie", "Sắt"], "fooderai_dauxanh.png"),
        ("Hạnh nhân", 579, "Hạnh nhân giàu vitamin E, magie và chất béo lành mạnh, tốt cho tim mạch và não bộ.", ["Vitamin E", "Magie", "Chất béo lành mạnh", "Protein", "Canxi", "Chất xơ"], "fooderai_hanhnhan.png"),
        ("Rau muống", 19, "Rau muống là loại rau quen thuộc nhất Việt Nam, giàu sắt và canxi.", ["Sắt", "Canxi", "Vitamin C", "Beta-carotene", "Chất xơ"], "fooderai_raumuong.png"),
        ("Bắp cải", 25, "Rau bắp cải giàu chất xơ, vitamin C, kali và folate. Tốt cho hệ tiêu hóa.", ["Vitamin C", "Chất xơ", "Kali", "Folate", "Khoáng chất"], "fooderai_bapcai.png"),
        ("Cà chua", 18, "Cà chua giàu lycopene — chất chống oxy hóa mạnh, tốt cho tim mạch và phòng ung thư.", ["Lycopene", "Vitamin C", "Kali", "Vitamin A", "Chất xơ"], "fooderai_cachua.png"),
        ("Cà rốt", 41, "Cà rốt nguồn beta-carotene dồi dào, tốt cho mắt và hệ miễn dịch.", ["Beta-carotene", "Vitamin A", "Chất xơ", "Kali", "Vitamin K"], "fooderai_carot.png"),
        ("Hành tây", 40, "Hành tây chứa quercetin — flavonoid mạnh chống viêm, tốt cho tim mạch và hệ miễn dịch.", ["Quercetin", "Vitamin C", "Chất xơ", "Kali", "Folate"], "fooderai_hanhtay.png"),
        ("Tỏi", 149, "Tỏi chứa allicin có tác dụng kháng khuẩn, kháng virus, hỗ trợ tim mạch và tăng đề kháng.", ["Allicin", "Vitamin C", "Vitamin B6", "Mangan", "Selenium"], "fooderai_garlic.png"),
        ("Gừng", 80, "Gừng chứa gingerol có tác dụng chống viêm, giảm buồn nôn và hỗ trợ tiêu hóa.", ["Gingerol", "Magie", "Vitamin B6", "Kali", "Vitamin C"], "fooderai_gung.png"),
        ("Sả", 99, "Sả chứa citral có tính kháng khuẩn, kháng nấm, hỗ trợ tiêu hóa và giải độc cơ thể.", ["Citral", "Vitamin A", "Kali", "Magie", "Vitamin C"], "fooderai_sa.png"),
        ("Ớt chuông", 31, "Ớt chuông đỏ chứa vitamin C gấp 3 lần cam, giàu beta-carotene và chất chống oxy hóa.", ["Vitamin C", "Beta-carotene", "Vitamin B6", "Kali", "Chất xơ"], "fooderai_otchuong.png"),
        ("Ớt sừng", 40, "Ớt sừng chứa capsaicin kích thích trao đổi chất, đốt cháy calo và có tính kháng viêm.", ["Capsaicin", "Vitamin C", "Vitamin A", "Kali", "Chất xơ"], "fooderai_otsung.png"),
        ("Nấm rơm", 22, "Nấm rơm giàu protein thực vật, beta-glucan tăng cường miễn dịch và chất chống oxy hóa.", ["Protein", "Beta-glucan", "Vitamin B", "Kali", "Sắt"], "fooderai_namrom.png"),
        ("Khổ qua", 17, "Khổ qua giàu vitamin C, chứa charantin giúp kiểm soát đường huyết, tốt cho người tiểu đường.", ["Vitamin C", "Charantin", "Chất xơ", "Kali", "Folate"], "fooderai_khoqua.png"),
        ("Bí đỏ", 26, "Bí đỏ chứa beta-carotene dồi dào, vitamin C và kali, thấp calo và tốt cho mắt.", ["Beta-carotene", "Vitamin C", "Kali", "Chất xơ", "Vitamin A"], "fooderai_bido.png"),
        ("Đậu bắp", 33, "Đậu bắp giàu chất nhầy có lợi cho tiêu hóa, chứa folate và vitamin K quan trọng.", ["Chất xơ", "Folate", "Vitamin K", "Vitamin C", "Magie"], "fooderai_daubap.png"),
        ("Quả mít", 95, "Quả mít nhiệt đới thơm ngọt giàu vitamin C và chất xơ, vừa là trái cây vừa là nguyên liệu nấu chay thay thịt cực phổ biến với giới GenZ.", ["Vitamin C", "Chất xơ", "Kali", "Vitamin B6", "Magie", "Đồng"], "fooderai_mit.png"),
        ("Cải thìa", 13, "Cải thìa giàu vitamin C, K và calcium, ít calo, tốt cho xương và hệ miễn dịch.", ["Vitamin C", "Vitamin K", "Canxi", "Chất xơ", "Beta-carotene"], "fooderai_caithia.png"),
        ("Giá đỗ", 30, "Giá đỗ mọc từ đậu xanh nảy mầm, giàu vitamin C, enzyme tiêu hóa và chất chống oxy hóa.", ["Vitamin C", "Protein", "Chất xơ", "Folate", "Vitamin K"], "fooderai_giado.png"),
        ("Bông cải xanh", 34, "Siêu thực phẩm giàu vitamin C, K, chất xơ và sulforaphane chống ung thư.", ["Vitamin C", "Vitamin K", "Chất xơ", "Folate", "Sắt"], "fooderai_bongcaixanh.png"),
        ("Cải bó xôi Spinach", 23, "Rau bina giàu sắt, vitamin K, folate và lutein bảo vệ mắt.", ["Sắt", "Vitamin K", "Folate", "Lutein", "Magie"], "fooderai_spinach.png"),
        ("Bơ Avocado", 160, "Bơ avocado giàu chất béo lành mạnh omega-9, kali và vitamin E tốt cho tim mạch.", ["Chất béo lành mạnh", "Kali", "Vitamin E", "Chất xơ", "Vitamin K"], "fooderai_avocado.png"),
        ("Atisô", 47, "Atisô chứa cynarin hỗ trợ gan mật, giàu chất xơ prebiotics tốt cho vi khuẩn đường ruột.", ["Chất xơ", "Cynarin", "Folate", "Vitamin C", "Magie"], "fooderai_atiso.png"),
        ("Cần tây", 16, "Cần tây giàu apigenin chống viêm, tốt cho huyết áp, thanh nhiệt và lợi tiểu.", ["Apigenin", "Vitamin K", "Kali", "Vitamin C", "Folate"], "fooderai_cantay.png"),
        ("Dưa leo", 16, "Dưa leo 95% là nước, giàu vitamin K và kali, giúp hydrat hóa cơ thể và mát gan.", ["Nước", "Vitamin K", "Kali", "Vitamin C", "Magie"], "fooderai_dualeo.png"),
        ("Chuối tiêu", 89, "Chuối tiêu giàu kali, vitamin B6 và serotonin tự nhiên giúp cải thiện tâm trạng.", ["Kali", "Vitamin B6", "Vitamin C", "Magie", "Chất xơ"], "fooderai_chuoi.png"),
        ("Xoài chín", 60, "Xoài chín ngọt thơm giàu beta-carotene, vitamin C và enzyme amylase hỗ trợ tiêu hóa.", ["Beta-carotene", "Vitamin C", "Chất xơ", "Kali", "Folate"], "fooderai_xoai.png"),
        ("Thanh long đỏ", 50, "Thanh long ruột đỏ giàu lycopene chống oxy hóa, vitamin C và probiotics tự nhiên.", ["Lycopene", "Vitamin C", "Chất xơ", "Magie", "Sắt"], "fooderai_thanhlong.png"),
        ("Dừa tươi", 354, "Dừa tươi chứa MCT — chất béo chuỗi trung bình dễ chuyển hóa thành năng lượng tức thì.", ["MCT", "Kali", "Magie", "Phốt pho", "Chất xơ"], "fooderai_duatuoi.png"),
        ("Dâu tây", 32, "Dâu tây giàu vitamin C, anthocyanin và ellagic acid chống ung thư, tốt cho da.", ["Vitamin C", "Anthocyanin", "Chất xơ", "Folate", "Kali"], "fooderai_dautay.png"),
        ("Táo xanh", 52, "Táo xanh giàu pectin — chất xơ hòa tan tốt cho ruột, quercetin và vitamin C.", ["Chất xơ", "Quercetin", "Vitamin C", "Kali", "Vitamin K"], "fooderai_taoxanh.png"),
        ("Việt quất", 57, "Việt quất giàu anthocyanin nhất trong các loại quả, bảo vệ não và cải thiện trí nhớ.", ["Anthocyanin", "Vitamin C", "Vitamin K", "Mangan", "Chất xơ"], "fooderai_vietquat.png"),
        ("Chanh vàng", 29, "Chanh vàng giàu vitamin C, limonene và flavonoid chống viêm, hỗ trợ miễn dịch và tiêu hóa.", ["Vitamin C", "Limonene", "Axit citric", "Kali", "Folate"], "fooderai_chanhvang.png"),
        ("Cải ngọt", 20, "Cải ngọt chứa nhiều vitamin A, C và chất xơ, phù hợp cho món luộc, xào hoặc nấu canh nhẹ.", ["Vitamin A", "Vitamin C", "Chất xơ", "Canxi", "Kali"], "fooderai_caingot.png"),
        ("Rau cải xanh", 27, "Rau cải xanh có vị thanh nhẹ, giàu vitamin K và chất chống oxy hóa tốt cho sức khỏe.", ["Vitamin K", "Vitamin C", "Chất xơ", "Folate", "Canxi"], "fooderai_caixanh.png"),
        ("Su su", 19, "Su su ít calo, giàu nước và chất xơ, phù hợp cho món luộc hoặc xào thanh đạm.", ["Chất xơ", "Vitamin C", "Kali", "Folate", "Magie"], "fooderai_susu.png"),
        ("Đậu hũ", 76, "Đậu hũ mềm giàu đạm thực vật và canxi, phù hợp cho nhiều món chay và món gia đình.", ["Protein", "Canxi", "Sắt", "Magie", "Isoflavone"], "fooderai_dauhu.png"),
        ("Cam", 47, "Cam tươi chứa lượng vitamin C dồi dào, hỗ trợ miễn dịch và bổ sung nước tự nhiên cho cơ thể.", ["Vitamin C", "Chất xơ", "Kali", "Folate", "Flavonoid"], "fooderai_cam.png"),
        ("Sữa chua", 59, "Sữa chua cung cấp lợi khuẩn probiotics cùng canxi và protein, hỗ trợ tiêu hóa và sức khỏe đường ruột.", ["Probiotics", "Canxi", "Protein", "Vitamin B12", "Kali"], "fooderai_suachua.png"),
        ("Đậu que", 31, "Đậu que xanh giòn giàu chất xơ và vitamin K, phù hợp cho món luộc, xào hoặc hấp nhẹ.", ["Chất xơ", "Vitamin K", "Vitamin C", "Folate", "Kali"], "fooderai_dauque.png"),
        ("Dưa hấu", 30, "Dưa hấu mọng nước giúp giải nhiệt cơ thể, bổ sung vitamin C và nước tự nhiên ngày nóng.", ["Vitamin C", "Nước", "Lycopene", "Kali", "Vitamin A"], "fooderai_duahau.png"),
        ("Hành lá", 32, "Hành lá tươi giàu vitamin K và C, thường dùng làm gia vị trang trí và tăng hương vị cho các món ăn Việt.", ["Vitamin K", "Vitamin C", "Chất xơ", "Kali", "Folate"], "fooderai_hanhla.png"),
        ("Nước mắm", 35, "Nước mắm truyền thống Việt Nam giàu đạm thủy phân và khoáng chất, gia vị không thể thiếu trong ẩm thực Việt.", ["Protein", "Natri", "Kali", "Magie", "Vitamin B12"], "fooderai_nuocmam.png"),
        ("Bánh phở tươi", 109, "Bánh phở tươi làm từ gạo, cung cấp tinh bột năng lượng nhanh, nguyên liệu chính của món phở truyền thống.", ["Tinh bột", "Protein", "Canxi", "Phốt pho", "Natri"], "fooderai_banhpho.png"),
        ("Phô mai", 402, "Phô mai béo ngậy giàu canxi và protein, nguyên liệu phổ biến trong pizza, burger, bánh mì nướng và các món ăn hiện đại.", ["Canxi", "Protein", "Chất béo", "Vitamin B12", "Vitamin A", "Phốt pho"], "fooderai_phomai.png"),
        ("Matcha bột", 324, "Bột trà xanh Nhật nguyên chất giàu L-theanine và catechin, nguyên liệu pha trà sữa, làm bánh và smoothie được giới GenZ ưa chuộng.", ["L-theanine", "Catechin", "Vitamin K", "Caffeine", "Chất chống oxy hóa", "Magie"], "fooderai_matchabot.png"),
    ],

    # --- Tab 3: Thức Uống (drink) — 60 món ---
    "drink": [
        ("Cà phê đen", 2, "Cà phê đen không đường — thức uống giảm calo lý tưởng, kích thích thần kinh và tăng trao đổi chất.", ["Caffeine", "Chất chống oxy hóa", "Magie", "Kali", "Niacin"], "fooderai_caphedenkhongduong.png"),
        ("Cà phê sữa đá", 80, "Cà phê phin truyền thống Việt pha với sữa đặc, đổ lên đá viên — thức uống quốc dân Việt Nam.", ["Caffeine", "Canxi", "Đường", "Chất béo", "Năng lượng"], "fooderai_caphesuada.png"),
        ("Espresso", 5, "Tách Espresso nguyên chất đậm đặc với lớp crema vàng óng, caffeine mạnh mẽ giúp tỉnh táo.", ["Caffeine", "Kali", "Magie", "Phốt pho", "Chất chống oxy hóa"], "fooderai_espresso.png"),
        ("Americano", 15, "Ly Americano thanh nhẹ kết hợp espresso và nước nóng, caffeine hỗ trợ trao đổi chất.", ["Caffeine", "Kali", "Magie", "Phốt pho", "Natri", "Chất chống oxy hóa"], "fooderai_americano.png"),
        ("Cappuccino", 110, "Tách Cappuccino chuẩn Ý hòa quyện espresso đậm đà, sữa tươi nóng và lớp bọt mịn màng.", ["Canxi", "Protein", "Carbohydrate", "Chất béo", "Caffeine", "Chất chống oxy hóa"], "fooderai_cappuccino.png"),
        ("Latte", 120, "Ly Latte mượt mà với espresso và lớp bọt sữa mịn màng tạo hình nghệ thuật.", ["Caffeine", "Canxi", "Carbohydrate", "Chất béo", "Protein", "Vitamin D"], "fooderai_latte.png"),
        ("Cold brew", 5, "Cold brew ngâm lạnh 12-24 giờ cho vị cà phê mượt mà ít đắng, caffeine cao nhưng ít axit hơn.", ["Caffeine", "Chất chống oxy hóa", "Magie", "Kali", "Crom"], "fooderai_coldbrew.png"),
        ("Cà phê trứng Hà Nội", 180, "Cà phê trứng Hà Nội độc đáo với lớp kem trứng đánh bông béo ngậy phủ lên cà phê đen đậm đà.", ["Caffeine", "Protein", "Chất béo", "Canxi", "Vitamin D"], "fooderai_caphetrunghn.png"),
        ("Bạc xỉu", 120, "Bạc xỉu — cà phê ít đắng nhiều sữa, thức uống đặc trưng của người Sài Gòn.", ["Caffeine", "Canxi", "Đường", "Chất béo", "Protein"], "fooderai_bacxiu.png"),
        ("Cà phê dừa", 150, "Cà phê kết hợp nước cốt dừa béo ngậy — đặc sản nổi tiếng Hội An và Đà Nẵng.", ["Caffeine", "Chất béo", "Canxi", "Magie", "Kali"], "fooderai_caphedua.png"),
        ("Mocha", 160, "Mocha hòa quyện giữa espresso, sữa và sốt chocolate — thức uống ngọt ngào đầy hương vị.", ["Caffeine", "Canxi", "Carbohydrate", "Chất béo", "Magie", "Sắt"], "fooderai_mocha.png"),
        ("Macchiato", 35, "Macchiato — espresso đậm đà với một chút sữa tạo điểm nhấn, cân bằng giữa đắng và béo.", ["Caffeine", "Canxi", "Chất béo", "Magie", "Kali"], "fooderai_macchiato.png"),
        ("Trà đá không đường", 0, "Trà đá không đường không calo, giàu polyphenol chống oxy hóa, thanh mát và giải nhiệt.", ["Polyphenol", "Catechin", "Fluoride", "Kali", "Magie"], "fooderai_tradakhongduong.png"),
        ("Trà sữa trân châu", 350, "Trà sữa trân châu với viên trân châu dai ngon, trà thơm và sữa béo ngậy.", ["Carbohydrate", "Canxi", "Protein", "Caffeine", "Đường"], "fooderai_trasuatranchau.png"),
        ("Trà xanh Matcha latte", 180, "Matcha latte với bột trà xanh Nhật nguyên chất giàu L-theanine, kết hợp sữa béo ngậy.", ["Caffeine", "L-theanine", "Catechin", "Canxi", "Vitamin K", "Chất chống oxy hóa"], "fooderai_matchalatte.png"),
        ("Hồng trà sữa", 220, "Hồng trà sữa đỏ đẹp mắt với vị trà Assam đậm đà kết hợp sữa tươi béo ngậy.", ["Caffeine", "Canxi", "Carbohydrate", "Chất béo", "Theanine", "Protein"], "fooderai_hongtrasua.png"),
        ("Trà atisô đá", 25, "Trà atisô mát lạnh hỗ trợ gan mật, giải độc và thanh nhiệt hiệu quả.", ["Cynarin", "Chất chống oxy hóa", "Canxi", "Kali", "Vitamin C"], "fooderai_traatiso.png"),
        ("Trà bí đao", 15, "Trà bí đao thanh mát lợi tiểu, hỗ trợ giảm cân và thanh nhiệt mùa hè.", ["Chất xơ", "Vitamin C", "Kali", "Magie", "Nước"], "fooderai_trabidao.png"),
        ("Trà hoa cúc", 5, "Trà hoa cúc thơm nhẹ với apigenin giúp thư giãn, cải thiện giấc ngủ và giảm lo âu.", ["Apigenin", "Chất chống oxy hóa", "Canxi", "Magie", "Kali"], "fooderai_trahoacuc.png"),
        ("Trà gừng mật ong", 60, "Trà gừng mật ong ấm nóng với gingerol kháng viêm và mật ong kháng khuẩn tự nhiên.", ["Gingerol", "Enzyme mật ong", "Vitamin C", "Magie", "Kali"], "fooderai_tragung.png"),
        ("Trà ô long đá", 20, "Trà ô long bán lên men với polyphenol phong phú, hỗ trợ giảm cân và kiểm soát đường huyết.", ["Polyphenol", "Caffeine", "Theanine", "Fluoride", "Kali"], "fooderai_traolongda.png"),
        ("Trà đào cam sả", 120, "Trà đào cam sả sảng khoái với vị chua ngọt từ đào, cam tươi và hương sả thơm mát.", ["Vitamin C", "Kali", "Chất chống oxy hóa", "Citral", "Đường tự nhiên"], "fooderai_tradaocamsa.png"),
        ("Boba matcha", 280, "Boba matcha với trân châu đen dai ngon, matcha Nhật xanh thơm và sữa tươi béo ngậy.", ["Caffeine", "L-theanine", "Canxi", "Carbohydrate", "Protein", "Vitamin K"], "fooderai_bobamatcha.png"),
        ("Nước ép cam tươi", 45, "Nước ép cam tươi nguyên chất giàu vitamin C, folate và chất chống oxy hóa.", ["Vitamin C", "Folate", "Kali", "Hesperidin", "Đường tự nhiên"], "fooderai_nuoepcam.png"),
        ("Nước ép dưa hấu", 30, "Nước ép dưa hấu mát lạnh, giải nhiệt với lycopene và vitamin C.", ["Lycopene", "Vitamin C", "Kali", "Nước", "Đường tự nhiên"], "fooderai_nuocepduahau.png"),
        ("Sinh tố bơ sữa", 280, "Sinh tố bơ sữa béo ngậy giàu chất béo lành mạnh, vitamin E và kali.", ["Chất béo lành mạnh", "Kali", "Vitamin E", "Canxi", "Magie"], "fooderai_sinhtocbosua.png"),
        ("Sinh tố xoài", 160, "Sinh tố xoài ngọt thơm giàu beta-carotene, vitamin C và enzyme tiêu hóa amylase.", ["Beta-carotene", "Vitamin C", "Enzyme amylase", "Kali", "Chất xơ"], "fooderai_sinhtocxoai.png"),
        ("Sinh tố dâu tây", 140, "Sinh tố dâu tây đỏ tươi giàu anthocyanin, vitamin C và ellagic acid.", ["Anthocyanin", "Vitamin C", "Folate", "Kali", "Canxi"], "fooderai_sinhtodautay.png"),
        ("Nước ép dứa", 50, "Nước ép dứa chứa bromelain enzyme tiêu hóa đặc biệt, giàu vitamin C và mangan.", ["Bromelain", "Vitamin C", "Mangan", "Kali", "Đồng"], "fooderai_nuocepdua.png"),
        ("Nước ép lựu", 84, "Nước ép lựu đỏ đậm giàu punicalagins và anthocyanin — chất chống oxy hóa mạnh nhất.", ["Punicalagins", "Anthocyanin", "Vitamin C", "Kali", "Folate"], "fooderai_nuocepluu.png"),
        ("Sinh tố việt quất", 120, "Sinh tố việt quất giàu anthocyanin bảo vệ não, cải thiện trí nhớ và thị lực.", ["Anthocyanin", "Vitamin C", "Vitamin K", "Mangan", "Chất xơ"], "fooderai_sinhtocvietquat.png"),
        ("Nước ép táo xanh", 48, "Nước ép táo xanh thanh mát giàu pectin, quercetin và vitamin C.", ["Chất xơ", "Quercetin", "Vitamin C", "Kali", "Vitamin K"], "fooderai_nuoceptaoxanh.png"),
        ("Sinh tố chuối sữa", 180, "Sinh tố chuối sữa béo ngậy giàu kali và năng lượng, lý tưởng sau tập luyện.", ["Kali", "Canxi", "Protein", "Vitamin B6", "Magie"], "fooderai_sinhtochuoisua.png"),
        ("Nước ép dưa leo", 16, "Nước ép dưa leo mát lạnh hydrat hóa cơ thể, giàu vitamin K và lợi tiểu.", ["Nước", "Vitamin K", "Kali", "Vitamin C", "Magie"], "fooderai_nuocepdualeo.png"),
        ("Sinh tố thanh long", 130, "Sinh tố thanh long đỏ giàu lycopene, betacyanin và vitamin C.", ["Lycopene", "Betacyanin", "Vitamin C", "Magie", "Sắt"], "fooderai_sinhtothanhlong.png"),
        ("Nước ép gừng chanh", 30, "Nước ép gừng chanh shot nóng kích thích miễn dịch, giảm viêm và detox cơ thể.", ["Gingerol", "Vitamin C", "Axit citric", "Magie", "Kali"], "fooderai_nuocepgungchanh.png"),
        ("Smoothie rau củ", 85, "Smoothie rau củ xanh tổng hợp giàu chất xơ, enzyme và phytonutrients.", ["Chất xơ", "Vitamin K", "Sắt", "Folate", "Chất chống oxy hóa"], "fooderai_smoothieraucu.png"),
        ("Sinh tố sữa chua dâu", 160, "Sinh tố sữa chua dâu giàu probiotics, vitamin C và canxi tốt cho đường ruột.", ["Probiotics", "Canxi", "Vitamin C", "Protein", "Anthocyanin"], "fooderai_sinhtosuachuadau.png"),
        ("Nước detox chanh dưa leo", 10, "Nước detox chanh dưa leo thanh mát, lợi tiểu và hỗ trợ giải độc cơ thể.", ["Vitamin C", "Nước", "Kali", "Magie", "Chất chống oxy hóa"], "fooderai_detoxchanhdualeo.png"),
        ("Nước mía", 73, "Nước mía tươi ngọt mát giàu đường tự nhiên sucrose, vitamin B và khoáng chất.", ["Sucrose", "Vitamin B", "Sắt", "Canxi", "Kali"], "fooderai_nuocmia.png"),
        ("Sữa đậu nành", 54, "Sữa đậu nành thơm béo giàu đạm thực vật và canxi, phù hợp cho bữa sáng hoặc ăn nhẹ.", ["Protein", "Canxi", "Isoflavone", "Vitamin B", "Kali"], "fooderai_suadaunanh.png"),
        ("Nước dừa tươi", 19, "Nước dừa tươi điện giải tự nhiên giàu kali, mangan và cytokinin chống lão hóa.", ["Điện giải", "Kali", "Mangan", "Cytokinin", "Vitamin C"], "fooderai_nuocduatuoi.png"),
        ("Rau má đá", 15, "Rau má đá thanh nhiệt giải độc, chứa asiaticoside tốt cho não và chữa lành vết thương.", ["Asiaticoside", "Vitamin C", "Chất chống oxy hóa", "Kali", "Sắt"], "fooderai_raumada.png"),
        ("Nước chanh muối", 12, "Nước chanh muối cân bằng điện giải, kích thích tiêu hóa và thanh nhiệt.", ["Vitamin C", "Natri", "Kali", "Axit citric", "Magie"], "fooderai_nuocchanhmuoi.png"),
        ("Lemonade bạc hà", 60, "Lemonade bạc hà sảng khoái với vị chua chanh, ngọt nhẹ và menthol bạc hà mát lạnh.", ["Vitamin C", "Menthol", "Kali", "Chất chống oxy hóa", "Đường tự nhiên"], "fooderai_lemonadebacha.png"),
        ("Mojito không cồn", 70, "Mojito không cồn sảng khoái với nước cốt chanh, bạc hà tươi, đường và soda.", ["Vitamin C", "Menthol", "Chất chống oxy hóa", "Kali", "Magie"], "fooderai_mojito.png"),
        ("Soda vải", 120, "Soda vải ngọt thơm từ vải thiều tươi với hương vị đặc trưng ngọt thanh.", ["Vitamin C", "Vitamin B6", "Kali", "Đồng", "Đường tự nhiên"], "fooderai_sodavai.png"),
        ("Sữa hạnh nhân", 40, "Sữa hạnh nhân không lactose giàu vitamin E, canxi tăng cường và axit béo omega-3.", ["Vitamin E", "Canxi", "Vitamin D", "Omega-3", "Magie"], "fooderai_suahanhnhan.png"),
        ("Sữa yến mạch", 60, "Sữa yến mạch bền vững giàu beta-glucan tốt cho tim mạch và kiểm soát đường huyết.", ["Beta-glucan", "Canxi", "Vitamin D", "Chất xơ", "Vitamin B"], "fooderai_suayenmach.png"),
        ("Hồng trà đào", 150, "Hồng trà đào thơm ngát với hồng trà Assam đậm đà, đào tươi ngọt chua và đường đỏ.", ["Caffeine", "Vitamin C", "Theanine", "Kali", "Chất chống oxy hóa"], "fooderai_hongtradao.png"),
        ("Nước gừng mật ong ấm", 65, "Nước gừng mật ong ấm uống buổi sáng kích hoạt hệ miễn dịch, giảm viêm và sưởi ấm cơ thể.", ["Gingerol", "Enzyme mật ong", "Vitamin C", "Kali", "Magie"], "fooderai_nuocgungmatong.png"),
    ],
}


# =====================================================================
# TRANG CHÍNH: PAGE FOOD ALMANAC
# =====================================================================
class PageFoodAlmanac(QFrame):
     def __init__(self, parent=None):
          super().__init__(parent)
          self.setFixedSize(1240, 640)
          self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
          self.current_tab = 0   # Tab đang chọn

          self.setStyleSheet("""
            PageFoodAlmanac { background-color: white; border: 3px solid rgba(0, 77, 77, 0.5); border-radius: 24px; }
          """)

          box_shadow = QGraphicsDropShadowEffect()
          box_shadow.setBlurRadius(5)
          box_shadow.setOffset(0, 3)
          box_shadow.setColor(QColor(150, 150, 150, 180))
          self.setGraphicsEffect(box_shadow)

          main_layout = QVBoxLayout(self)
          main_layout.setContentsMargins(15, 10, 15, 15)
          main_layout.setSpacing(8)

          # ===========================================================
          # PHẦN 1: BANNER TIÊU ĐỀ (giữ nguyên từ phiên trước)
          # ===========================================================
          self.banner = QFrame()
          self.banner.setFixedSize(1210, 60)

          color_hex = "#5C94FA"
          base_color = QColor(color_hex)
          color_80, color_100 = base_color.darker(109).name(), base_color.darker(131).name()

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

          banner_shadow = QGraphicsDropShadowEffect()
          banner_shadow.setBlurRadius(6)
          banner_shadow.setOffset(0, 0)
          banner_shadow.setColor(QColor(0, 0, 0, 204))
          self.banner.setGraphicsEffect(banner_shadow)

          banner_layout = QHBoxLayout(self.banner)
          banner_layout.setContentsMargins(3, 0, 12, 0)
          banner_layout.setSpacing(0)

          title_group = QWidget()
          title_group.setStyleSheet("background: transparent;")
          title_layout = QHBoxLayout(title_group)
          title_layout.setContentsMargins(7, 0, 3, 0)
          title_layout.setSpacing(5)

          title_icon = QLabel()
          tab_icon_path = os.path.join("assets", "fooderai-almanacfood-ui", "almanac_titleicon.png")
          if os.path.exists(tab_icon_path):
               title_icon.setPixmap(QPixmap(tab_icon_path).scaledToHeight(45, Qt.TransformationMode.SmoothTransformation))

          title_text = QLabel("Sổ tay món ăn")
          title_text.setStyleSheet("""
               color: white; border: none;
               font-family: 'Roboto'; font-size: 25px; font-weight: 800;
          """)

          title_layout.addWidget(title_icon)
          title_layout.addWidget(title_text)

          self.search_bar = CustomSearchBar()

          banner_layout.addWidget(title_group, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
          banner_layout.addStretch()
          banner_layout.addWidget(self.search_bar, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

          main_layout.addWidget(self.banner, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

          # ===========================================================
          # PHẦN 2: BODY — Sidebar trái + Grid phải + Scrollbar tùy chỉnh
          # ===========================================================
          body_layout = QHBoxLayout()
          body_layout.setSpacing(10)
          body_layout.setContentsMargins(-5, 0, 0, 0)

          # --- SIDEBAR 4 TAB (giữ nguyên từ phiên trước) ---
          self.food_list_panel = QFrame()
          self.food_list_panel.setFixedSize(225, 540)
          self.food_list_panel.setStyleSheet("""
               QFrame {
                    background-color: #F2F2F2;
                    border: 2px solid #004d4d;
                    border-radius: 12px;
               }
          """)

          sidebar_layout = QVBoxLayout(self.food_list_panel)
          sidebar_layout.setSpacing(10)
          sidebar_layout.setContentsMargins(5, 10, 5, 10)

          categories = [
               ("almanac-allfood-mode.png", "Tất cả món ăn"),
               ("almanac-food-mode.png", "Món Ăn"),
               ("almanac-ingredient-mode.png", "Thực phẩm"),
               ("almanac-drink-mode.png", "Thức uống"),
          ]

          self.tab_frames = []
          for icon_file, label_text in categories:
               tab_frame = QFrame()
               tab_frame.setStyleSheet("QFrame { background: transparent; border: none; }")
               tab_frame.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

               tab_layout = QVBoxLayout(tab_frame)
               tab_layout.setContentsMargins(0, -4, 0, -4)
               tab_layout.setSpacing(0)
               tab_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

               lbl_icon = QLabel()
               lbl_icon.setStyleSheet("border: none; background: transparent;")
               lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

               loop_icon_path = os.path.join("assets", "fooderai-almanacfood-ui", icon_file)
               if os.path.exists(loop_icon_path):
                    lbl_icon.setPixmap(QPixmap(loop_icon_path).scaledToHeight(70, Qt.TransformationMode.SmoothTransformation))

               lbl_text = QLabel(label_text)
               lbl_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
               lbl_text.setStyleSheet("border: none; background: transparent; color: #1a1a1a;")

               tab_font = QFont("Roboto")
               tab_font.setPixelSize(20)
               tab_font.setWeight(QFont.Weight.Medium)
               tab_font.setStretch(QFont.Stretch.SemiCondensed)
               lbl_text.setFont(tab_font)

               tab_layout.addWidget(lbl_icon)
               tab_layout.addWidget(lbl_text)

               self.tab_frames.append((tab_frame, lbl_text))
               idx = len(self.tab_frames) - 1
               tab_frame.mousePressEvent = lambda e, i=idx: self.select_tab(i)

               sidebar_layout.addWidget(tab_frame, stretch=1)

          from PySide6.QtCore import QTimer
          QTimer.singleShot(0, lambda: self.select_tab(0))

          # --- KHU VỰC PHẢI: LƯỚI + SCROLLBAR ---
          right_container = QWidget()
          right_container.setStyleSheet("background: transparent;")
          right_h_layout = QHBoxLayout(right_container)
          right_h_layout.setContentsMargins(0, 0, 0, 0)
          right_h_layout.setSpacing(4)

          # [A] SCROLL AREA chứa lưới FoodCard
          self.scroll_area = QScrollArea()
          self.scroll_area.setWidgetResizable(True)
          # Ẩn scrollbar mặc định (ta dùng scrollbar tùy chỉnh)
          self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
          self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
          self.scroll_area.setStyleSheet("""
               QScrollArea {
                    background-color: #FFFFFF;
                    border: 2px solid #004d4d;
                    border-radius: 12px;
               }
               QScrollArea > QWidget > QWidget { background: transparent; }
          """)

          # Widget nội dung bên trong ScrollArea
          self.grid_widget = QWidget()
          self.grid_widget.setStyleSheet("background: transparent;")
          self.grid_layout = QGridLayout(self.grid_widget)
          self.grid_layout.setContentsMargins(12, 12, 12, 12)

          # 2 cột, khoảng cách 10px
          self.grid_layout.setHorizontalSpacing(10)
          self.grid_layout.setVerticalSpacing(10)

          self.scroll_area.setWidget(self.grid_widget)

          # [B] SCROLLBAR TÙY CHỈNH (Bevel + Quả cầu)
          self.custom_scrollbar = BevelScrollBar(self.scroll_area)

          # Kết nối: khi ScrollArea cuộn thì vẽ lại scrollbar
          self.scroll_area.verticalScrollBar().valueChanged.connect(
               lambda: self.custom_scrollbar.update()
          )

          right_h_layout.addWidget(self.scroll_area, 1)
          right_h_layout.addWidget(self.custom_scrollbar)

          body_layout.addWidget(self.food_list_panel)
          body_layout.addWidget(right_container, 1)

          main_layout.addLayout(body_layout)

          # Nạp dữ liệu tab đầu tiên
          self._load_tab_data("all")

     # ===========================================================
     # HÀM NẠP DỮ LIỆU VÀO LƯỚI
     # ===========================================================
     def _load_tab_data(self, key):
          """
          [GIẢI THÍCH]
          Xóa toàn bộ widget cũ trong grid, sau đó tạo lại FoodCard
          từ danh sách dữ liệu tương ứng với key tab đang chọn.
          Xếp 2 thẻ mỗi hàng: cột 0 và cột 1.
          """
          # Xóa tất cả widget cũ ra khỏi lưới
          while self.grid_layout.count():
               item = self.grid_layout.takeAt(0)
               if item.widget():
                    item.widget().deleteLater()

          items = FOOD_DATA.get(key, [])

          BASE_IMG_DIR = os.path.join("assets", "fooder-almanac-content")

          for i, (name, kcal, desc, nutrients, img_file) in enumerate(items):
               pix = None
               # =========================================
               # TỰ ĐỘNG XÁC ĐỊNH THƯ MỤC ẢNH
               # =========================================

               possible_paths = []

               # Tab cụ thể
               if key == "food":
                    possible_paths.append(
                         os.path.join(BASE_IMG_DIR, "food", img_file)
                    )
               elif key == "drink":
                    possible_paths.append(
                         os.path.join(BASE_IMG_DIR, "drink", img_file)
                    )

               elif key == "ingredient":
                    possible_paths.append(
                         os.path.join(BASE_IMG_DIR, "ingredient", img_file)
                    )
               # Tab ALL → dò toàn bộ folder
               else:
                    possible_paths.extend([
                         os.path.join(BASE_IMG_DIR, "food", img_file),
                         os.path.join(BASE_IMG_DIR, "drink", img_file),
                         os.path.join(BASE_IMG_DIR, "ingredient", img_file),
                    ])

               # =========================================
               # LOAD ẢNH
               # =========================================
               found_path = None
               for path in possible_paths:
                    if os.path.exists(path):
                         found_path = path
                         break

               if found_path:
                    pix = QPixmap(found_path)
               else:
                    print(f"[IMAGE NOT FOUND] {img_file}")

               card = FoodCard(name, kcal, desc, nutrients, pix)
               row = i // 2
               col = i % 2

               self.grid_layout.addWidget(card, row, col)

          # Cuộn về đầu sau khi nạp xong
          self.scroll_area.verticalScrollBar().setValue(0)
          self.custom_scrollbar.update()

     # ===========================================================
     # HÀM CHUYỂN TAB
     # ===========================================================
     def select_tab(self, index):
          ACTIVE_COLOR_1 = "#5C94FA"
          ACTIVE_COLOR_2 = "#3B6FD4"

          STYLE_ACTIVE = f"""
               QFrame {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                         stop:0 {ACTIVE_COLOR_1}, stop:1 {ACTIVE_COLOR_2});
                    border-radius: 10px;
                    border: none;
               }}
          """
          STYLE_INACTIVE = "QFrame { background: transparent; border: none; }"

          # Map index → key dữ liệu
          tab_keys = ["all", "food", "ingredient", "drink"]

          for i, (frame, lbl_text) in enumerate(self.tab_frames):
               if i == index:
                    frame.setStyleSheet(STYLE_ACTIVE)
                    lbl_text.setStyleSheet("border: none; background: transparent; color: white;")
               else:
                    frame.setStyleSheet(STYLE_INACTIVE)
                    lbl_text.setStyleSheet("border: none; background: transparent; color: #1a1a1a;")

          # Nạp dữ liệu tương ứng
          self.current_tab = index
          self._load_tab_data(tab_keys[index])

# ── Helper: kiểm tra file ảnh món ăn ─────────────────────────────────────────
# food_image_map dùng riêng — chỉ kiểm tra ảnh (không có video như gym)
# Dùng `os` có sẵn từ dòng đầu file, không import thêm

FILE_FOUND     = "✓ Có file"
FILE_NOT_FOUND = "✗ Không tìm thấy file"

def check_image(img_path: str) -> str:
    """
    Kiểm tra 1 đường dẫn ảnh món ăn có tồn tại không.

    Tham số:
        img_path : đường dẫn tuyệt đối hoặc tương đối tới file ảnh

    Trả về:
        "✓ Có file"           — file tồn tại, có thể QPixmap(img_path) ngay
        "✗ Không tìm thấy file" — file chưa có, hiện placeholder thay vì crash

    Dùng trong page_almanac.py (_load_tab_data):
        _st = check_image(found_path)
        if _st == FILE_FOUND:
            pix = QPixmap(found_path)
        else:
            print(f"{_st}: {img_file}")   # in rõ tên file thiếu
    """
    return FILE_FOUND if os.path.exists(img_path) else FILE_NOT_FOUND