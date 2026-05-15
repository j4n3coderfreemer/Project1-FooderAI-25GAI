"""
PHÂN XƯỞNG BACK-END: NUTRITION LOGIC ENGINE
Nhiệm vụ: Thực hiện các phép tính toán học chuyên sâu về dinh dưỡng theo chuẩn y khoa.
Đầu ra của phân xưởng này sẽ được đưa lên các StatCard trên giao diện.
"""

class NutritionLogic:
    @staticmethod
    def calculate_bmi(weight, height_cm):
        """
        THUẬT TOÁN TÍNH CHỈ SỐ KHỐI CƠ THỂ (BMI - Body Mass Index)
        1. Cơ sở khoa học: Tính toán BMI là bước cốt lõi trong module dinh dưỡng để đánh giá thể trạng cơ bản.
        2. Công thức chứng minh: Tỷ lệ giữa trọng lượng cơ thể và bình phương chiều cao (BMI = W / H^2).
        3. Trong đó: W là cân nặng tính bằng kilogram (kg) và H là chiều cao tính bằng mét (m).
        4. Ý nghĩa y khoa: Thuật toán giúp hệ thống Fooder AI phân loại người dùng một cách tự động.
        5. Chuyển đổi dữ liệu: Hệ thống ép kiểu và tính toán H_m = H_cm / 100 để đúng hệ quy chiếu mét.
        """
        if height_cm <= 0: return 0
        height_m = height_cm / 100
        bmi = weight / (height_m * height_m)
        return round(bmi, 1)

    @staticmethod
    def calculate_bmr(weight, height_cm, age, gender="male"):
        """
        THUẬT TOÁN TÍNH TỈ LỆ TRAO ĐỔI CHẤT CƠ BẢN (BMR - Basal Metabolic Rate)
        1. Cơ sở khoa học: BMR là calo tối thiểu cơ thể cần để duy trì sự sống khi nghỉ ngơi hoàn toàn.
        2. Lựa chọn thuật toán: Sử dụng phương trình Mifflin-St Jeor cho độ chính xác cao nhất hiện nay.
        3. Công thức tổng quát: BMR = (10 * W) + (6.25 * H) - (5 * A) + Biến số giới tính (S).
        4. Biến số giới tính (S): Thuật toán cộng thêm 5 cho Nam và trừ đi 161 cho Nữ.
        5. Vai trò: Giúp AI xác định ngưỡng calo không được phép ăn dưới mức này để tránh suy nhược.
        """
        if gender.lower() == "male":
            return int(10 * weight + 6.25 * height_cm - 5 * age + 5)
        else:
            return int(10 * weight + 6.25 * height_cm - 5 * age - 161)

    @staticmethod
    def calculate_tdee(bmr, activity_level=1.2):
        """
        THUẬT TOÁN TÍNH TỔNG NĂNG LƯỢNG TIÊU HAO HẰNG NGÀY (TDEE)
        1. Cơ sở khoa học: TDEE phản ánh toàn bộ calo đốt cháy trong 24h bao gồm cả vận động.
        2. Công thức chứng minh: TDEE = BMR * Hệ số vận động (Activity Factor).
        3. Ứng dụng: Đây là 'con số vàng' để AI thiết lập mục tiêu tăng hoặc giảm cân cho người dùng.
        """
        return int(bmr * activity_level)