import os
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QPixmap


class PageExercise(QFrame):
     def __init__(self, parent=None):
          super().__init__(parent)
          self.setFixedSize(1240,640)

          self.setStyleSheet("""
            PageExercise { background-color: white; border: 3px solid rgba(0, 77, 77, 0.5); border-radius: 24px; }
        """)

          box_shadow = QGraphicsDropShadowEffect()
          box_shadow.setBlurRadius(5)
          box_shadow.setOffset(0, 3)
          box_shadow.setColor(QColor(150, 150, 150, 180))
          self.setGraphicsEffect(box_shadow)

          main_layout = QVBoxLayout(self)
          main_layout.setContentsMargins(15, 10, 15, 15)

          self.banner = QFrame()
          self.banner.setFixedSize(1210, 60)

          color_hex = "#D250F6"
          base_color = QColor(color_hex)
          color_80, color_100 = base_color.darker(109).name(), base_color.darker(131).name()

          """
          ================================================================================
          [GIẢI THÍCH THUẬT TOÁN: TẠI SAO RA ÁNG CHỪNG 80 ĐỘ?]
          ================================================================================
          1. CƠ CHẾ NỘI SUY (LINEAR INTERPOLATION):
          - Qt xác định một đoạn thẳng nối từ A(x1, y1) đến B(x2, y2) làm trục chuẩn.
          - Với mọi pixel P trên Banner, nó tính giá trị t = (P hình chiếu lên AB) / độ dài AB.
          - Giá trị t (từ 0 đến 1) sẽ quyết định màu sắc tại pixel đó dựa trên các 'stop'.

          2. TOÁN HỌC GÓC NGHIÊNG:
          - Ta có Vector hướng $\vec{u} = (x2 - x1, y1 - y2)$ (đảo y vì trục y màn hình hướng xuống).
          - Độ dốc hình học (Slope) $m = \frac{\Delta y}{\Delta x} = \frac{1 - 0.2}{1 - 0} = 0.8$.
          - Góc thuần túy $\theta = \arctan(0.8) \approx 38.6^\circ$.

          3. HIỆU ỨNG TỈ LỆ KHUNG HÌNH (ASPECT RATIO COMPENSATION):
          - Vì Banner của em rất "dẹt" (Rộng 1210px, Cao chỉ 60px).
          - Một đơn vị di chuyển theo chiều dọc (Y) thực tế chỉ dài 60px, trong khi một đơn vị 
          theo chiều ngang (X) dài tới 1210px.
          - Công thức góc nhìn thực tế: alpha = arctan((delta(y) × width) / (delta(x) × height))
          - Tính toán: alpha = arctan((0.8 x 1210) / 1 x 60)) = arctan(16.13) ~= 86.4°
          => Kết quả: Nhờ sự chênh lệch tỉ lệ cực lớn giữa Width và Height, góc nghiêng 
          bị dựng đứng lên, tạo ra hiệu ứng chuyển sắc xéo ~80-85 độ cực đẹp.
          ================================================================================
          """

          # MINH CHỨNG CÂU LỆNH ĐÃ ÁP DỤNG:
          self.banner.setStyleSheet(f"""
                    QFrame {{
                    background-color: qlineargradient(
                    x1:0, y1:0.2,     /* Bắt đầu: Gần góc Trên - Phải */
                    x2:1, y2:1,       /* Kết thúc: Góc Dưới - Trái */
                    stop:0 {color_hex}, 
                    stop:0.8 {color_80}, 
                    stop:1.0 {color_100}
                    );
                    border-radius: 15px;
                    border: none;
               }}
          """)

          banner_shadow = QGraphicsDropShadowEffect()
          banner_shadow.setBlurRadius(2)
          banner_shadow.setOffset(0, 0)
          banner_shadow.setColor(QColor(0, 0, 0, 204))
          self.banner.setGraphicsEffect(banner_shadow)
          main_layout.addWidget(self.banner, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

          self.content_box = QWidget()
          content_layout = QVBoxLayout(self.content_box)
          content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
          content_layout.setSpacing(3)

          self.lbl_icon = QLabel()
          self.lbl_icon.setFixedHeight(45)
          self.lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
          icon_path = os.path.join("assets", "fooderai-blockcomponent", "fooderai-exercise-assistant.png")
          if os.path.exists(icon_path):
               self.lbl_icon.setPixmap(
                    QPixmap(icon_path).scaledToHeight(45, Qt.TransformationMode.SmoothTransformation))

          self.lbl_text1 = QLabel('Chức năng "Chế độ thể dục"')
          self.lbl_text1.setFont(QFont("Roboto Condensed", 25, QFont.Weight.Bold))
          self.lbl_text1.setStyleSheet("color: #266066; border: none;")
          self.lbl_text1.setAlignment(Qt.AlignmentFlag.AlignCenter)

          self.lbl_text2 = QLabel("Xin lỗi quý khách, chức năng này đang được cập nhật")
          self.lbl_text2.setFont(QFont("Roboto SemiCondensed", 18))
          self.lbl_text2.setStyleSheet("color: #666666; border: none;")
          self.lbl_text2.setAlignment(Qt.AlignmentFlag.AlignCenter)

          content_layout.addWidget(self.lbl_icon)
          content_layout.addWidget(self.lbl_text1)
          content_layout.addWidget(self.lbl_text2)
          main_layout.addWidget(self.content_box, 1)