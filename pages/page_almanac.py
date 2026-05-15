import os
# [MỚI] Thêm QHBoxLayout (Dàn hàng ngang), QLineEdit (Ô nhập chữ), QEvent (Bắt sự kiện click chuột)
# [MỚI v2] Thêm QScrollArea, QScrollBar, QGridLayout để tạo lưới 2 cột + cuộn
from PySide6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel,
                               QWidget, QGraphicsDropShadowEffect, QLineEdit,
                               QScrollArea, QScrollBar, QGridLayout, QSizePolicy)
from PySide6.QtCore import Qt, QEvent, QRect, QPoint, QSize
from PySide6.QtGui import QFont, QColor, QPixmap, QPainter, QPainterPath, QLinearGradient, QBrush, QPen, QRadialGradient
# insert file vô làm rõ vấn đề về thức ăn
from pages.food_image_map import FOOD_DATA  # Nguồn dữ liệu duy nhất — không lưu data ở đây nữa


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
# TRANG CHÍNH: PAGE FOOD ALMANAC
# =====================================================================
class PageFoodAlmanac(QFrame):
     def __init__(self, parent=None):
          super().__init__(parent)
          self.setFixedSize(1240, 640)
          self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
          self.current_tab = 0  # Tab đang chọn

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
               title_icon.setPixmap(
                    QPixmap(tab_icon_path).scaledToHeight(45, Qt.TransformationMode.SmoothTransformation))

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
          banner_layout.addWidget(self.search_bar,
                                  alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

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
                    lbl_icon.setPixmap(
                         QPixmap(loop_icon_path).scaledToHeight(70, Qt.TransformationMode.SmoothTransformation))

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

          # --- KHU VỰC PHẢI: KHUNG CHỨA GRID + SCROLLBAR ---
          right_container = QFrame()
          right_container.setFixedSize(980, 540)

          right_container.setStyleSheet("""
              QFrame {
                  background-color: #FFFFFF;
                  border: 2px solid #004d4d;
                  border-radius: 12px;
              }
          """)

          right_h_layout = QHBoxLayout(right_container)
          right_h_layout.setContentsMargins(8, 8, 8, 8)
          right_h_layout.setSpacing(6)

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
                    background: transparent;
                    border: none;
               }

               QScrollArea > QWidget > QWidget {
                    background: transparent;
               }
          """)

          # Widget nội dung bên trong ScrollArea
          self.grid_widget = QWidget()
          self.grid_widget.setStyleSheet("background: transparent;")
          self.grid_layout = QGridLayout(self.grid_widget)
          self.grid_layout.setContentsMargins(12, 12, 12, 12)
          # [FIX SCROLL]
          # Cho phép grid co giãn đúng chiều cao để scrollbar nhận diện được nội dung dài
          self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

          # [FIX SCROLL]
          # Ép widget bên trong tự mở rộng theo chiều dọc
          self.grid_widget.setSizePolicy(
               QSizePolicy.Policy.Expanding,
               QSizePolicy.Policy.Minimum
          )

          # 2 cột đều nhau: setColumnStretch đảm bảo col 0 và col 1 giãn bằng nhau
          self.grid_layout.setHorizontalSpacing(10)
          self.grid_layout.setVerticalSpacing(10)
          self.grid_layout.setColumnStretch(0, 1)
          self.grid_layout.setColumnStretch(1, 1)

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

          # Kích hoạt tab đầu tiên — gọi trực tiếp vì mọi widget đã sẵn sàng ở đây
          self.select_tab(0)

          # ========================================================================
          # KẾT NỐI SIGNAL LIVE SEARCH
          # ========================================================================
          """
          Mỗi khi nội dung ô nhập thay đổi (gõ thêm, xóa bớt, paste...),
          Qt tự động phát signal này và gọi hàm được kết nối — ở đây là
          self._on_search_changed — truyền vào chuỗi text hiện tại.

          Cú pháp kết nối signal:
              <widget>.<signal>.connect(<hàm_nhận>)

          Ở đây:
              self.search_bar          → CustomSearchBar (QFrame bọc ngoài)
              .input_box               → QLineEdit bên trong
              .textChanged             → signal phát mỗi khi text thay đổi
              .connect(...)            → đăng ký hàm lắng nghe
          """
          self.search_bar.input_box.textChanged.connect(self._on_search_changed)

     # ===========================================================
     # LIVE SEARCH — method của class, KHÔNG nằm trong __init__
     # ===========================================================
     def _on_search_changed(self, text: str):
          """
          Hàm này được signal textChanged gọi tự động.
          - self: bắt buộc vì đây là method của class
          - text: chuỗi Qt tự truyền vào mỗi khi nội dung ô nhập thay đổi
          """
          tab_keys = ["all", "food", "ingredient", "drink"]
          current_key = tab_keys[self.current_tab]
          self._load_tab_data(current_key, search_text=text.strip())

     # ===========================================================
     # HÀM NẠP DỮ LIỆU VÀO LƯỚI
     # ===========================================================
     def _load_tab_data(self, key, search_text: str = ""):
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

          if key == "all":
               items = (
                         FOOD_DATA.get("food", []) +
                         FOOD_DATA.get("ingredient", []) +
                         FOOD_DATA.get("drink", [])
               )
          else:
               items = FOOD_DATA.get(key, [])

          # ===========================================================
          # LỌC THEO TỪ KHÓA TÌM KIẾM (LIVE SEARCH)
          # ===========================================================
          """
          Thuật toán filter đơn giản, không phân biệt hoa thường:

          1. Chuẩn hóa: lower() → đưa cả keyword lẫn tên món về chữ thường
             VD: "Cà Chua" → "cà chua", "CÀ CHUA" → "cà chua"

          2. Kiểm tra: keyword in name.lower()
             → True nếu keyword xuất hiện BẤT KỲ ĐÂU trong tên
             VD: keyword="chua" → khớp "Cà chua", "Canh chua cá kho"

          3. Nếu search_text rỗng (chưa gõ gì) → giữ nguyên toàn bộ items
              Điều kiện: `if not keyword` → bỏ qua filter, lấy all
          """
          keyword = search_text.lower()  # Chuẩn hóa về chữ thường

          if keyword:
               items = [
                    item for item in items
                    if keyword in item[0].lower()  # item[0] = tên món
               ]

          # Hiện thông báo nếu không tìm thấy gì
          if not items:
               lbl_empty = QLabel(f'Không tìm thấy món nào với từ khóa "{search_text}"')
               lbl_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
               lbl_empty.setStyleSheet("color: #999; font-size: 15px; border: none;")

               self.grid_layout.addWidget(lbl_empty, 0, 0, 1, 2)
               self.scroll_area.verticalScrollBar().setValue(0)
               self.custom_scrollbar.update()
               return

          # Base folder chứa toàn bộ ảnh Almanac
          BASE_IMG_DIR = os.path.join("assets", "fooder-almanac-content")

          for i, (name, kcal, desc, nutrients, img_file) in enumerate(items):

               pix = None

               if key == "food":
                    subfolder = "food"
               elif key == "ingredient":
                    subfolder = "ingredient"
               elif key == "drink":
                    subfolder = "drink"
               else:
                    subfolder = None

               if subfolder:
                    img_path = os.path.join(BASE_IMG_DIR, subfolder, img_file)

                    if os.path.exists(img_path):
                         pix = QPixmap(img_path)
                    else:
                         print(f"[IMAGE NOT FOUND] {img_path}")

               else:
                    found = False

                    for folder in ["food", "ingredient", "drink"]:

                         img_path = os.path.join(BASE_IMG_DIR, folder, img_file)

                         if os.path.exists(img_path):
                              pix = QPixmap(img_path)
                              found = True
                              break

                    if not found:
                         print(f"[IMAGE NOT FOUND] {img_file}")

               # =====================================================
               # ADD CARD VÀO GRID
               # =====================================================
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
          # [FIX UI]
          # Tăng chiều cao card để text có không gian thở 😌
          self.setFixedHeight(135)

          # [FIX UI]
          # Giới hạn chiều rộng tối đa để grid 2 cột không bị ép #sửa tại đây
          self.setMaximumWidth(460)
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
          card_shadow.setBlurRadius(8)
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
               # Không hiện icon fallback nữa
               self.lbl_img.setText("")

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
          lbl_desc.setMaximumHeight(40)

          # Hàng 3: Nhãn dinh dưỡng
          nutrients_str = ", ".join(nutrients[:5]) if nutrients else ""
          lbl_nutrients = QLabel(f"⊕ DINH DƯỠNG: {nutrients_str.upper()}")
          nut_font = QFont("Roboto")
          nut_font.setPixelSize(11)
          nut_font.setWeight(QFont.Weight.Bold)
          lbl_nutrients.setFont(nut_font)
          lbl_nutrients.setStyleSheet("color: #2A7ADB; border: none; background: transparent;")

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
          self.scroll_area = scroll_area  # Tham chiếu đến vùng cuộn cần điều khiển
          self.setFixedWidth(22)  # Thanh cuộn rộng 22px
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
          track_x = (w - 12) // 2  # Rãnh rộng 12px, căn giữa theo chiều ngang

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
          ball_d = 18  # Đường kính quả cầu 18px
          travel_h = h - 8 - ball_d  # Khoảng di chuyển thực tế
          if travel_h <= 0:
               travel_h = 1

          # Tỉ lệ vị trí (0.0 → 1.0)
          ratio = (sb_val - sb_min) / max(1, sb_max - sb_min)
          ball_y = 4 + int(ratio * travel_h)  # Tọa độ Y trên cùng của quả cầu
          ball_cx = w // 2  # Tâm X (căn giữa thanh cuộn)
          ball_cy = ball_y + ball_d // 2  # Tâm Y

          # -----------------------------------------------
          # BƯỚC 4: VẼ QUẢ CẦU 3D (RADIAL GRADIENT)
          # Điểm sáng lệch góc trên-trái tạo cảm giác cầu phình ra
          # -----------------------------------------------
          ball_rect = QRect(ball_cx - ball_d // 2, ball_y, ball_d, ball_d)

          # Gradient radial: tâm sáng (trắng xanh) → viền tối (xanh đậm)
          ball_grad = QRadialGradient(
               ball_cx - ball_d * 0.2,  # Tiêu điểm X lệch trái 20%
               ball_cy - ball_d * 0.25,  # Tiêu điểm Y lệch lên 25%
               ball_d * 0.75  # Bán kính gradient
          )
          ball_grad.setColorAt(0.0, QColor("#AADEFF"))  # Điểm sáng nhất (trắng xanh nhạt)
          ball_grad.setColorAt(0.35, QColor("#5C94FA"))  # Màu xanh chính
          ball_grad.setColorAt(0.7, QColor("#2A5BBF"))  # Xanh trung
          ball_grad.setColorAt(1.0, QColor("#0D2A6A"))  # Viền tối nhất

          painter.setBrush(QBrush(ball_grad))
          painter.setPen(QPen(QColor("#0A2050"), 1))  # Viền ngoài quả cầu rất tối
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
               self.update()  # Vẽ lại thanh cuộn

     def mouseReleaseEvent(self, event):
          self._dragging = False

     def wheelEvent(self, event):
          """Cuộn bằng bánh xe chuột trên thanh cuộn"""
          sb = self.scroll_area.verticalScrollBar()
          delta = -event.angleDelta().y() // 3
          sb.setValue(sb.value() + delta)
          self.update()