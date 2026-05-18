import os
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QWidget, QGraphicsDropShadowEffect, QStackedWidget, QScrollArea, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QPixmap


class PageFoodScanner(QFrame):
     def __init__(self, parent=None):
          super().__init__(parent)
          self.setFixedSize(1240,640)

          self.setStyleSheet("""
            PageFoodScanner { background-color: white; border: 3px solid rgba(0, 77, 77, 0.5); border-radius: 24px; }
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
          # PHẦN 1: BANNER TIÊU ĐỀ (cấu trúc giống almanac)
          # ===========================================================
          self.banner = QFrame()
          self.banner.setFixedSize(1210, 60)

          color_hex = "#F4960C"
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

          # Layout ngang cho banner (giống almanac)
          banner_layout = QHBoxLayout(self.banner)
          banner_layout.setContentsMargins(3, 0, 12, 0)
          banner_layout.setSpacing(0)

          title_group = QWidget()
          title_group.setStyleSheet("background: transparent;")
          title_layout = QHBoxLayout(title_group)
          title_layout.setContentsMargins(7, 0, 3, 0)
          title_layout.setSpacing(5)

          # Icon tiêu đề (dùng icon scan riêng)
          title_icon = QLabel()
          tab_icon_path = os.path.join("assets", "fooderai-scanfood", "fooderai-scanfood-logo.png")
          if os.path.exists(tab_icon_path):
               title_icon.setPixmap(
                    QPixmap(tab_icon_path).scaledToHeight(45, Qt.TransformationMode.SmoothTransformation))
          title_icon.setStyleSheet("border: none; background: transparent;")

          title_text = QLabel("Quét món ăn")
          title_text.setStyleSheet("""
               color: white; border: none;
               font-family: 'Roboto'; font-size: 25px; font-weight: 800;
          """)

          title_layout.addWidget(title_icon)
          title_layout.addWidget(title_text)

          banner_layout.addWidget(title_group, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
          banner_layout.addStretch()

          main_layout.addWidget(self.banner, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

          # ===========================================================
          # PHẦN 2: CONTENT STACK — 2 trạng thái chồng nhau
          # QStackedWidget = "máy chiếu slide": index 0 = upload, index 1 = kết quả AI
          # ===========================================================
          self.content_stack = QStackedWidget()
          self.content_stack.setFixedSize(1210, 550)

          # --- TRANG 0: UPLOAD BOX — icon camera, click để chọn ảnh ---
          self.upload_box = QFrame()
          self.upload_box.setFixedSize(1210, 550)
          self.upload_box.setStyleSheet(
               "QFrame { background-color: white; border: 2px solid #F9C070; border-radius: 8px; }")
          self.upload_box.setCursor(Qt.CursorShape.PointingHandCursor)
          self.upload_box.mousePressEvent = lambda event: self._flash_and_open()

          upload_layout = QVBoxLayout(self.upload_box)
          upload_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
          upload_layout.setSpacing(10)

          self.lbl_upload_icon = QLabel()
          self.lbl_upload_icon.setStyleSheet("border: none; background: transparent;")
          self.lbl_upload_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
          icon_attach_path = os.path.join("assets", "fooderai-scanfood", "fdai-foodscan-photoattach.png")
          if os.path.exists(icon_attach_path):
               self.lbl_upload_icon.setPixmap(
                    QPixmap(icon_attach_path).scaledToHeight(72, Qt.TransformationMode.SmoothTransformation))

          self.lbl_upload_text = QLabel("Nhấn để tải ảnh hoặc chụp ảnh")
          font_upload = QFont("Roboto")
          font_upload.setPixelSize(20)
          font_upload.setWeight(QFont.Weight.Medium)
          font_upload.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1.1)
          self.lbl_upload_text.setFont(font_upload)
          self.lbl_upload_text.setStyleSheet("color: #888888; border: none;")
          self.lbl_upload_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

          upload_layout.addWidget(self.lbl_upload_icon)
          upload_layout.addWidget(self.lbl_upload_text)

          # --- TRANG 1: KẾT QUẢ AI — ảnh trái + thông tin phải ---
          self.result_box = QFrame()
          self.result_box.setFixedSize(1210, 550)
          self.result_box.setStyleSheet(
               "QFrame { background-color: white; border: 2px solid #F9C070; border-radius: 8px; }")

          result_layout = QHBoxLayout(self.result_box)
          result_layout.setContentsMargins(12, 12, 0, 12)
          result_layout.setSpacing(12)

          # [LEFT] nút back + ảnh 500x500
          left_col = QVBoxLayout()
          left_col.setSpacing(8)
          left_col.setContentsMargins(0, 0, 0, 0)

          self.btn_back = QPushButton("◄")
          self.btn_back.setFixedSize(44, 44)
          self.btn_back.setStyleSheet("""
                         QPushButton { background-color: #FDD58D; border: 2px solid #F4960C; border-radius: 8px; font-size: 18px; color: #7A4000; }
                         QPushButton:hover { background-color: #F4960C; color: white; }
                    """)
          self.btn_back.clicked.connect(lambda: self.content_stack.setCurrentIndex(0))

          self.lbl_food_img = QLabel()
          self.lbl_food_img.setFixedSize(500, 500)
          self.lbl_food_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
          self.lbl_food_img.setStyleSheet(
               "QLabel { border: 3px solid #FDD58D; border-radius: 12px; background-color: #FFF8EE; }")
          img_shadow = QGraphicsDropShadowEffect()
          img_shadow.setBlurRadius(20)
          img_shadow.setOffset(0, 0)
          img_shadow.setColor(QColor(0, 0, 0, 120))
          self.lbl_food_img.setGraphicsEffect(img_shadow)

          left_col.addWidget(self.btn_back, alignment=Qt.AlignmentFlag.AlignLeft)
          left_col.addWidget(self.lbl_food_img)
          left_col.addStretch()

          # [RIGHT] scroll area màu cam + nội dung AI
          self.scroll_area = QScrollArea()
          self.scroll_area.setWidgetResizable(True)
          self.scroll_area.setStyleSheet("""
                         QScrollArea { background-color: #EF8511; border: none; border-radius: 0px; }
                         QScrollBar:vertical { background: #C96800; width: 12px; border-radius: 6px; }
                         QScrollBar::handle:vertical { background: #FDD58D; border-radius: 6px; min-height: 30px; }
                         QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
                    """)

          self.result_content = QWidget()
          self.result_content.setStyleSheet("background-color: #EF8511;")
          content_inner_layout = QVBoxLayout(self.result_content)
          content_inner_layout.setContentsMargins(20, 20, 20, 20)
          content_inner_layout.setSpacing(10)

          self.lbl_food_name = QLabel("TÊN MÓN ĂN")
          font_name = QFont("Roboto")
          font_name.setPixelSize(36)
          font_name.setWeight(QFont.Weight.Black)
          self.lbl_food_name.setFont(font_name)
          self.lbl_food_name.setStyleSheet("color: #FFEBB3; border: none; background: transparent;")
          self.lbl_food_name.setWordWrap(True)

          divider = QFrame()
          divider.setFixedHeight(2)
          divider.setStyleSheet("background-color: #FFEBB3; border: none;")

          self.lbl_food_desc = QLabel("Đang phân tích món ăn...")
          font_desc = QFont("Roboto")
          font_desc.setPixelSize(20)
          self.lbl_food_desc.setFont(font_desc)
          self.lbl_food_desc.setStyleSheet("color: #FFEBB3; border: none; background: transparent;")
          self.lbl_food_desc.setWordWrap(True)
          self.lbl_food_desc.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

          content_inner_layout.addWidget(self.lbl_food_name)
          content_inner_layout.addWidget(divider)
          content_inner_layout.addWidget(self.lbl_food_desc)
          content_inner_layout.addStretch()

          self.scroll_area.setWidget(self.result_content)
          result_layout.addLayout(left_col)
          result_layout.addWidget(self.scroll_area, 1)

          # Nạp 2 trang vào stack, mặc định hiện trang 0
          self.content_stack.addWidget(self.upload_box)
          self.content_stack.addWidget(self.result_box)
          self.content_stack.setCurrentIndex(0)

          main_layout.addWidget(self.content_stack, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

     def _on_upload_clicked(self):
          from PySide6.QtWidgets import QFileDialog
          file_path, _ = QFileDialog.getOpenFileName(
               self, "Chọn ảnh món ăn", "",
               "Ảnh (*.png *.jpg *.jpeg *.webp)"
          )
          if not file_path:
               print("[SCAN] Người dùng hủy chọn ảnh.")
               return

          print(f"[SCAN] Đã nhận ảnh: {file_path}")

          # Hiển thị ảnh vào lbl_food_img, scale vừa 500x500 giữ tỉ lệ
          pixmap = QPixmap(file_path).scaled(
               500, 500,
               Qt.AspectRatioMode.KeepAspectRatio,
               Qt.TransformationMode.SmoothTransformation
          )
          self.lbl_food_img.setPixmap(pixmap)

          # Đặt text placeholder chờ AI — sau này thay bằng gọi API thật
          self.lbl_food_name.setText("Đang nhận diện món ăn...")
          self.lbl_food_desc.setText("⏳ AI đang phân tích ảnh, vui lòng chờ...")

          # Chuyển sang trang kết quả (index 1)
          self.content_stack.setCurrentIndex(1)
          print("[SCAN] Đã chuyển sang trang kết quả.")

     def _flash_and_open(self):
          # [1] Đổi nền sang màu vàng cam nhạt #FBF4BD ngay lập tức
          self.upload_box.setStyleSheet("""
               QFrame { background-color: #FBF4BD; border: 2px solid #F9C070; border-radius: 8px; } #sửa màu tại đây
          """)

          # [2] QTimer.singleShot = hẹn giờ 1 lần, sau 30ms tự động chạy lambda
          #     → Trả nền về trắng rồi mở hộp thoại file
          from PySide6.QtCore import QTimer
          QTimer.singleShot(30, lambda: (
               self.upload_box.setStyleSheet("""
                    QFrame { background-color: white; border: 2px solid #F9C070; border-radius: 8px; }
               """),
               self._on_upload_clicked()
          ))