# pages/gym_exercise_map.py
# ============================================================
# DỮ LIỆU BÀI TẬP THỂ DỤC — FOOER AI
# Demo 3 bài: Nhảy dây (Trẻ em) | Squat (Thanh niên) | Thở bụng (Người già)
# ============================================================
# Cấu trúc mỗi bài:
#   id          : str  — key định danh, khớp với tên file asset
#   ten         : str  — tên hiển thị
#   nhom_tuoi   : str  — "Trẻ em" | "Thanh niên" | "Người già"
#   thumbnail   : str  — đường dẫn tương đối từ thư mục gốc project
#   video       : str  — đường dẫn tương đối từ thư mục gốc project
#   tong_quan   : str  — 80–105 chữ
#   cac_buoc    : list[dict]  — tối đa 5 bước, mỗi bước có "so" và "noi_dung"
#   loi_ich     : list[str]  — đúng 3 ý, mỗi ý 45–60 chữ
#   luu_y       : list[str]  — đúng 3 ý, mỗi ý 45–60 chữ
# ============================================================

# BASE_DIR: thư mục gốc project (D:\FooderAI)
# Dùng __file__ của file này để tính ngược lên 1 cấp (pages/ → D:\FooderAI)
# Tránh lỗi os.path.exists trả False khi working directory không phải D:\FooderAI
import os as _os

BASE_DIR = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))

def _p(rel: str) -> str:
    """Chuyển đường dẫn tương đối → tuyệt đối từ thư mục gốc project"""
    return _os.path.join(BASE_DIR, rel.replace("/", _os.sep))


EXERCISE_MAP = {

    # ── NHẢY DÂY — Trẻ em ────────────────────────────────────────────
    "nhayday": {
        "id": "nhayday",
        "ten": "Nhảy dây trẻ em",
        "nhom_tuoi": "Trẻ em",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_nhayday_thumbnail.png"),
        "video":     _p("assets/fdai-gym-content/video/fdgym_nhayday_video.mp4"),

        "tong_quan": (
            "Nhảy dây là bài tập thể dục đơn giản, không cần dụng cụ phức tạp, "
            "chỉ cần một sợi dây và khoảng sân nhỏ là có thể bắt đầu ngay. "
            "Bài tập này giúp trẻ rèn luyện sức bền, tăng cường phối hợp tay-chân "
            "và phát triển thể lực toàn diện một cách tự nhiên, vui vẻ."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Cầm hai đầu dây, mỗi tay một đầu. Đứng thẳng, thả dây ra phía sau lưng, "
                    "chân rộng bằng vai, đầu gối hơi chùng nhẹ."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Vung dây qua đầu từ sau ra trước bằng cổ tay — không phải cả cánh tay. "
                    "Khi dây chạm đất phía trước, bật nhẹ hai chân lên vừa đủ để dây lướt qua."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Giữ nhịp đều đặn, mắt nhìn thẳng phía trước. "
                    "Bắt đầu đếm 10 cái rồi nghỉ, tăng dần lên 20 rồi 30 khi đã quen nhịp."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Thực hiện 2–3 hiệp, mỗi hiệp 30 lần nhảy, nghỉ 30 giây giữa các hiệp. "
                    "Thở đều bằng mũi khi nhảy, không nín thở."
                ),
            },
        ],

        "loi_ich": [
            (
                "Tăng cường sức bền tim mạch và phổi: nhảy dây liên tục kích thích hệ tuần hoàn "
                "hoạt động hiệu quả hơn, giúp trẻ có sức khỏe nền tốt và ít mệt mỏi trong học tập."
            ),
            (
                "Cải thiện phối hợp vận động toàn thân: động tác nhảy dây yêu cầu tay và chân "
                "phối hợp đồng thời, giúp não bộ và hệ thần kinh vận động phát triển nhanh hơn."
            ),
            (
                "Củng cố xương và cơ chân từ sớm: lực tác động nhẹ khi chạm đất là kích thích "
                "tự nhiên giúp mật độ xương tăng trưởng tốt trong giai đoạn phát triển chiều cao."
            ),
        ],

        "luu_y": [
            (
                "Chọn dây vừa chiều cao: đứng lên giữa dây, hai đầu kéo lên phải ngang tầm nách. "
                "Dây quá dài dễ vướng chân, dây quá ngắn không vung được nhịp đều."
            ),
            (
                "Nhảy trên nền phẳng, mềm: tránh sàn gạch cứng hoặc xi măng không bằng phẳng. "
                "Mang giày thể thao có đệm để bảo vệ khớp gối và mắt cá chân."
            ),
            (
                "Không nhảy khi vừa ăn no: chờ ít nhất 45 phút sau bữa ăn. Nếu thấy đau bên hông "
                "hoặc khó thở trong lúc nhảy, dừng lại nghỉ và uống nước bổ sung ngay."
            ),
        ],
    },

    # ── JUMPING JACK — Trẻ em ────────────────────────────────────────
    "jumpingjack": {
        "id": "jumpingjack",
        "ten": "Jumping Jack",
        "nhom_tuoi": "Trẻ em",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_jumpingjack_thumbnail.png"),
        "video":     _p("assets/fdai-gym-content/video/fdgym_jumpingjack_video.mp4"),

        "tong_quan": (
            "Jumping Jack là bài tập toàn thân không cần dụng cụ, thực hiện được ở bất kỳ "
            "đâu chỉ cần một khoảng trống nhỏ. Động tác bật chân và vỗ tay đồng thời "
            "giúp trẻ làm nóng cơ thể nhanh, tăng nhịp tim và rèn phối hợp vận động "
            "tay-chân một cách vui vẻ, dễ học."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Đứng thẳng, hai chân khép lại, hai tay thả dọc theo thân. "
                    "Lưng thẳng, mắt nhìn thẳng phía trước, cơ bụng hơi giữ nhẹ."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Bật nhẹ hai chân ra ngang rộng hơn vai, đồng thời đưa hai tay "
                    "lên cao vỗ nhau trên đỉnh đầu. Tay thẳng, không gập khuỷu."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Bật trở về tư thế ban đầu — chân khép, tay xuống — trong một nhịp liên tục. "
                    "Tiếp đất bằng mũi chân, không nện gót xuống sàn."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Thực hiện 20 cái liên tục rồi nghỉ 20 giây, lặp 3 hiệp. "
                    "Giữ nhịp đều, thở ra khi tay lên, hít vào khi tay xuống."
                ),
            },
        ],

        "loi_ich": [
            (
                "Khởi động toàn thân nhanh và hiệu quả: chỉ 30 giây Jumping Jack đã đủ "
                "làm nóng cơ bắp từ chân đến vai, giảm nguy cơ chấn thương khi chuyển "
                "sang các bài tập cường độ cao hơn."
            ),
            (
                "Tăng nhịp tim và sức bền tim mạch: động tác bật liên tục kích thích "
                "hệ tuần hoàn, giúp trẻ cải thiện sức bền nền và ít thở dốc khi "
                "chạy hoặc chơi thể thao sau này."
            ),
            (
                "Rèn phối hợp tay-chân và cảm giác nhịp điệu: yêu cầu tay và chân "
                "chuyển động đồng bộ giúp não bộ xử lý tín hiệu vận động nhanh hơn, "
                "hỗ trợ trẻ học các môn thể thao khác dễ dàng hơn."
            ),
        ],

        "luu_y": [
            (
                "Tiếp đất bằng mũi chân, không bằng gót: nện gót mạnh liên tục tạo lực "
                "chấn lên khớp gối và cột sống. Mang giày thể thao có đệm, không tập "
                "chân trần trên sàn cứng."
            ),
            (
                "Không bật quá cao, giữ biên độ vừa phải: mục tiêu là nhịp đều chứ không "
                "phải bật thật cao. Bật thấp và nhanh an toàn hơn bật cao và mạnh, "
                "đặc biệt với trẻ mới bắt đầu."
            ),
            (
                "Dừng ngay nếu cảm thấy đau mắt cá hoặc đầu gối: đây là dấu hiệu kỹ thuật "
                "tiếp đất chưa đúng. Nghỉ và kiểm tra lại tư thế trước khi tiếp tục, "
                "không cố tập khi đang đau."
            ),
        ],
    },

    # ── CHẠY TẠI CHỖ NÂNG GỐI — Trẻ em ─────────────────────────────
    "chaytaicho": {
        "id": "chaytaicho",
        "ten": "Chạy tại chỗ nâng gối",
        "nhom_tuoi": "Trẻ em",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_chaytaicho_thumbnail.png"),
        "video":     _p("assets/fdai-gym-content/video/fdgym_chaytaicho_video.mp4"),

        "tong_quan": (
            "Chạy tại chỗ nâng gối là bài tập cardio đơn giản nhất có thể làm trong phòng "
            "mà không cần di chuyển. Động tác nâng gối cao ngang hông kết hợp đánh tay "
            "giúp tăng nhịp tim nhanh, đốt năng lượng hiệu quả và rèn sức bền "
            "cho trẻ chỉ trong vài phút mỗi ngày."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Đứng thẳng, hai chân rộng bằng hông, tay co tự nhiên như tư thế chạy bộ. "
                    "Cơ bụng giữ nhẹ, lưng thẳng không khom."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Nâng gối phải lên ngang hông đồng thời đánh tay trái ra trước. "
                    "Gối nâng tới mức vuông góc với sàn — không cần cao hơn."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Hạ chân phải xuống, lập tức nâng gối trái lên và đánh tay phải ra trước. "
                    "Giữ nhịp luân phiên đều đặn như đang chạy bộ tại chỗ."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Chạy liên tục 30 giây rồi nghỉ 15 giây, thực hiện 3 hiệp. "
                    "Thở đều qua mũi, không nín thở. Tăng dần lên 45 giây khi đã quen."
                ),
            },
        ],

        "loi_ich": [
            (
                "Đốt calo cao mà không cần không gian rộng: chạy tại chỗ 30 giây cường độ "
                "vừa tiêu hao tương đương chạy bộ thật, phù hợp tập trong nhà hoặc "
                "phòng học mà không ảnh hưởng hàng xóm."
            ),
            (
                "Tăng cường sức mạnh cơ đùi và cơ bắp chân: động tác nâng gối cao liên tục "
                "kích thích nhóm cơ trước đùi và bắp chân, giúp trẻ chạy nhanh hơn "
                "và bền hơn trong các hoạt động thể thao."
            ),
            (
                "Cải thiện sự tập trung và phản xạ: nhịp chạy đều đòi hỏi não bộ duy trì "
                "điều phối liên tục, kích thích sản sinh endorphin giúp trẻ tỉnh táo "
                "và tập trung tốt hơn sau khi tập."
            ),
        ],

        "luu_y": [
            (
                "Không nâng gối quá cao khi mới bắt đầu: gối nâng ngang hông là đủ. "
                "Cố nâng cao hơn khi chưa đủ sức dễ làm mất thăng bằng và té ngã, "
                "đặc biệt với trẻ nhỏ tuổi."
            ),
            (
                "Giữ thân trên thẳng, không ngả về trước: khom lưng khi chạy tại chỗ "
                "tạo áp lực sai lên cột sống thắt lưng. Nhìn thẳng và giữ vai thả lỏng "
                "để duy trì tư thế đúng suốt bài."
            ),
            (
                "Tập trên nền có ma sát tốt, không trơn trượt: sàn gạch men hoặc sàn ướt "
                "rất nguy hiểm khi chạy tại chỗ. Dùng thảm tập hoặc mang giày "
                "có đế chống trượt để đảm bảo an toàn."
            ),
        ],
    },

    # ── BẬT XA TẠI CHỖ — Trẻ em ─────────────────────────────────────
    "batxa": {
        "id": "batxa",
        "ten": "Bật xa tại chỗ",
        "nhom_tuoi": "Trẻ em",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_batxa_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_batxa_video.mp4"),

        "tong_quan": (
            "Bật xa tại chỗ là bài tập thể lực quen thuộc trong giờ thể dục tiểu học "
            "Việt Nam, không cần dụng cụ, chỉ cần một khoảng sân nhỏ. "
            "Động tác bật 2 chân về phía trước rèn sức mạnh cơ chân, "
            "tăng khả năng bật nhảy và giúp trẻ phát triển thể lực toàn diện."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Đứng thẳng, hai chân rộng bằng vai, mũi chân hướng thẳng. "
                    "Hai tay đưa ra phía trước ngang vai để chuẩn bị lấy đà."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Gập nhẹ đầu gối, đánh tay ra sau đồng thời hạ thấp trọng tâm — "
                    "đây là động tác lấy đà, giữ lưng thẳng, không khom."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Bật mạnh 2 chân, đánh tay ra trước để lấy đà, nhảy về phía trước "
                    "càng xa càng tốt. Tiếp đất bằng cả 2 chân cùng lúc, đầu gối hơi chùng."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Thực hiện 5 lần liên tiếp, nghỉ 30 giây, lặp 2–3 hiệp. "
                    "Có thể đánh dấu điểm rơi để theo dõi tiến bộ theo từng buổi tập."
                ),
            },
        ],

        "loi_ich": [
            (
                "Phát triển sức mạnh bùng nổ cơ chân: động tác bật xa kích hoạt "
                "toàn bộ cơ đùi, bắp chân và cơ mông cùng lúc, giúp trẻ chạy nhanh "
                "hơn và bật cao hơn trong các môn thể thao như bóng đá, bóng rổ."
            ),
            (
                "Rèn phản xạ và khả năng phối hợp toàn thân: bật xa đòi hỏi tay, "
                "chân và thân người phối hợp đồng bộ trong tích tắc, "
                "giúp não bộ và hệ thần kinh vận động phát triển tốt hơn."
            ),
            (
                "Tăng mật độ xương tự nhiên: lực tác động khi tiếp đất sau mỗi lần bật "
                "là kích thích cơ học giúp xương chân phát triển chắc khỏe, "
                "đặc biệt có lợi trong giai đoạn trẻ đang tăng trưởng chiều cao."
            ),
        ],

        "luu_y": [
            (
                "Tiếp đất bằng cả 2 chân, đầu gối hơi chùng: không tiếp đất bằng gót "
                "hay chỉ 1 chân vì dễ bị trẹo mắt cá. Tập tiếp đất mềm trước "
                "khi tăng cường độ bật xa hơn."
            ),
            (
                "Khởi động kỹ trước khi bật: xoay mắt cá chân, xoay đầu gối "
                "và nhảy nhẹ tại chỗ 30 giây trước khi bắt đầu. "
                "Cơ lạnh chưa khởi động dễ bị căng khi bật mạnh đột ngột."
            ),
            (
                "Tập trên nền phẳng, không trơn: sân gạch ướt hoặc sàn nhẵn "
                "rất nguy hiểm khi tiếp đất. Chọn sân đất, thảm tập "
                "hoặc sân xi măng khô ráo, mang giày thể thao có đế bám."
            ),
        ],
    },

    # ── VƯƠN NGƯỜI BUỔI SÁNG — Trẻ em ──────────────────────────────
    "vuonnguoi": {
        "id": "vuonnguoi",
        "ten": "Vươn người buổi sáng",
        "nhom_tuoi": "Trẻ em",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_vuonnguoi_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_vuonnguoi_video.mp4"),

        "tong_quan": (
            "Vươn người buổi sáng là bài tập khởi động quen thuộc nhất trong giờ thể dục "
            "tiểu học Việt Nam. Động tác đơn giản — đưa tay lên cao, sang ngang, cúi người — "
            "giúp cơ thể thức dậy hoàn toàn, tăng lưu thông máu và chuẩn bị "
            "cho các hoạt động trong ngày chỉ trong vài phút."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Đứng thẳng, hai chân rộng bằng vai, hai tay thả dọc thân. "
                    "Hít sâu một lần, thả lỏng vai và cổ trước khi bắt đầu."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Từ từ đưa hai tay lên cao qua đầu, hít vào — "
                    "vươn người lên thật cao như muốn chạm trần nhà, đứng lên đầu ngón chân."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Hạ tay xuống, đưa sang 2 bên ngang vai rồi cúi người về phía trước nhẹ nhàng, "
                    "thở ra — không cần cúi sâu, chỉ cần cảm nhận cơ lưng giãn ra."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Đứng thẳng lại, lặp lại toàn bộ động tác 8–10 lần theo nhịp đều đặn. "
                    "Thực hiện mỗi sáng sau khi thức dậy hoặc trước giờ học thể dục."
                ),
            },
        ],

        "loi_ich": [
            (
                "Đánh thức cơ thể sau giấc ngủ dài: các động tác vươn giãn giúp máu lưu thông "
                "trở lại toàn thân, xóa tan cảm giác mỏi cơ sau khi ngủ và giúp trẻ "
                "tỉnh táo, sẵn sàng cho buổi học mới."
            ),
            (
                "Tăng độ linh hoạt cột sống và cơ lưng: cúi người và vươn cao luân phiên "
                "kéo giãn nhóm cơ dựng cột sống, giúp trẻ ngồi học lâu mà ít mỏi lưng "
                "và duy trì tư thế thẳng tự nhiên hơn."
            ),
            (
                "Cải thiện hô hấp và tập trung: hít thở sâu kết hợp vươn người "
                "tăng lượng oxy vào não, giúp trẻ tập trung tốt hơn trong vòng "
                "15–20 phút đầu sau khi tập."
            ),
        ],

        "luu_y": [
            (
                "Vươn người từ từ, không giật mạnh: động tác quá nhanh hoặc giật cơ "
                "khi cơ thể chưa khởi động dễ gây căng cơ lưng và cổ. "
                "Giữ mỗi tư thế 2–3 giây thay vì chuyển liên tục."
            ),
            (
                "Không cúi gập người quá sâu nếu thấy căng: mỗi trẻ có độ linh hoạt "
                "khác nhau, chỉ cúi đến điểm thoải mái. Không cố ép người xuống "
                "chạm tay sàn nếu cơ lưng chưa đủ giãn."
            ),
            (
                "Thở đều trong suốt bài — không nín thở: hít vào khi vươn lên, "
                "thở ra khi hạ xuống hoặc cúi người. Nín thở làm mất tác dụng "
                "của bài và dễ gây chóng mặt nhẹ với trẻ nhỏ."
            ),
        ],
    },

    # ── XOAY KHỚP TOÀN THÂN — Trẻ em ────────────────────────────────
    "xoaykhop_kids": {
        "id": "xoaykhop_kids",
        "ten": "Xoay khớp toàn thân",
        "nhom_tuoi": "Trẻ em",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_xoaykhop_kids_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_xoaykhop_kids_video.mp4"),

        "tong_quan": (
            "Xoay khớp toàn thân là bài khởi động thể dục trường học kinh điển — "
            "xoay lần lượt từ cổ xuống vai, hông, gối đến mắt cá chân. "
            "Chỉ mất 3–4 phút nhưng giúp tất cả các khớp được làm nóng đều, "
            "giảm nguy cơ chấn thương khi chuyển sang vận động mạnh hơn."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Xoay cổ: nghiêng đầu sang trái — phải — trước — sau nhẹ nhàng, "
                    "mỗi hướng 3 lần. Không xoay tròn cổ 360 độ vì dễ chóng mặt."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Xoay vai: đưa 2 vai lên — ra sau — xuống — ra trước thành vòng tròn. "
                    "5 vòng ra sau rồi 5 vòng ra trước. Giữ lưng thẳng trong lúc xoay."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Xoay hông: đặt 2 tay lên hông, xoay vòng tròn sang trái 5 vòng "
                    "rồi đổi chiều 5 vòng — như xoay hula hoop tưởng tượng."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Xoay gối và mắt cá: đặt 2 tay lên đầu gối, xoay tròn nhẹ 5 vòng mỗi chiều. "
                    "Sau đó nhấc từng chân xoay mắt cá 5 vòng mỗi bên. Tổng thời gian 3–4 phút."
                ),
            },
        ],

        "loi_ich": [
            (
                "Làm nóng toàn bộ khớp trước khi vận động: dịch khớp được tiết ra "
                "khi xoay giúp bôi trơn bề mặt khớp, giảm ma sát và ngăn ngừa "
                "chấn thương khi trẻ chạy nhảy hoặc chơi thể thao sau đó."
            ),
            (
                "Tăng phạm vi chuyển động tự nhiên: xoay khớp đều đặn mỗi ngày "
                "giúp dây chằng và gân cơ dần linh hoạt hơn, trẻ vận động "
                "thoải mái hơn và ít bị cứng khớp vào buổi sáng."
            ),
            (
                "Xây dựng thói quen khởi động đúng cách từ nhỏ: trẻ học được "
                "nguyên tắc luôn khởi động trước khi tập — thói quen này "
                "bảo vệ sức khỏe xương khớp suốt cả cuộc đời."
            ),
        ],

        "luu_y": [
            (
                "Không xoay cổ tròn 360 độ: xoay tròn cổ đầy đủ gây áp lực lên "
                "đốt sống cổ và động mạch, dễ chóng mặt. Chỉ nghiêng đầu "
                "4 hướng trái-phải-trước-sau là đủ và an toàn."
            ),
            (
                "Xoay chậm và đều — không xoay giật cục: mục tiêu là làm nóng khớp "
                "chứ không phải kiểm tra độ linh hoạt. Xoay nhanh hoặc giật mạnh "
                "dễ kéo căng dây chằng khi cơ chưa đủ ấm."
            ),
            (
                "Dừng ngay nếu nghe tiếng kêu lạo xạo kèm đau: tiếng khớp kêu nhẹ "
                "khi xoay là bình thường. Nhưng nếu kèm theo đau nhức hoặc "
                "sưng thì cần dừng và báo người lớn kiểm tra."
            ),
        ],
    },

    # ── SQUAT — Thanh niên ────────────────────────────────────────────
    "squat_teen": {
        "id": "squat_teen",
        "ten": "Squat cơ bản",
        "nhom_tuoi": "Thanh niên",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_squat_teen_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_squat_teen_video.mp4"),

        "tong_quan": (
            "Squat là bài tập nền tảng của mọi chương trình gym, tác động đồng thời lên cơ đùi, "
            "cơ mông và cơ lõi. Không cần tạ khi mới bắt đầu — chỉ cần đúng tư thế là đủ "
            "để cơ thể thay đổi rõ rệt sau 3 đến 4 tuần tập đều đặn."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Đứng thẳng, hai chân rộng bằng vai hoặc hơn một chút, "
                    "mũi chân hướng ra ngoài khoảng 15–30 độ."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Đưa tay thẳng ra trước để giữ thăng bằng, hít sâu vào, "
                    "sau đó từ từ hạ hông xuống như đang ngồi vào ghế phía sau."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Xuống đến khi đùi song song với sàn hoặc thấp hơn nếu được. "
                    "Giữ lưng thẳng, ngực ưỡn ra, không để gối vượt quá mũi chân quá nhiều."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Đẩy gót chân xuống sàn để đứng lên, thở ra trong lúc đứng dậy. "
                    "Thực hiện 3 hiệp x 12 lần, nghỉ 60 giây giữa hiệp."
                ),
            },
        ],

        "loi_ich": [
            (
                "Phát triển cơ đùi và cơ mông toàn diện: squat kích hoạt nhóm cơ lớn nhất cơ thể, "
                "giúp tăng cơ hiệu quả và đốt calo cao hơn so với các bài cô lập đơn lẻ."
            ),
            (
                "Cải thiện sức mạnh lõi và ổn định cột sống: giữ lưng thẳng trong suốt động tác "
                "buộc cơ bụng và cơ lưng hoạt động liên tục, tăng độ vững chắc cho toàn thân."
            ),
            (
                "Tăng mật độ xương và sức khỏe khớp gối: tải trọng tự nhiên từ squat kích thích "
                "xương đùi và xương chày phát triển, giảm nguy cơ loãng xương về lâu dài."
            ),
        ],

        "luu_y": [
            (
                "Không để gối đổ vào trong: khi hạ xuống, đẩy gối ra ngoài theo hướng mũi chân. "
                "Gối xụp vào trong là lỗi phổ biến nhất và dễ gây chấn thương dây chằng nhất."
            ),
            (
                "Không cúi lưng hoặc ưỡn quá mức: lưng trung tính là vị trí an toàn nhất. "
                "Nếu không giữ được lưng thẳng khi xuống sâu, hãy thu hẹp biên độ lại trước."
            ),
            (
                "Khởi động kỹ trước khi squat nặng: xoay khớp hông, khớp gối và mắt cá tối thiểu "
                "5 phút. Nhảy vào squat lạnh ngay khi mới vào phòng tập dễ kéo căng cơ đột ngột."
            ),
        ],
    },

    # ── PUSH-UP — Thanh niên ─────────────────────────────────────────
    "pushup": {
        "id": "pushup",
        "ten": "Push-up (Chống đẩy)",
        "nhom_tuoi": "Thanh niên",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_pushup_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_pushup_video.mp4"),

        "tong_quan": (
            "Push-up là bài tập thân trên kinh điển nhất — không cần tạ, không cần máy, "
            "chỉ cần sàn nhà. Một động tác đúng kỹ thuật kích hoạt đồng thời cơ ngực, "
            "cơ vai, cơ tay sau và cơ lõi. Làm đúng 10 cái còn hiệu quả hơn "
            "làm ẩu 30 cái."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Chống 2 bàn tay xuống sàn, rộng hơn vai một chút. "
                    "Ngón tay hướng thẳng về phía trước, cánh tay thẳng. "
                    "Chống mũi 2 chân, toàn thân thành 1 đường thẳng từ đầu đến gót."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Siết cơ bụng và cơ mông — giữ suốt cả bài. "
                    "Hít vào, từ từ hạ người xuống bằng cách gập khuỷu tay ra sau "
                    "khoảng 45 độ so với thân — không dang khuỷu ra ngang."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Hạ xuống đến khi ngực cách sàn 2–3cm hoặc chạm nhẹ. "
                    "Giữ cổ thẳng với cột sống, mắt nhìn xuống sàn phía trước "
                    "khoảng 30cm — không ngẩng đầu lên."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Thở ra, đẩy người lên về tư thế ban đầu. "
                    "Thực hiện 3 hiệp x 10 lần, nghỉ 60 giây giữa hiệp. "
                    "Nếu chưa đủ sức, chống gối xuống sàn để giảm tải."
                ),
            },
        ],

        "loi_ich": [
            (
                "Phát triển cơ ngực, vai và tay sau toàn diện: push-up kích hoạt "
                "3 nhóm cơ thân trên cùng lúc, hiệu quả tương đương bench press "
                "nhưng không cần dụng cụ và an toàn hơn cho người mới tập."
            ),
            (
                "Củng cố cơ lõi mạnh mẽ: giữ thân thẳng trong suốt bài buộc "
                "cơ bụng và cơ lưng dưới hoạt động liên tục như một bài plank động, "
                "giúp tăng sự ổn định toàn thân."
            ),
            (
                "Tập được mọi lúc mọi nơi, không cần thiết bị: phòng ngủ, sân nhà "
                "hay phòng khách sách đều tập được. Không có lý do nào để bỏ buổi tập "
                "khi bài này chỉ cần đúng 1m² sàn trống."
            ),
        ],

        "luu_y": [
            (
                "Không để hông xệ xuống hoặc nhô lên: đây là lỗi phổ biến nhất. "
                "Hông xệ gây đau lưng, hông nhô làm mất tác dụng bài. "
                "Siết mông và bụng từ đầu đến cuối để giữ thân thẳng."
            ),
            (
                "Khuỷu tay ra sau 45 độ, không dang ngang: khuỷu dang ra ngang "
                "tạo áp lực sai lên khớp vai và dễ gây chấn thương. "
                "Hình dung mũi tên chữ V hướng về phía chân khi nhìn từ trên xuống."
            ),
            (
                "Bắt đầu bằng push-up gối nếu chưa đủ sức: không có gì sai khi "
                "chống gối — đây là biến thể chính thống giúp xây nền sức mạnh. "
                "Tập đủ 3x10 push-up gối trước khi chuyển lên push-up đầy đủ."
            ),
        ],
    },

    # ── LUNGE (bước dài) — Thanh niên ───────────────────────────────
    "lunge": {
        "id": "lunge",
        "ten": "Lunge (Bước dài)",
        "nhom_tuoi": "Thanh niên",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_lunge_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_lunge_video.mp4"),

        "tong_quan": (
            "Lunge là bài tập chân đơn phổ biến nhất trong gym, tập từng chân riêng lẻ "
            "giúp phát hiện và khắc phục chênh lệch sức mạnh 2 bên. "
            "Không cần dụng cụ, kích hoạt đồng thời cơ đùi trước, cơ mông "
            "và cơ bắp chân, cải thiện cân bằng và phối hợp vận động toàn thân."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Đứng thẳng, 2 chân rộng bằng hông, tay thả dọc thân hoặc "
                    "đặt lên hông. Nhìn thẳng phía trước, vai thả lỏng."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Bước chân phải dài về phía trước, hạ người xuống cho đến khi "
                    "đùi phải song song với sàn và gối trái gần chạm sàn."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Giữ lưng thẳng, gối phải không vượt quá mũi chân, "
                    "trọng tâm dồn đều 2 chân. Giữ 1 giây ở điểm thấp nhất."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Đẩy gót chân phải xuống sàn để đứng lên về tư thế ban đầu, "
                    "đổi sang chân trái. Thực hiện 3 hiệp x 10 reps mỗi chân, nghỉ 60 giây."
                ),
            },
        ],

        "loi_ich": [
            (
                "Phát triển cơ chân đều 2 bên: tập từng chân riêng giúp phát hiện "
                "chân yếu hơn và buộc cả 2 bên phải làm việc độc lập, "
                "ngăn ngừa mất cân bằng cơ dẫn đến chấn thương lâu dài."
            ),
            (
                "Cải thiện thăng bằng và phối hợp vận động: tư thế lunge yêu cầu "
                "ổn định hông và cổ chân liên tục, rèn luyện hệ thần kinh vận động "
                "hữu ích cho mọi môn thể thao."
            ),
            (
                "Tăng linh hoạt khớp hông: bước chân dài kéo giãn cơ hông gấp "
                "ở chân sau — nhóm cơ thường bị co cứng ở người ngồi nhiều, "
                "giúp giảm đau lưng dưới và cải thiện tư thế đi đứng."
            ),
        ],

        "luu_y": [
            (
                "Không để gối trước vượt quá mũi chân quá nhiều: một chút vượt qua "
                "là bình thường, nhưng vượt quá nhiều tạo áp lực lớn lên sụn khớp gối. "
                "Bước chân dài hơn nếu thấy gối hay vượt quá."
            ),
            (
                "Giữ thân trên thẳng, không ngả về trước: khom người ra trước "
                "chuyển tải trọng lên lưng thay vì chân. "
                "Giữ ngực ưỡn nhẹ và cằm song song với sàn suốt bài."
            ),
            (
                "Không để gối sau chạm sàn mạnh: hạ gối sau xuống chậm và kiểm soát, "
                "dừng cách sàn 2–3cm. Chạm sàn mạnh liên tục gây chai và đau "
                "phần xương bánh chè của chân sau."
            ),
        ],
    },

    # ── PLANK NÂNG CAO (full plank) — Thanh niên ─────────────────────
    "plank_nangcao": {
        "id": "plank_nangcao",
        "ten": "Plank nâng cao (Full Plank)",
        "nhom_tuoi": "Thanh niên",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_plank_nangcao_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_plank_nangcao_video.mp4"),

        "tong_quan": (
            "Plank nâng cao dùng 2 bàn tay thay vì khuỷu tay, tăng tải lên cơ vai "
            "và cơ lõi so với plank khuỷu tay thông thường. Đây là nền tảng "
            "của nhiều bài tập sàn khác như push-up và mountain climber, "
            "giúp toàn thân ổn định và chắc khỏe từ trong ra ngoài."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Chống 2 bàn tay xuống sàn rộng bằng vai, ngón tay hướng thẳng. "
                    "Chống mũi 2 chân, toàn thân thành 1 đường thẳng từ đầu đến gót."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Siết cơ bụng, cơ mông và cơ đùi — giữ suốt thời gian plank. "
                    "Không để hông xệ xuống hoặc nhô lên."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Nhìn xuống sàn, cổ thẳng với cột sống. "
                    "Thở đều và chậm — không nín thở. "
                    "Mỗi lần thở ra siết bụng thêm một chút."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Bắt đầu từ 30 giây, tăng dần 5–10 giây mỗi tuần. "
                    "Mục tiêu: 3 hiệp x 60 giây, nghỉ 45 giây giữa hiệp."
                ),
            },
        ],

        "loi_ich": [
            (
                "Kích hoạt toàn bộ cơ lõi sâu: plank tay kích thích cả rectus abdominis, "
                "transverse abdominis và cơ chéo bụng đồng thời — "
                "không bài tập bụng nào khác làm được điều này hiệu quả hơn."
            ),
            (
                "Tăng sức mạnh vai và cổ tay: chịu toàn bộ trọng lượng cơ thể trên bàn tay "
                "giúp cơ vai trước và cơ cẳng tay phát triển, "
                "hỗ trợ trực tiếp cho push-up và các bài tập sàn khác."
            ),
            (
                "Cải thiện tư thế và giảm đau lưng: cơ lõi mạnh hơn giúp cột sống "
                "được đỡ tốt hơn trong mọi hoạt động hằng ngày, "
                "từ ngồi làm việc đến mang vác đồ nặng."
            ),
        ],

        "luu_y": [
            (
                "Không để hông xệ xuống: đây là lỗi phổ biến nhất khi mệt. "
                "Nếu không giữ được thân thẳng, dừng nghỉ và làm hiệp mới — "
                "plank sai tư thế gây đau lưng, không có tác dụng."
            ),
            (
                "Không khóa cứng khuỷu tay: giữ khuỷu tay hơi mềm tự nhiên, "
                "không thẳng cứng hoàn toàn. Khóa khớp khuỷu lâu dài "
                "gây áp lực không cần thiết lên sụn khớp."
            ),
            (
                "Dừng ngay nếu thấy đau cổ tay: đau cổ tay khi plank thường do "
                "cổ tay chưa đủ linh hoạt hoặc góc chống tay sai. "
                "Thử xoay bàn tay ra ngoài 45 độ hoặc dùng nắm đấm để giảm áp lực."
            ),
        ],
    },

    # ── MOUNTAIN CLIMBER — Thanh niên ────────────────────────────────
    "mountainclimber": {
        "id": "mountainclimber",
        "ten": "Mountain Climber",
        "nhom_tuoi": "Thanh niên",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_mountainclimber_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_mountainclimber_video.mp4"),

        "tong_quan": (
            "Mountain Climber kết hợp plank và chạy tại chỗ trong cùng một động tác — "
            "giữ tư thế chống đẩy và co gối luân phiên vào ngực nhanh nhất có thể. "
            "Bài tập đốt calo cao, rèn cơ lõi, cơ vai và cardio cùng lúc "
            "mà không cần dụng cụ hay không gian rộng."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Bắt đầu từ tư thế plank tay — 2 bàn tay chống sàn rộng bằng vai, "
                    "toàn thân thẳng từ đầu đến gót. Siết cơ bụng."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Co gối phải kéo nhanh vào ngực, mũi chân phải gần chạm sàn dưới hông. "
                    "Hông giữ thẳng với vai — không nhô lên."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Bật chân phải về vị trí cũ đồng thời co gối trái vào ngực. "
                    "Thực hiện luân phiên nhanh nhất có thể như đang chạy."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Thực hiện liên tục 20 giây rồi nghỉ 10 giây, lặp 3 hiệp. "
                    "Tăng dần lên 30 giây khi đã quen. Thở đều, không nín thở."
                ),
            },
        ],

        "loi_ich": [
            (
                "Đốt calo cao và rèn cardio hiệu quả: mountain climber ở tốc độ cao "
                "tương đương chạy bộ về mức tiêu hao năng lượng, nhưng tập được "
                "trong phòng hẹp và không gây tiếng động lớn như nhảy."
            ),
            (
                "Rèn cơ lõi trong điều kiện động: khác với plank tĩnh, mountain climber "
                "buộc cơ lõi phải ổn định thân trong khi chân chuyển động nhanh — "
                "mô phỏng đúng cách cơ lõi hoạt động trong thực tế."
            ),
            (
                "Cải thiện sức bền vai và cánh tay: giữ tư thế chống tay liên tục "
                "trong khi chân chuyển động nhanh tạo ra thử thách lớn cho cơ vai, "
                "giúp push-up và các bài tập tay trở nên dễ hơn."
            ),
        ],

        "luu_y": [
            (
                "Không để hông nhô lên khi kéo gối vào: đây là lỗi phổ biến nhất. "
                "Hông nhô lên làm mất tác dụng cơ lõi và tạo áp lực sai lên lưng. "
                "Giảm tốc độ nếu không giữ được hông thẳng."
            ),
            (
                "Bắt đầu chậm, tăng tốc dần: người mới nên làm chậm như đi bộ "
                "để học đúng tư thế trước khi tăng tốc. "
                "Tốc độ sai tư thế không hiệu quả bằng chậm đúng tư thế."
            ),
            (
                "Giữ cổ tay thẳng với cẳng tay, không gập: cổ tay gập xuống sàn "
                "lâu gây đau và viêm cổ tay. Nếu sàn trơn, dùng thảm tập "
                "để bàn tay không bị trượt khi thực hiện nhanh."
            ),
        ],
    },

    # ── BURPEE — Thanh niên (bài 12) ─────────────────────────────────
    "burpee": {
        "id": "burpee",
        "ten": "Burpee",
        "nhom_tuoi": "Thanh niên",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_burpee_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_burpee_video.mp4"),

        "tong_quan": (
            "Burpee là bài tập toàn thân cường độ cao kết hợp squat, chống đẩy và bật nhảy "
            "trong một động tác liên hoàn. Không cần dụng cụ, chỉ cần 2m² sàn trống. "
            "10 cái burpee liên tục có thể đốt khoảng 10–15 calo — "
            "tương đương chạy bộ nhanh trong cùng khoảng thời gian."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Đứng thẳng, sau đó ngồi xổm xuống và đặt 2 tay xuống sàn "
                    "ngay trước mũi chân, rộng bằng vai."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Bật 2 chân ra sau về tư thế chống đẩy — toàn thân thẳng, "
                    "cơ bụng siết. Thực hiện 1 cái chống đẩy (bỏ qua nếu mới bắt đầu)."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Bật 2 chân về phía trước trở lại tư thế ngồi xổm, "
                    "tay vẫn đặt trên sàn, gối gần chạm ngực."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Đứng lên và bật nhảy thẳng lên cao, tay đưa lên đầu. "
                    "Thực hiện 3 hiệp x 8 reps, nghỉ 60–90 giây giữa hiệp."
                ),
            },
        ],

        "loi_ich": [
            (
                "Đốt calo cực cao trong thời gian ngắn: burpee kích hoạt hầu hết "
                "nhóm cơ lớn cùng lúc, 10 cái liên tục tiêu hao khoảng 10–15 calo, "
                "tương đương chạy bộ nhanh mà không cần không gian rộng."
            ),
            (
                "Tăng sức bền tim mạch và cơ bắp song song: không như cardio thông thường "
                "chỉ tập tim mạch, burpee đồng thời rèn cơ ngực, vai, bụng và chân "
                "trong mỗi lần lặp lại, tiết kiệm thời gian tập luyện."
            ),
            (
                "Không cần dụng cụ, tập được mọi lúc mọi nơi: phòng ngủ, khách sạn "
                "hay sân nhỏ đều tập được. Burpee là bài tập hiệu quả nhất "
                "tính theo tỷ lệ kết quả trên chi phí dụng cụ bỏ ra."
            ),
        ],

        "luu_y": [
            (
                "Không nhảy vào burpee khi chưa khởi động: cơ lạnh kết hợp động tác "
                "bùng nổ cao dễ kéo căng cơ đùi và cơ lưng. "
                "Khởi động ít nhất 5 phút trước khi bắt đầu."
            ),
            (
                "Người mới bỏ qua bước bật nhảy và chống đẩy trước: làm phiên bản đơn giản "
                "— ngồi xổm, bật chân ra sau, bật về, đứng lên — "
                "cho đến khi đủ sức thêm 2 động tác còn lại."
            ),
            (
                "Không để lưng võng khi ở tư thế chống đẩy: siết bụng và mông "
                "trong suốt bước này. Lưng võng dưới tải trọng lặp đi lặp lại "
                "là nguyên nhân phổ biến nhất gây đau thắt lưng khi tập burpee."
            ),
        ],
    },

    # ── GLUTE BRIDGE (cầu mông) — Thanh niên (bài 13) ────────────────
    "glutebridge": {
        "id": "glutebridge",
        "ten": "Glute Bridge (Cầu mông)",
        "nhom_tuoi": "Thanh niên",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_glutebridge_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_glutebridge_video.mp4"),

        "tong_quan": (
            "Glute Bridge là bài tập nằm ngửa giúp kích hoạt và phát triển cơ mông "
            "một cách chính xác và an toàn cho lưng. Không cần tạ, không cần máy, "
            "chỉ cần sàn nhà. Đây là bài tập nền tảng cho ai muốn cải thiện "
            "vóc dáng phần dưới và giảm đau lưng dưới hiệu quả."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Nằm ngửa trên sàn, hai gối gập, bàn chân đặt phẳng cách mông "
                    "khoảng 30cm. Hai tay để dọc theo thân, lòng bàn tay úp xuống sàn."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Siết cơ mông và đẩy hông lên cao cho đến khi vai, hông và gối "
                    "tạo thành một đường thẳng. Không ưỡn lưng quá mức."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Giữ tư thế trên cùng 2 giây, siết mông thật chặt. "
                    "Thở ra trong lúc đẩy lên, hít vào khi hạ xuống."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Hạ hông xuống chậm rãi, không để chạm sàn hoàn toàn giữa các rep. "
                    "Thực hiện 3 hiệp x 15 reps, nghỉ 45 giây giữa hiệp."
                ),
            },
        ],

        "loi_ich": [
            (
                "Kích hoạt và phát triển cơ mông toàn diện: glute bridge cô lập cơ mông "
                "tốt hơn squat vì loại bỏ sự tham gia của cơ đùi, "
                "giúp cơ mông được kích thích trực tiếp và phát triển nhanh hơn."
            ),
            (
                "Giảm đau lưng dưới hiệu quả: cơ mông yếu là nguyên nhân số 1 gây đau lưng "
                "ở người ngồi làm việc nhiều. Tập glute bridge đều đặn giúp cơ mông "
                "đỡ bớt tải cho cột sống thắt lưng."
            ),
            (
                "An toàn tuyệt đối, phù hợp mọi trình độ: không tải trọng lên cột sống "
                "hay khớp gối, nằm ngửa hoàn toàn. Phù hợp cả người mới bắt đầu "
                "lẫn người đang phục hồi chấn thương lưng."
            ),
        ],

        "luu_y": [
            (
                "Không ưỡn lưng quá mức ở đỉnh động tác: đường thẳng vai-hông-gối "
                "là giới hạn đúng — đẩy cao hơn mức đó gây áp lực sai lên cột sống. "
                "Siết bụng để kiểm soát biên độ."
            ),
            (
                "Đặt bàn chân đúng khoảng cách: quá gần mông làm cơ đùi sau căng quá, "
                "quá xa làm cơ đùi trước thay thế cơ mông. "
                "Thử đến khi cảm nhận rõ lực kéo ở mông là đúng vị trí."
            ),
            (
                "Siết mông ở đỉnh chứ không siết lưng: nhiều người vô tình ưỡn lưng "
                "thay vì đẩy bằng mông. Tập trung vào cơ mông — "
                "nếu thấy căng ở lưng là đang làm sai kỹ thuật."
            ),
        ],
    },

    # ── JUMPING SQUAT (squat bật) — Thanh niên (bài 14) ──────────────
    "jumpingsquat": {
        "id": "jumpingsquat",
        "ten": "Jumping Squat (Squat bật)",
        "nhom_tuoi": "Thanh niên",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_jumpingsquat_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_jumpingsquat_video.mp4"),

        "tong_quan": (
            "Jumping Squat là phiên bản bùng nổ của squat thường — thêm bước bật nhảy "
            "lên cao sau mỗi lần ngồi xuống. Bài tập tăng sức mạnh bùng nổ cơ chân, "
            "đốt nhiều calo hơn squat thường và cải thiện "
            "khả năng nhảy cao, chạy nhanh rõ rệt sau vài tuần tập."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Đứng rộng bằng vai, mũi chân hướng ra ngoài nhẹ. "
                    "Tay đưa ra trước hoặc khoanh trước ngực để giữ thăng bằng."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Ngồi xuống tư thế squat — đùi song song sàn, lưng thẳng, "
                    "gối không vượt quá mũi chân. Hít vào khi ngồi xuống."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Bật mạnh lên cao hết sức, tay đánh xuống để lấy đà. "
                    "Toàn thân rời khỏi sàn, thẳng người trong không trung."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Tiếp đất nhẹ nhàng bằng mũi chân, đầu gối hơi chùng để giảm xung. "
                    "Thực hiện 3 hiệp x 10 reps, nghỉ 60 giây giữa hiệp."
                ),
            },
        ],

        "loi_ich": [
            (
                "Tăng sức mạnh bùng nổ cơ chân: bật nhảy từ tư thế squat kích thích "
                "sợi cơ nhanh — loại sợi cơ chịu trách nhiệm cho tốc độ và sức mạnh "
                "tức thời mà squat thường không kích hoạt được."
            ),
            (
                "Đốt calo nhiều hơn squat thường 30–40%: yếu tố bật nhảy đẩy nhịp tim "
                "lên vùng cardio, biến bài tập sức mạnh thành bài tập kết hợp "
                "giảm mỡ hiệu quả hơn."
            ),
            (
                "Cải thiện khả năng thể thao toàn diện: bật cao, chạy nhanh, đổi hướng "
                "đột ngột trong các môn thể thao đều cần sức mạnh bùng nổ cơ chân — "
                "đúng thứ jumping squat rèn luyện mỗi buổi tập."
            ),
        ],

        "luu_y": [
            (
                "Tiếp đất mềm, không nện gót xuống sàn: tiếp đất cứng liên tục "
                "tạo lực chấn động lớn lên khớp gối và cột sống. "
                "Mang giày đệm tốt và tập trên sàn có độ đàn hồi."
            ),
            (
                "Không tập khi đầu gối đang đau: jumping squat tạo lực tác động cao "
                "lên khớp gối, không phù hợp khi khớp đang bị viêm hoặc chấn thương "
                "— dùng squat thường thay thế cho đến khi hồi phục."
            ),
            (
                "Làm nóng kỹ trước khi bắt đầu: xoay khớp hông, gối, mắt cá "
                "và 10 cái squat thường trước khi chuyển sang jumping squat. "
                "Cơ lạnh bật mạnh đột ngột rất dễ kéo căng cơ đùi."
            ),
        ],
    },

    # ── CALF RAISE (kiễng gót) — Thanh niên (bài 15) ─────────────────
    "calfraise": {
        "id": "calfraise",
        "ten": "Calf Raise (Kiễng gót)",
        "nhom_tuoi": "Thanh niên",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_calfraise_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_calfraise_video.mp4"),

        "tong_quan": (
            "Calf Raise là bài tập đơn giản nhất để phát triển cơ bắp chân — "
            "đứng thẳng và kiễng 2 gót lên cao. Có thể làm ở bậc thang để tăng biên độ. "
            "Bắp chân khỏe giúp chạy nhanh hơn, ít bị chuột rút "
            "và giảm nguy cơ chấn thương mắt cá chân khi vận động."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Đứng thẳng, 2 chân rộng bằng hông. Tay có thể tựa nhẹ vào tường "
                    "hoặc ghế để giữ thăng bằng — không dựa người vào."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Từ từ kiễng 2 gót lên cao nhất có thể, đứng trên đầu ngón chân. "
                    "Siết cơ bắp chân ở điểm cao nhất, giữ 1–2 giây."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Hạ gót xuống chậm rãi trong 2–3 giây — phần hạ xuống chậm "
                    "quan trọng không kém phần kiễng lên, đừng thả rơi tự do."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Thực hiện 3 hiệp x 20 reps, nghỉ 45 giây. "
                    "Nâng cao: đứng mũi chân trên bậc thang để gót có thể hạ thấp hơn sàn."
                ),
            },
        ],

        "loi_ich": [
            (
                "Phát triển cơ bắp chân cân đối: calf raise kích hoạt cả 2 đầu cơ bắp chân "
                "— gastrocnemius và soleus — giúp bắp chân phát triển đều "
                "và săn chắc hơn so với các bài tập toàn thân thông thường."
            ),
            (
                "Giảm nguy cơ chuột rút và chấn thương mắt cá: bắp chân mạnh hơn "
                "hỗ trợ khớp mắt cá tốt hơn, giảm tần suất chuột rút khi chạy "
                "và ngủ — vấn đề phổ biến ở người ít vận động."
            ),
            (
                "Cải thiện tuần hoàn máu từ chân lên tim: động tác co bắp chân "
                "hoạt động như bơm máu phụ, đẩy máu từ tĩnh mạch chân lên tim, "
                "giảm phù chân sau ngày dài ngồi làm việc."
            ),
        ],

        "luu_y": [
            (
                "Không nhún nhanh hoặc bật lên: động tác phải chậm và có kiểm soát "
                "cả chiều lên lẫn chiều xuống. Nhún nhanh dùng quán tính "
                "thay vì cơ bắp chân, mất đi phần lớn tác dụng bài tập."
            ),
            (
                "Không khóa cứng gối khi kiễng lên: giữ gối thẳng tự nhiên, "
                "không siết khớp gối hoàn toàn. Khóa gối cứng lâu dài "
                "gây áp lực không cần thiết lên sụn khớp."
            ),
            (
                "Tăng dần số rep trước khi thêm tạ: bắt đầu bằng trọng lượng cơ thể "
                "đến khi làm được 3x20 dễ dàng rồi mới thêm tạ hoặc balo nặng. "
                "Bắp chân chịu tải cả ngày nên cần thời gian thích ứng dần."
            ),
        ],
    },

    # ── SUPERMAN — Thanh niên (bài 16) ───────────────────────────────
    "superman": {
        "id": "superman",
        "ten": "Superman",
        "nhom_tuoi": "Thanh niên",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_superman_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_superman_video.mp4"),

        "tong_quan": (
            "Superman là bài tập nằm sấp, đồng thời nâng tay và chân lên khỏi sàn "
            "giống tư thế bay của siêu anh hùng. Không cần dụng cụ, tập trung "
            "kích hoạt cơ lưng dưới, cơ mông và cơ lưng trên — "
            "nhóm cơ thường bị bỏ quên trong các bài tập thông thường."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Nằm sấp trên sàn, 2 tay duỗi thẳng ra trước đầu, "
                    "2 chân duỗi thẳng ra sau. Trán đặt nhẹ xuống sàn."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Hít vào, sau đó đồng thời nâng 2 tay và 2 chân lên khỏi sàn "
                    "càng cao càng tốt. Siết cơ mông và cơ lưng trong lúc nâng."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Giữ tư thế trên cùng 2–3 giây, nhìn xuống sàn — "
                    "không ngẩng đầu lên để tránh căng cổ."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Hạ tay chân xuống từ từ, thở ra. "
                    "Thực hiện 3 hiệp x 12 reps, nghỉ 45 giây giữa hiệp."
                ),
            },
        ],

        "loi_ich": [
            (
                "Tăng cường cơ lưng dưới và chống đau lưng: cơ erector spinae "
                "được kích hoạt trực tiếp, giúp giảm đau lưng mãn tính do ngồi nhiều "
                "và cải thiện tư thế đứng thẳng trong sinh hoạt hằng ngày."
            ),
            (
                "Cân bằng cơ trước-sau toàn thân: hầu hết bài tập phổ biến "
                "tập cơ phía trước (ngực, bụng, đùi trước). Superman bù đắp "
                "cho phía sau (lưng, mông, đùi sau) — giảm nguy cơ mất cân bằng cơ."
            ),
            (
                "Không tải trọng lên cột sống: khác với deadlift hay good morning, "
                "superman nằm sàn hoàn toàn nên không có lực nén lên đĩa đệm, "
                "an toàn kể cả khi có tiền sử đau lưng nhẹ."
            ),
        ],

        "luu_y": [
            (
                "Không ngẩng đầu lên khi nâng người: cổ phải thẳng với cột sống "
                "trong suốt động tác. Ngẩng đầu cố để nâng cao hơn "
                "gây căng cơ cổ và không tăng thêm hiệu quả bài tập."
            ),
            (
                "Nâng bằng cơ lưng và mông, không phải đà: động tác phải chậm "
                "và có kiểm soát, không dùng quán tính lắc người. "
                "Nâng nhanh bằng đà làm mất tác dụng và dễ căng cơ thắt lưng."
            ),
            (
                "Đặt khăn mềm dưới hông nếu sàn cứng: xương chậu tỳ lên sàn cứng "
                "lâu gây khó chịu và mất tập trung. "
                "Thảm yoga hoặc tấm đệm mỏng là đủ để tập thoải mái."
            ),
        ],
    },

    # ── SIDE LUNGE (bước sang ngang) — Thanh niên (bài 17) ──────────
    "sidelunge": {
        "id": "sidelunge",
        "ten": "Side Lunge (Bước sang ngang)",
        "nhom_tuoi": "Thanh niên",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_sidelunge_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_sidelunge_video.mp4"),

        "tong_quan": (
            "Side Lunge là biến thể bước dài sang ngang, tập nhóm cơ đùi trong và cơ háng "
            "mà lunge thông thường không chạm tới. Không cần dụng cụ, "
            "cải thiện linh hoạt hông và tăng sức mạnh chân theo hướng ngang — "
            "hữu ích cho bóng đá, bóng rổ và cầu lông."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Đứng thẳng, 2 chân rộng bằng hông, tay đặt trước ngực "
                    "hoặc lên hông. Nhìn thẳng phía trước, lưng thẳng."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Bước chân phải rộng sang phải, ngồi xuống phía chân phải — "
                    "đùi phải gần song song sàn, chân trái duỗi thẳng sang trái."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Giữ lưng thẳng, ngực ưỡn nhẹ, gối phải không vượt quá mũi chân. "
                    "Trọng tâm dồn về gót chân phải, giữ 1 giây ở điểm thấp nhất."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Đẩy gót chân phải để đứng lên về tư thế ban đầu, đổi sang bên trái. "
                    "Thực hiện 3 hiệp x 10 reps mỗi bên, nghỉ 60 giây giữa hiệp."
                ),
            },
        ],

        "loi_ich": [
            (
                "Tập cơ đùi trong và cơ háng thường bị bỏ quên: lunge thẳng và squat "
                "hầu như không kích hoạt được nhóm cơ này. Side lunge lấp đầy khoảng trống "
                "đó, giúp chân phát triển cân đối hơn."
            ),
            (
                "Tăng linh hoạt khớp hông theo hướng ngang: nhiều người bị cứng hông "
                "do ngồi nhiều, side lunge kéo giãn cơ háng hiệu quả "
                "và tăng phạm vi chuyển động sang ngang cần thiết trong thể thao."
            ),
            (
                "Cải thiện khả năng di chuyển ngang trong thể thao: đổi hướng nhanh "
                "trong bóng đá, bóng rổ hay cầu lông đều cần sức mạnh đẩy sang ngang — "
                "đúng thứ side lunge rèn luyện."
            ),
        ],

        "luu_y": [
            (
                "Không để gối vượt quá mũi chân: lỗi phổ biến nhất khi mới tập side lunge. "
                "Bước chân ra rộng hơn nếu gối hay vượt quá, "
                "hoặc giảm độ sâu ngồi xuống cho đến khi đủ linh hoạt."
            ),
            (
                "Chân duỗi thẳng hoàn toàn ở bên không chịu lực: bàn chân phẳng xuống sàn, "
                "không nhấc gót. Nếu cơ háng quá cứng không duỗi được, "
                "giảm bước sang cho đến khi cơ dần giãn ra."
            ),
            (
                "Giữ lưng thẳng, không cúi người về phía chân chịu lực: "
                "cúi người ra trước chuyển tải lên lưng thay vì chân. "
                "Nhìn thẳng và giữ ngực ưỡn nhẹ suốt toàn bộ động tác."
            ),
        ],
    },

    # ── HIP THRUST (đẩy hông) — Thanh niên (bài 18) ──────────────────
    # ── HIP THRUST (đẩy hông có tạ) — Thanh niên (bài 18) ───────────
    "hipthrust": {
        "id": "hipthrust",
        "ten": "Hip Thrust (Đẩy hông có tạ)",
        "nhom_tuoi": "Thanh niên",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_hipthrust_thumbnail.png"),
        "video":     _p("assets/fdai-gym-content/video/fdgym_hipthrust_video.mp4"),

        "tong_quan": (
            "Hip Thrust là bài tập đẩy hông với lưng tựa vào mép ghế và tạ đặt lên hông, "
            "tạo kháng lực trực tiếp lên cơ mông. Dụng cụ cần: 1 chiếc ghế thấp chắc chắn "
            "và tạ đĩa hoặc tạ tay 5–20kg đặt lên hông. "
            "Đây là bài tập phát triển cơ mông hiệu quả nhất theo khoa học thể thao hiện đại."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Ngồi trên sàn, lưng tựa vào mép ghế thấp ngang xương bả vai. "
                    "Đặt tạ lên hông, giữ tạ bằng 2 tay. "
                    "Hai chân đặt phẳng trước mặt, rộng bằng vai, gối gập 90 độ."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Siết cơ mông và đẩy hông lên cao chống lại lực nặng của tạ, "
                    "cho đến khi vai, hông, gối tạo thành đường thẳng — "
                    "thân trên song song với sàn."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Giữ ở đỉnh 1–2 giây, siết mông thật chặt. "
                    "Thở ra khi đẩy lên, hít vào khi hạ xuống. "
                    "Mắt nhìn thẳng về trước, không ngẩng cằm lên."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Hạ hông xuống chậm, không chạm sàn hoàn toàn giữa các rep. "
                    "Thực hiện 3 hiệp x 12 reps, nghỉ 60 giây giữa hiệp. "
                    "Tăng cân tạ dần khi đã quen với kỹ thuật."
                ),
            },
        ],

        "loi_ich": [
            (
                "Kích hoạt cơ mông tối đa nhờ kháng lực trực tiếp: tạ đặt lên hông "
                "tạo lực cản ngay tại điểm cơ mông hoạt động mạnh nhất, "
                "hiệu quả hơn hẳn glute bridge bodyweight hay squat có tạ."
            ),
            (
                "Biên độ chuyển động lớn hơn glute bridge nằm sàn: lưng tựa ghế "
                "cho phép hông hạ thấp hơn sàn, tăng tầm kéo giãn cơ mông "
                "và kích thích phát triển cơ sâu hơn mỗi rep."
            ),
            (
                "Cải thiện hiệu suất chạy bộ và thể thao: cơ mông mạnh từ hip thrust "
                "trực tiếp tăng lực đẩy mỗi bước chạy, giúp chạy nhanh hơn "
                "và bền hơn mà không tốn thêm năng lượng."
            ),
        ],

        "luu_y": [
            (
                "Lót khăn hoặc đệm mỏng dưới tạ: tạ đĩa cạnh sắc tỳ trực tiếp "
                "lên xương hông rất đau và để lại vết bầm. "
                "Gấp đôi khăn tập hoặc dùng pad barbell chuyên dụng để bảo vệ."
            ),
            (
                "Ghế phải chắc chắn và sát tường: dùng ghế tựa tường hoặc đặt ghế "
                "sát tường trước khi tập. Ghế trượt khi đẩy hông lên với tạ nặng "
                "rất nguy hiểm và dễ gây chấn thương lưng đột ngột."
            ),
            (
                "Bắt đầu với tạ nhẹ để học kỹ thuật trước: dùng tạ 5kg làm quen "
                "với tư thế và cảm giác cân bằng tạ trên hông. "
                "Tăng cân tạ chỉ khi thực hiện được 3x12 hoàn toàn kiểm soát."
            ),
        ],
    },

    # ── TRICEP DIP (chống tay ghế) — Thanh niên (bài 19) ─────────────
    "tricepdip": {
        "id": "tricepdip",
        "ten": "Tricep Dip (Chống tay ghế)",
        "nhom_tuoi": "Thanh niên",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_tricepdip_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_tricepdip_video.mp4"),

        "tong_quan": (
            "Tricep Dip tập cơ tay sau bằng cách chống tay vào mép ghế phía sau lưng "
            "và hạ người xuống bằng cách gập khuỷu. Chỉ cần 1 chiếc ghế chắc chắn. "
            "Đây là bài tập cơ tay sau hiệu quả nhất không cần tạ, "
            "giúp tay săn chắc và hỗ trợ các bài đẩy khác."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Ngồi trên mép ghế, 2 tay chống vào mép ghế ngay bên hông, "
                    "ngón tay hướng về phía trước. Trượt mông ra khỏi ghế, "
                    "chân duỗi thẳng hoặc gập 90 độ tùy độ khó."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Từ từ hạ người xuống bằng cách gập khuỷu tay ra sau — "
                    "không để khuỷu dang ra ngang. Hạ đến khi cánh tay "
                    "tạo góc 90 độ, không hạ thấp hơn."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Giữ lưng gần sát cạnh ghế trong suốt động tác. "
                    "Hít vào khi hạ xuống, thở ra khi đẩy lên."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Đẩy người lên về tư thế ban đầu bằng cách duỗi khuỷu tay. "
                    "Thực hiện 3 hiệp x 10 reps, nghỉ 60 giây giữa hiệp."
                ),
            },
        ],

        "loi_ich": [
            (
                "Phát triển cơ tay sau toàn diện không cần tạ: tricep dip kích hoạt "
                "cả 3 đầu cơ tay sau đồng thời, hiệu quả hơn nhiều so với "
                "các bài cô lập dùng tạ nhỏ như tricep kickback."
            ),
            (
                "Hỗ trợ trực tiếp cho push-up và các bài đẩy: cơ tay sau là nhóm cơ "
                "phụ quan trọng nhất trong push-up. Tập tricep dip giúp "
                "tăng số rep push-up và cải thiện kỹ thuật rõ rệt."
            ),
            (
                "Chỉ cần 1 chiếc ghế, tập được mọi nơi: ghế văn phòng, ghế ăn "
                "hay bất kỳ bề mặt cao ngang hông nào đều dùng được, "
                "không cần đến gym hay mua dụng cụ."
            ),
        ],

        "luu_y": [
            (
                "Không để vai nhô lên tai khi hạ người: vai nhô lên là dấu hiệu "
                "đang dùng cơ vai thay vì cơ tay sau. Giữ vai thả xuống "
                "và kéo bả vai lại với nhau trong suốt bài."
            ),
            (
                "Không hạ người thấp hơn 90 độ: hạ quá sâu khi mới bắt đầu "
                "tạo áp lực quá lớn lên khớp vai và có thể gây chấn thương. "
                "Tăng độ sâu dần khi cơ tay sau đã đủ mạnh."
            ),
            (
                "Giữ lưng sát cạnh ghế, không để người trôi ra xa: lưng xa ghế "
                "chuyển lực từ cơ tay sang khớp vai. "
                "Tưởng tượng đang trượt dọc theo cạnh ghế khi hạ xuống."
            ),
        ],
    },

    # ── DEAD BUG (bọ chết) — Thanh niên (bài 20) ─────────────────────
    "deadbug": {
        "id": "deadbug",
        "ten": "Dead Bug (Bọ chết)",
        "nhom_tuoi": "Thanh niên",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_deadbug_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_deadbug_video.mp4"),

        "tong_quan": (
            "Dead Bug là bài tập cơ lõi sâu nằm ngửa — hạ tay và chân đối diện "
            "xuống gần sàn rồi đổi bên luân phiên. An toàn cho lưng hơn sit-up "
            "vì không uốn cong cột sống. Tên gọi đến từ tư thế "
            "giống con bọ lật ngửa giơ chân lên trời."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Nằm ngửa, 2 tay duỗi thẳng lên trần, 2 chân nâng lên "
                    "gối gập 90 độ — cẳng chân song song với sàn. "
                    "Lưng dưới ép phẳng xuống sàn, siết bụng."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Từ từ hạ tay phải xuống sau đầu đồng thời duỗi thẳng chân trái "
                    "xuống gần sàn — 2 chi đối diện chuyển động cùng lúc. "
                    "Hít vào trong lúc hạ xuống."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Giữ lưng dưới phẳng với sàn trong suốt động tác — "
                    "đây là điều quan trọng nhất. Nếu lưng bị vổng lên, "
                    "chưa hạ tay chân thấp hơn được."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Đưa tay và chân về vị trí ban đầu, thở ra, đổi sang bên kia. "
                    "Thực hiện 3 hiệp x 10 reps mỗi bên, nghỉ 45 giây giữa hiệp."
                ),
            },
        ],

        "loi_ich": [
            (
                "Tập cơ lõi sâu an toàn tuyệt đối cho lưng: dead bug kích hoạt "
                "transverse abdominis — lớp cơ bụng sâu nhất — "
                "mà không uốn cong cột sống như sit-up, phù hợp cả người đau lưng."
            ),
            (
                "Rèn phối hợp tay-chân đối diện: chuyển động 2 chi đối diện đồng thời "
                "đòi hỏi não bộ điều phối phức tạp, cải thiện khả năng phối hợp vận động "
                "và phản xạ thần kinh cơ toàn thân."
            ),
            (
                "Nền tảng cho mọi bài tập sàn và thể thao: cơ lõi mạnh từ dead bug "
                "giúp ổn định thân trong tất cả các bài khác như squat, deadlift "
                "và mọi động tác thể thao đòi hỏi chuyển hướng nhanh."
            ),
        ],

        "luu_y": [
            (
                "Lưng dưới phải phẳng với sàn trong suốt bài: đây là nguyên tắc số 1. "
                "Nếu lưng bị vổng lên khi hạ tay chân, giảm biên độ xuống "
                "cho đến khi cơ lõi đủ mạnh để kiểm soát hoàn toàn."
            ),
            (
                "Thở đều, không nín thở: nhiều người nín thở để giữ lưng phẳng — "
                "đây là sai lầm. Thở ra khi đưa tay chân về, hít vào khi hạ xuống, "
                "và học cách siết bụng trong khi vẫn thở bình thường."
            ),
            (
                "Bắt đầu chậm để học đúng tư thế: dead bug trông đơn giản "
                "nhưng làm đúng khó hơn nhiều bài tập khác. "
                "Làm chậm từng rep, ưu tiên chất lượng tư thế hơn tốc độ."
            ),
        ],
    },

    # ── ĐẠP XE TĨNH — Thanh niên (bài 21) ───────────────────────────
    "dapxetinh": {
        "id": "dapxetinh",
        "ten": "Đạp xe tĩnh",
        "nhom_tuoi": "Thanh niên",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_dapxetinh_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_dapxetinh_video.mp4"),

        "tong_quan": (
            "Đạp xe tĩnh là bài cardio nhẹ nhàng nhất cho khớp gối so với chạy bộ, "
            "có thể duy trì liên tục 20–30 phút mà không gây đau khớp. "
            "Dụng cụ cần: xe đạp tập tại chỗ (stationary bike) — "
            "có thể thuê tại gym hoặc mua về nhà tập."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Chỉnh yên xe đúng chiều cao: khi đạp đến điểm thấp nhất, "
                    "gối hơi cong nhẹ — không duỗi thẳng hoàn toàn và không gập quá nhiều. "
                    "Tư thế yên đúng là quan trọng nhất."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Ngồi thẳng lưng, tay cầm nhẹ tay cầm — không dựa toàn bộ trọng lượng "
                    "lên tay. Vai thả lỏng, không gồng. "
                    "Đạp bằng cả bàn chân, không chỉ mũi chân."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Bắt đầu với cường độ nhẹ 5 phút đầu để khởi động. "
                    "Sau đó tăng lên mức vừa phải — có thể nói chuyện nhưng hơi thở nhanh hơn bình thường."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Duy trì 20–30 phút ở cường độ vừa, giảm nhẹ 5 phút cuối để hạ nhiệt. "
                    "Tập 3–5 buổi mỗi tuần để thấy kết quả rõ ràng."
                ),
            },
        ],

        "loi_ich": [
            (
                "Cardio nhẹ nhàng nhất cho khớp gối: không có lực tác động khi tiếp đất "
                "như chạy bộ, phù hợp người thừa cân hoặc có vấn đề về khớp gối "
                "muốn tập cardio mà không gây thêm tổn thương."
            ),
            (
                "Đốt calo ổn định trong thời gian dài: 30 phút đạp xe cường độ vừa "
                "đốt khoảng 200–300 calo tùy thể trạng, lý tưởng cho mục tiêu "
                "giảm mỡ bền vững khi kết hợp với chế độ ăn hợp lý."
            ),
            (
                "Cải thiện sức bền tim mạch không gây mệt cơ bắp: đạp xe ít làm đau cơ "
                "hơn so với squat hay lunge, cho phép tập nhiều buổi hơn mỗi tuần "
                "và phục hồi nhanh hơn giữa các buổi tập nặng."
            ),
        ],

        "luu_y": [
            (
                "Chỉnh yên xe đúng chiều cao trước khi đạp: yên quá thấp gây đau đầu gối, "
                "yên quá cao gây đau hông và mất thăng bằng. "
                "Dành 2 phút chỉnh yên đúng cách trước mỗi buổi tập."
            ),
            (
                "Không cúi lưng hoặc dựa toàn thân lên tay cầm: ngồi thẳng và chỉ "
                "đặt tay nhẹ lên tay cầm để giữ thăng bằng. "
                "Dựa nặng lên tay cầm gây đau cổ tay và giảm hiệu quả bài tập."
            ),
            (
                "Uống nước đều đặn trong khi đạp: đạp xe trong phòng kín đổ mồ hôi "
                "nhiều hơn tập ngoài trời do không có gió. "
                "Uống 150–200ml nước mỗi 15 phút để tránh mất nước."
            ),
        ],
    },

    # ── DUMBBELL CURL (cuộn tạ tay) — Thanh niên (bài 22) ────────────
    "dumbbellcurl": {
        "id": "dumbbellcurl",
        "ten": "Dumbbell Curl (Cuộn tạ tay)",
        "nhom_tuoi": "Thanh niên",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_dumbbellcurl_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_dumbbellcurl_video.mp4"),

        "tong_quan": (
            "Dumbbell Curl là bài tập cơ bắp tay trước kinh điển nhất — "
            "cầm tạ 2 tay và cuộn lên ngang vai. Dụng cụ cần: 1 đôi tạ tay 2–5kg. "
            "Đây là bài tập cô lập tốt nhất cho cơ bắp tay trước, "
            "giúp tay trở nên săn chắc và tăng sức mạnh cầm nắm."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Đứng thẳng, cầm tạ 2 tay, lòng bàn tay hướng ra trước. "
                    "Khuỷu tay sát thân, vai thả lỏng, lưng thẳng."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Cuộn tạ lên bằng cách gập khuỷu — chỉ khuỷu tay di chuyển, "
                    "vai và thân không lắc. Cuộn đến khi tạ ngang vai."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Giữ ở đỉnh 1 giây, siết cơ bắp tay trước thật chặt. "
                    "Thở ra khi cuộn lên, hít vào khi hạ xuống."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Hạ tạ xuống chậm rãi trong 2–3 giây về tư thế ban đầu. "
                    "Thực hiện 3 hiệp x 12 reps mỗi tay, nghỉ 60 giây giữa hiệp."
                ),
            },
        ],

        "loi_ich": [
            (
                "Phát triển cơ bắp tay trước hiệu quả và cô lập: dumbbell curl "
                "tập trung hoàn toàn vào bicep mà không phân tán lực sang cơ khác, "
                "giúp cơ bắp tay phát triển nhanh và rõ hơn so với bài tổng hợp."
            ),
            (
                "Tăng sức mạnh cầm nắm và kéo: bicep mạnh hơn cải thiện trực tiếp "
                "khả năng kéo trong pull-up, rowing và mọi động tác kéo về phía cơ thể "
                "trong sinh hoạt hằng ngày."
            ),
            (
                "Dụng cụ rẻ, nhỏ gọn, dùng được cả đời: 1 đôi tạ 2–5kg giá "
                "50–200k tại shop thể thao, không tốn chỗ và không hỏng bao giờ. "
                "Đầu tư một lần dùng hàng chục năm."
            ),
        ],

        "luu_y": [
            (
                "Không lắc thân hoặc dùng đà để cuộn tạ lên: lắc thân là dấu hiệu "
                "tạ quá nặng hoặc đang gian lận. Giảm cân tạ xuống và "
                "thực hiện đúng kỹ thuật — tạ nhẹ đúng tư thế hiệu quả hơn tạ nặng sai."
            ),
            (
                "Không để khuỷu tay di chuyển ra trước hoặc sang ngang: khuỷu phải "
                "cố định sát thân suốt bài. Khuỷu di chuyển làm cơ vai tham gia "
                "thay thế bicep và giảm hiệu quả bài tập."
            ),
            (
                "Hạ tạ chậm quan trọng không kém cuộn lên: phần hạ chậm "
                "(eccentric) kích thích cơ phát triển nhiều hơn phần cuộn lên. "
                "Đếm 2–3 giây khi hạ xuống thay vì thả rơi tạ."
            ),
        ],
    },

    # ── THỞ BỤNG SÂU — Người già — Người già (bài 23) ────────────────
    "thobung": {
        "id": "thobung",
        "ten": "Thở bụng sâu",
        "nhom_tuoi": "Người già",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_thobung_thumbnail.png"),
        "video":     _p("assets/fdai-gym-content/video/fdgym_thobung_video.mp4"),

        "tong_quan": (
            "Thở bụng sâu là bài tập nền tảng dành cho người lớn tuổi — đơn giản, "
            "ngồi tại chỗ, không cần di chuyển. Chỉ 10 nhịp thở đúng cách mỗi ngày "
            "giúp ổn định huyết áp, giảm căng thẳng và chuẩn bị cơ thể sẵn sàng "
            "cho các bài vận động tiếp theo một cách an toàn nhất."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Ngồi thẳng lưng trên ghế, hai bàn chân đặt phẳng xuống sàn, "
                    "hai tay đặt nhẹ lên bụng để cảm nhận chuyển động."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Hít vào chậm bằng mũi trong 4 giây — cảm nhận bụng phình ra "
                    "đẩy nhẹ vào lòng bàn tay, ngực ít di chuyển."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Giữ hơi nhẹ trong 2 giây, không nín cứng — chỉ dừng tự nhiên, "
                    "vai và cổ hoàn toàn thả lỏng."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Thở ra chậm bằng miệng trong 6 giây, để bụng xẹp dần vào. "
                    "Lặp lại 10 lần. Thực hiện mỗi sáng trước khi rời khỏi giường."
                ),
            },
        ],

        "loi_ich": [
            (
                "Ổn định huyết áp tự nhiên mỗi ngày: nhịp thở chậm và sâu kích hoạt "
                "hệ thần kinh phó giao cảm, giúp hạ nhịp tim và huyết áp mà không cần thuốc."
            ),
            (
                "Giảm lo âu và căng thẳng hiệu quả: chỉ 5 phút thở bụng đã đủ để hạ "
                "nồng độ cortisol — hormone stress — giúp tinh thần bình tĩnh và ngủ sâu hơn."
            ),
            (
                "Tăng cường dung tích phổi theo tuổi tác: luyện thở sâu đều đặn giúp cơ hoành "
                "linh hoạt hơn, cải thiện lượng oxy vào máu và giảm cảm giác khó thở khi gắng sức."
            ),
        ],

        "luu_y": [
            (
                "Không nín thở cứng trong bước giữ hơi: chỉ dừng tự nhiên, không siết cổ họng. "
                "Nín cứng dễ làm tăng áp lực trong lồng ngực, không tốt cho người huyết áp cao."
            ),
            (
                "Ngồi trên ghế có tựa lưng, không ngồi mép ghế: lưng được đỡ đúng cách "
                "giúp cơ hoành hoạt động tự do, tránh căng cơ lưng khi tập kéo dài."
            ),
            (
                "Nếu thấy chóng mặt, dừng ngay và thở bình thường: cảm giác hơi lâng lâng "
                "nhẹ ban đầu là bình thường, nhưng nếu chóng mặt rõ thì đang thở quá nhanh — "
                "cần làm chậm lại nhịp thở."
            ),
        ],
    },

    # ── XOAY CỔ TAY VÀ MẮT CÁ CHÂN — Người già (bài 24) ────────────
    "xoaykhop": {
        "id": "xoaykhop",
        "ten": "Xoay cổ tay và mắt cá chân",
        "nhom_tuoi": "Người già",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_xoaykhop_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_xoaykhop_video.mp4"),
        # Video tham khảo: https://www.youtube.com/watch?v=n_MCNEwdT_k

        "tong_quan": (
            "Xoay cổ tay và mắt cá chân là bài tập ngồi ghế đơn giản nhất, "
            "không cần di chuyển, không cần sức. Chỉ cần xoay vòng tròn nhẹ nhàng "
            "giúp khớp nhỏ được bôi trơn, giảm tê bì tay chân và tăng lưu thông máu "
            "— đặc biệt tốt cho người ngồi nhiều cả ngày."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Ngồi thẳng lưng trên ghế, 2 chân đặt phẳng xuống sàn. "
                    "Đưa 2 tay ra trước, cổ tay thả lỏng hoàn toàn."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Xoay 2 cổ tay cùng lúc theo chiều kim đồng hồ 10 vòng chậm rãi, "
                    "sau đó đổi chiều ngược kim đồng hồ 10 vòng. Giữ vai thả lỏng."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Nhấc 1 chân lên nhẹ, xoay mắt cá chân 10 vòng theo chiều kim đồng hồ "
                    "rồi đổi chiều 10 vòng. Hạ chân xuống và đổi sang chân kia."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Thực hiện 2–3 lượt toàn bộ chuỗi động tác. "
                    "Tổng thời gian khoảng 5 phút — có thể làm ngay khi ngồi xem TV hoặc đọc sách."
                ),
            },
        ],

        "loi_ich": [
            (
                "Giảm tê bì và cứng khớp tay chân: xoay khớp đều đặn kích thích dịch khớp "
                "bôi trơn bề mặt, giảm cảm giác tê và cứng đặc biệt vào buổi sáng "
                "hoặc sau khi ngồi lâu không vận động."
            ),
            (
                "Cải thiện lưu thông máu đến bàn tay và bàn chân: người lớn tuổi thường "
                "bị lạnh tay chân do tuần hoàn kém. Xoay cổ tay và mắt cá mỗi ngày "
                "giúp máu lưu thông tốt hơn đến các chi xa tim."
            ),
            (
                "Duy trì linh hoạt khớp nhỏ — phòng ngừa thoái hóa: các khớp nhỏ "
                "như cổ tay và mắt cá dễ bị thoái hóa nếu không vận động. "
                "Chỉ 5 phút xoay nhẹ mỗi ngày là đủ để duy trì phạm vi chuyển động."
            ),
        ],

        "luu_y": [
            (
                "Xoay chậm và nhẹ nhàng — không xoay mạnh hay giật cục: mục tiêu là "
                "làm nóng và bôi trơn khớp, không phải kiểm tra độ linh hoạt. "
                "Xoay quá mạnh khi khớp chưa ấm dễ gây căng dây chằng nhỏ."
            ),
            (
                "Dừng nếu nghe tiếng kêu lạo xạo kèm đau: tiếng khớp kêu nhẹ "
                "khi xoay là bình thường với người lớn tuổi. Nhưng nếu kèm đau nhức "
                "hoặc sưng thì cần ngừng và hỏi ý kiến bác sĩ trước khi tiếp tục."
            ),
            (
                "Có thể làm nhiều lần trong ngày, không cần chờ 'giờ tập': "
                "đây là bài tập có thể làm lúc xem TV, ngồi chờ hay đọc sách. "
                "Làm 2–3 lần mỗi ngày hiệu quả hơn 1 lần dài."
            ),
        ],
    },

    # ── CHAIR CAT-COW — Người già (bài 25) ───────────────────────────
    "chaircatcow": {
        "id": "chaircatcow",
        "ten": "Chair Cat-Cow (Co giãn cột sống)",
        "nhom_tuoi": "Người già",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_chaircatcow_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_chaircatcow_video.mp4"),
        # Video tham khảo: https://www.youtube.com/watch?v=PMxA3xlFpAk

        "tong_quan": (
            "Chair Cat-Cow là bài co giãn cột sống ngồi trên ghế — "
            "hít vào ưỡn ngực ra, thở ra khom lưng tròn, tất cả đều thực hiện "
            "trong tư thế ngồi thẳng, không xuống sàn, không cần dụng cụ. "
            "Chỉ 5 phút mỗi ngày giúp cột sống linh hoạt, giảm đau lưng mãn tính."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Ngồi thẳng trên ghế, 2 chân đặt phẳng xuống sàn rộng bằng hông. "
                    "Đặt 2 tay lên đùi, ngồi hơi ra phần giữa ghế — không tựa lưng vào ghế."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Hít vào chậm: ưỡn ngực ra trước, vai kéo ra sau, "
                    "lưng dưới hơi cong về trước — tư thế 'bò ngồi'. Giữ 2 giây."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Thở ra chậm: khom lưng tròn ra sau, cúi đầu nhẹ xuống, "
                    "cảm nhận toàn bộ cột sống từ thắt lưng đến cổ giãn ra — tư thế 'mèo ngồi'. Giữ 2 giây."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Luân phiên nhịp nhàng 2 tư thế theo hơi thở, không nghỉ giữa. "
                    "Thực hiện 10 lần rồi nghỉ, lặp 2–3 lượt. Tổng thời gian 5 phút."
                ),
            },
        ],

        "loi_ich": [
            (
                "Giảm đau lưng mãn tính hiệu quả và an toàn: chuyển động nhẹ nhàng "
                "của cột sống kích thích dịch đĩa đệm lưu thông, giảm áp lực lên "
                "các đốt sống và dây thần kinh — nguyên nhân chính của đau lưng mãn tính."
            ),
            (
                "Cải thiện tư thế ngồi sau vài tuần tập: cơ dựng cột sống và cơ bụng "
                "được kích hoạt nhẹ trong cả 2 tư thế, dần dần giúp cơ thể "
                "tự duy trì tư thế thẳng mà không cần cố gắng."
            ),
            (
                "Thư giãn hệ thần kinh và giảm căng thẳng: kết hợp hơi thở sâu với "
                "chuyển động nhịp nhàng kích hoạt phản ứng thư giãn của cơ thể, "
                "giảm cortisol và cải thiện giấc ngủ khi tập vào buổi tối."
            ),
        ],

        "luu_y": [
            (
                "Không ưỡn hoặc khom quá mức: biên độ vừa phải là đủ — "
                "không cần ưỡn ngực thật sâu hay khom lưng thật tròn. "
                "Người có thoát vị đĩa đệm nên hỏi bác sĩ trước khi tập."
            ),
            (
                "Ghế phải có 4 chân chắc chắn, không dùng ghế có bánh xe: "
                "ghế có bánh xe dễ trượt khi cơ thể nghiêng về trước hoặc sau. "
                "Đặt ghế sát tường nếu muốn thêm an toàn."
            ),
            (
                "Thở đúng theo chuyển động — không nín thở: hít vào khi ưỡn ngực, "
                "thở ra khi khom lưng. Thở đúng là phần quan trọng nhất của bài, "
                "tạo ra tác dụng thư giãn và giảm đau thực sự."
            ),
        ],
    },

    # ── WALL PUSH-UP — Người già (bài 26) ────────────────────────────
    "wallpushup": {
        "id": "wallpushup",
        "ten": "Wall Push-Up (Chống đẩy vào tường)",
        "nhom_tuoi": "Người già",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_wallpushup_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_wallpushup_video.mp4"),
        # Video tham khảo: https://www.youtube.com/watch?v=PkFu8ee6IuY

        "tong_quan": (
            "Wall Push-Up là bài chống đẩy đứng thẳng vào tường — an toàn nhất "
            "trong tất cả các biến thể push-up vì không tải trọng lên khớp cổ tay "
            "và vai như push-up sàn. Chỉ cần 1 bức tường, "
            "tập được ngay trong nhà bếp hoặc phòng khách."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Đứng cách tường khoảng 1 bước chân, đặt 2 tay lên tường "
                    "ngang vai, rộng bằng vai. Ngón tay hướng lên, lưng thẳng."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Từ từ gập khuỷu tay, để người nghiêng vào tường. "
                    "Giữ toàn thân thẳng — không để hông nhô ra sau hay cúi lưng."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Hạ đến khi mũi gần chạm tường hoặc đến điểm thoải mái. "
                    "Hít vào khi hạ xuống, giữ 1 giây."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Đẩy người trở về tư thế ban đầu, thở ra khi đẩy. "
                    "Thực hiện 2 hiệp x 8–10 reps, nghỉ 45 giây giữa hiệp."
                ),
            },
        ],

        "loi_ich": [
            (
                "Tăng sức mạnh thân trên an toàn tuyệt đối cho người lớn tuổi: "
                "tường chịu phần lớn trọng lượng cơ thể, khớp vai và cổ tay "
                "không bị tải nặng — phù hợp kể cả người có vấn đề về xương khớp."
            ),
            (
                "Cải thiện khả năng tự chăm sóc hằng ngày: sức mạnh đẩy từ wall push-up "
                "giúp đứng dậy khỏi ghế, mở cửa nặng và giữ thăng bằng khi vươn tay "
                "lên cao lấy đồ — những việc quan trọng để sống độc lập."
            ),
            (
                "Xây dựng nền tảng sức mạnh để tiến lên push-up khó hơn: "
                "wall push-up là bước đầu tiên của hành trình push-up. "
                "Khi làm được 3x10 dễ dàng, có thể chuyển sang chống đẩy bàn hoặc ghế."
            ),
        ],

        "luu_y": [
            (
                "Chân không trượt — đứng trên nền có ma sát tốt: sàn gạch trơn "
                "rất nguy hiểm khi nghiêng người vào tường. "
                "Đi dép có đế cao su hoặc đứng trên thảm trước khi tập."
            ),
            (
                "Không để hông nhô ra sau: toàn thân phải thẳng từ đầu đến gót "
                "như một tấm ván. Hông nhô ra sau làm mất tác dụng bài tập "
                "và tạo áp lực sai lên lưng dưới."
            ),
            (
                "Bắt đầu đứng gần tường, tăng khoảng cách dần: đứng gần tường "
                "thì bài dễ hơn, đứng xa hơn thì khó hơn. "
                "Mới bắt đầu đứng cách 30–40cm, tăng dần khi đã quen."
            ),
        ],
    },

    # ── ĐỨNG MỘT CHÂN TỰA TƯỜNG — Người già (bài 27) ─────────────────
    "thangbang": {
        "id": "thangbang",
        "ten": "Đứng một chân tựa tường",
        "nhom_tuoi": "Người già",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_thangbang_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_thangbang_video.mp4"),
        # Video tham khảo: https://www.youtube.com/watch?v=CSbUet53L68

        "tong_quan": (
            "Đứng một chân tựa tường là bài luyện thăng bằng quan trọng nhất "
            "cho người trên 53 tuổi. Chỉ cần 1 bức tường để tựa tay, "
            "nhấc 1 chân lên vài cm và giữ thăng bằng. "
            "Tập đều đặn giảm đáng kể nguy cơ té ngã — nguyên nhân hàng đầu "
            "gây chấn thương nghiêm trọng ở người cao tuổi Việt Nam."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Đứng thẳng, tựa nhẹ 1 hoặc 2 ngón tay vào tường — "
                    "không bám chặt, chỉ chạm nhẹ để có điểm tựa khi mất thăng bằng."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Từ từ nhấc chân phải lên khỏi sàn vài cm. "
                    "Nhìn thẳng vào 1 điểm cố định trên tường phía trước để giữ thăng bằng."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Giữ tư thế 5–10 giây, thở đều. Không nín thở. "
                    "Chân trụ hơi chùng gối tự nhiên — không khóa gối cứng."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Hạ chân xuống nhẹ nhàng, nghỉ 5 giây rồi đổi chân. "
                    "Thực hiện 5 lần mỗi chân. Tăng dần thời gian giữ khi đã quen."
                ),
            },
        ],

        "loi_ich": [
            (
                "Giảm nguy cơ té ngã — vấn đề số 1 với người 53+: "
                "thăng bằng kém là nguyên nhân chính gây té ngã ở người cao tuổi. "
                "Tập đứng 1 chân đều đặn củng cố cơ ổn định hông và mắt cá, "
                "giúp cơ thể phản ứng nhanh hơn khi bị vấp."
            ),
            (
                "Tăng sức mạnh cơ chân trụ và cơ hông: đứng 1 chân buộc "
                "cơ mông và cơ hông phía chân trụ làm việc liên tục để ổn định, "
                "phát triển sức mạnh mà không cần tạ hay máy móc."
            ),
            (
                "Cải thiện các hoạt động hằng ngày: leo cầu thang, bước qua ngưỡng cửa, "
                "đi bộ trên nền không bằng phẳng đều đòi hỏi thăng bằng tốt. "
                "Bài tập này giúp duy trì sự tự tin và độc lập trong sinh hoạt."
            ),
        ],

        "luu_y": [
            (
                "Luôn tập gần tường hoặc ghế chắc chắn: không bao giờ tập đứng 1 chân "
                "ở giữa phòng trống. Tường hoặc lưng ghế phải trong tầm với tay "
                "để bám vào ngay khi có dấu hiệu mất thăng bằng."
            ),
            (
                "Bắt đầu từ 5 giây — không cố giữ lâu ngay từ đầu: người mới "
                "5 giây là đủ thách thức. Tăng dần 2–3 giây mỗi tuần. "
                "Cố giữ quá lâu khi chưa đủ sức dễ bị ngã."
            ),
            (
                "Không nhìn xuống chân khi đứng: nhìn xuống làm mất điểm tham chiếu "
                "thị giác và tăng nguy cơ mất thăng bằng. "
                "Nhìn thẳng vào 1 điểm cố định ngang tầm mắt là kỹ thuật đúng."
            ),
        ],
    },

    # ── GIẬM CHÂN TẠI CHỖ TRÊN GHẾ — Người già (bài 28) ────────────
    "giamchan": {
        "id": "giamchan",
        "ten": "Giậm chân tại chỗ trên ghế",
        "nhom_tuoi": "Người già",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_giamchan_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_giamchan_video.mp4"),
        # Video tham khảo: https://www.youtube.com/watch?v=1PvAcyKfK-M

        "tong_quan": (
            "Giậm chân tại chỗ trên ghế là bài cardio ngồi đơn giản nhất — "
            "nâng chân trái phải luân phiên như đang đi bộ mà không cần đứng dậy. "
            "Chỉ 2 phút mỗi ngày đủ để kích thích tuần hoàn máu chân, "
            "giảm tê bì và phù chân sau khi ngồi lâu."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Ngồi thẳng trên ghế, lưng không tựa vào ghế, "
                    "2 chân đặt phẳng xuống sàn rộng bằng hông. "
                    "Tay đặt nhẹ lên đùi hoặc tựa vào thành ghế."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Nâng đầu gối phải lên cao ngang hông rồi hạ xuống, "
                    "ngay lập tức nâng gối trái lên — luân phiên đều đặn "
                    "như đang đi bộ tại chỗ trong tư thế ngồi."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Giữ nhịp vừa phải, không cần nhanh. "
                    "Thở đều trong suốt bài — hít vào khi 1 chân lên, "
                    "thở ra khi chân đó hạ xuống."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Thực hiện liên tục 2 phút. Có thể làm ngay khi ngồi xem TV, "
                    "đọc sách hoặc sau bữa ăn 30 phút để giúp tiêu hóa và tuần hoàn."
                ),
            },
        ],

        "loi_ich": [
            (
                "Kích thích tuần hoàn máu chân ngay lập tức: cơ đùi và cơ bắp chân "
                "co bóp liên tục đẩy máu từ tĩnh mạch chân lên tim, "
                "giảm cảm giác nặng chân và phù nhẹ sau khi ngồi lâu."
            ),
            (
                "Tăng cường cơ hông gấp và cơ đùi: động tác nâng gối liên tục "
                "kích hoạt nhóm cơ hông trước — nhóm cơ quan trọng cho việc "
                "đứng dậy, leo cầu thang và đi bộ ổn định."
            ),
            (
                "Phù hợp tập mọi lúc không cần thay đồ hay dọn chỗ: "
                "bài này làm được ngay trên ghế sofa, ghế ăn hay ghế văn phòng. "
                "Không cần giày thể thao, không cần không gian rộng."
            ),
        ],

        "luu_y": [
            (
                "Không tựa lưng vào ghế khi tập: ngồi thẳng và tự giữ lưng "
                "giúp cơ bụng và cơ lưng cùng tham gia, tăng hiệu quả bài tập. "
                "Chỉ tựa lưng nếu cảm thấy mệt hoặc đau lưng."
            ),
            (
                "Dừng nếu cảm thấy khó thở hoặc tim đập mạnh bất thường: "
                "dù là bài nhẹ, người có bệnh tim mạch nên bắt đầu từ 1 phút "
                "và tăng dần. Hỏi ý kiến bác sĩ nếu có tiền sử tim mạch."
            ),
            (
                "Ghế phải chắc chắn, không dùng ghế có bánh xe: "
                "ghế có bánh xe có thể trượt khi nâng chân mạnh. "
                "Đặt ghế sát tường để thêm an toàn khi mới bắt đầu tập."
            ),
        ],
    },

    # ── KIỄNG GÓT MỘT CHÂN TỰA TƯỜNG — Người già (bài 29) ─────────
    "kienggot": {
        "id": "kienggot",
        "ten": "Kiễng gót một chân tựa tường",
        "nhom_tuoi": "Người già",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_kienggot_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_kienggot_video.mp4"),
        # Video tham khảo: https://www.youtube.com/watch?v=Aownr2GWLbA

        "tong_quan": (
            "Kiễng gót một chân tựa tường là phiên bản nâng cao của kiễng gót thông thường — "
            "đứng trên 1 chân, tay tựa nhẹ vào tường để giữ thăng bằng. "
            "Tăng gấp đôi cường độ cho cơ bắp chân so với 2 chân, "
            "phù hợp người già còn khỏe và muốn bắp chân mạnh hơn thực sự."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Đứng cách tường 20–30cm, đặt 2 tay nhẹ lên tường ngang vai. "
                    "Dồn trọng lượng sang chân phải, nhấc chân trái lên khỏi sàn nhẹ nhàng."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Từ từ kiễng gót chân phải lên cao nhất có thể, "
                    "đứng trên đầu ngón chân phải. Giữ 2 giây ở điểm cao nhất."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Hạ gót xuống chậm rãi trong 2–3 giây — không thả rơi. "
                    "Thực hiện 10 reps rồi đổi sang chân trái. "
                    "Thở ra khi kiễng lên, hít vào khi hạ xuống."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Thực hiện 2 hiệp x 10 reps mỗi chân, nghỉ 45 giây giữa hiệp. "
                    "Nếu chưa đủ sức 1 chân, bắt đầu bằng 2 chân rồi chuyển dần."
                ),
            },
        ],

        "loi_ich": [
            (
                "Tăng sức mạnh bắp chân gấp đôi so với kiễng 2 chân: "
                "toàn bộ trọng lượng cơ thể dồn vào 1 chân buộc cơ bắp chân "
                "làm việc tối đa, phát triển cơ nhanh hơn và hiệu quả hơn."
            ),
            (
                "Cải thiện thăng bằng trên từng chân riêng lẻ: đứng 1 chân "
                "trong khi kiễng gót đòi hỏi cơ mắt cá và cơ bắp chân phối hợp "
                "để giữ ổn định — rèn thăng bằng thực tế hơn bài 2 chân."
            ),
            (
                "Giảm phù chân và tăng tuần hoàn hiệu quả hơn: cơ bắp chân "
                "co mạnh hơn khi chịu tải 1 chân, bơm máu từ tĩnh mạch chân "
                "lên tim tốt hơn, giảm phù nhanh hơn sau khi ngồi lâu."
            ),
        ],

        "luu_y": [
            (
                "CHỈ tập khi đã quen bài kiễng 2 chân: đây là bài nâng cao, "
                "không dành cho người mới hoàn toàn. Tập kiễng 2 chân ít nhất "
                "2 tuần trước khi chuyển sang 1 chân."
            ),
            (
                "Tay phải tựa chắc vào tường trong suốt bài: không cố thả tay "
                "để thách thức thêm — mục tiêu là rèn bắp chân, không phải thăng bằng. "
                "Té ngã khi kiễng gót 1 chân rất nguy hiểm với người lớn tuổi."
            ),
            (
                "Đứng trên nền phẳng, không trơn — bắt buộc: "
                "sàn trơn khi đứng 1 chân kiễng gót cực kỳ nguy hiểm. "
                "Mang giày thể thao đế cao su hoặc đứng trên thảm tập."
            ),
        ],
    },

    # ── VƯƠN TAY SANG NGANG TRÊN GHẾ — Người già (bài 30) ────────────
    "vuontay": {
        "id": "vuontay",
        "ten": "Vươn tay sang ngang trên ghế",
        "nhom_tuoi": "Người già",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_vuontay_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_vuontay_video.mp4"),
        # Video tham khảo: https://www.youtube.com/watch?v=s_L-Jgy51Uk

        "tong_quan": (
            "Vươn tay sang ngang trên ghế là bài tập vai và cổ đơn giản — "
            "ngồi thẳng, từ từ đưa 2 tay ra ngang ngang vai rồi hạ xuống. "
            "Không cần dụng cụ, không cần đứng dậy. "
            "Tập đều đặn giảm cứng vai, đau cổ gáy "
            "và cải thiện tư thế ngồi cho người lớn tuổi."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Ngồi thẳng lưng trên ghế, không tựa lưng vào ghế. "
                    "2 chân đặt phẳng xuống sàn, 2 tay thả dọc theo thân."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Từ từ đưa 2 tay ra 2 bên cho đến khi ngang vai — "
                    "lòng bàn tay hướng xuống sàn. "
                    "Hít vào trong lúc đưa tay ra."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Giữ tư thế 3 giây. Vai không nhô lên tai — "
                    "giữ vai thả xuống tự nhiên trong suốt bài. "
                    "Nhìn thẳng phía trước, cổ thả lỏng."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Hạ tay xuống chậm rãi, thở ra. "
                    "Thực hiện 2 hiệp x 10 reps, nghỉ 30 giây giữa hiệp."
                ),
            },
        ],

        "loi_ich": [
            (
                "Giảm cứng vai và đau cổ gáy mãn tính: cơ thang và cơ delta "
                "được kéo giãn và tăng cường đồng thời, giảm căng thẳng tích tụ "
                "ở vùng vai cổ sau nhiều giờ ngồi không vận động."
            ),
            (
                "Tăng linh hoạt khớp vai cho sinh hoạt hằng ngày: "
                "khớp vai linh hoạt giúp với tay lên kệ cao, mặc áo, "
                "tắm rửa dễ dàng hơn — những việc quan trọng để sống tự lập."
            ),
            (
                "Cải thiện tư thế và chống gù lưng: cơ vai sau và cơ lưng trên "
                "được kích hoạt kéo vai ra sau tự nhiên, "
                "chống lại xu hướng khom người ra trước thường gặp ở người cao tuổi."
            ),
        ],

        "luu_y": [
            (
                "Không nâng tay cao hơn vai nếu khớp vai đang đau: "
                "ngang vai là biên độ an toàn nhất. "
                "Nếu có viêm gân hay thoái hóa khớp vai, chỉ nâng đến mức thoải mái."
            ),
            (
                "Không nhún vai lên khi nâng tay: đây là lỗi phổ biến nhất. "
                "Nhún vai làm căng cơ cổ thay vì tập cơ vai. "
                "Nếu khó giữ vai thả xuống, bắt đầu bằng nâng 1 tay trước."
            ),
            (
                "Chuyển động chậm và kiểm soát — không giật tay: "
                "đưa tay ra trong 2 giây, giữ 3 giây, hạ xuống 2 giây. "
                "Chuyển động chậm kích hoạt cơ tốt hơn và an toàn hơn cho khớp."
            ),
        ],
    },

    # ── XOAY VAI TRÊN GHẾ — Người già (bài 31) ──────────────────────
    "xoaivai": {
        "id": "xoaivai",
        "ten": "Xoay vai trên ghế",
        "nhom_tuoi": "Người già",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_xoaivai_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_xoaivai_video.mp4"),
        # Video tham khảo: https://www.youtube.com/watch?v=lf4D3U3QUYw

        "tong_quan": (
            "Xoay vai trên ghế là bài giãn vai và cổ gáy đơn giản nhất — "
            "ngồi thẳng và xoay 2 vai ra sau rồi ra trước thành vòng tròn. "
            "Không cần dụng cụ, không cần đứng dậy. "
            "Chỉ 3 phút giải phóng căng thẳng tích tụ ở vai và cổ "
            "sau nhiều giờ ngồi không vận động."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Ngồi thẳng lưng trên ghế, 2 tay thả lỏng dọc theo thân. "
                    "Hít thở sâu 2–3 lần, thả lỏng hoàn toàn trước khi bắt đầu."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Xoay 2 vai ra sau thành vòng tròn lớn — lên, ra sau, xuống, ra trước. "
                    "Thực hiện 10 vòng chậm rãi, cảm nhận cơ vai và cơ thang giãn ra."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Đổi chiều: xoay 2 vai ra trước thành vòng tròn — "
                    "lên, ra trước, xuống, ra sau. Thực hiện 10 vòng."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Lặp lại 2–3 lượt mỗi chiều. Tổng thời gian 3–4 phút. "
                    "Có thể làm nhiều lần trong ngày khi vai bắt đầu cứng hoặc mỏi."
                ),
            },
        ],

        "loi_ich": [
            (
                "Giảm cứng vai và đau cổ gáy nhanh chóng: xoay vai kích thích "
                "dịch khớp vai bôi trơn và kéo giãn cơ thang — nhóm cơ chịu trách nhiệm "
                "chính cho cảm giác cứng cổ và đau đầu phía sau ở người lớn tuổi."
            ),
            (
                "Cải thiện tư thế và chống gù lưng: xoay vai ra sau "
                "kéo bả vai lại với nhau, mở rộng lồng ngực và tự nhiên "
                "giúp cột sống thẳng hơn — chống lại xu hướng khom người ra trước."
            ),
            (
                "Thư giãn tức thì, làm được mọi lúc mọi nơi: "
                "xoay vai không gây tiếng động, không cần thay đồ, "
                "làm được ngay trên ghế làm việc, ghế ăn hay ghế sofa."
            ),
        ],

        "luu_y": [
            (
                "Xoay vòng tròn lớn và chậm — không xoay nhỏ và nhanh: "
                "vòng xoay lớn kéo giãn toàn bộ nhóm cơ vai. "
                "Xoay nhỏ nhanh chỉ tạo cảm giác mà không có tác dụng thực sự."
            ),
            (
                "Thở đều trong suốt bài — không nín thở: "
                "hít vào khi vai lên cao, thở ra khi vai hạ xuống. "
                "Kết hợp hơi thở giúp cơ giãn sâu hơn và thư giãn tốt hơn."
            ),
            (
                "Dừng nếu nghe tiếng lạo xạo kèm đau: tiếng khớp vai kêu nhẹ "
                "khi xoay là bình thường. Nhưng nếu kèm đau nhói hoặc "
                "giới hạn chuyển động thì cần gặp bác sĩ trước khi tiếp tục."
            ),
        ],
    },

    # ── THÁI CỰC QUYỀN 8 THỨC CƠ BẢN — Người già (bài 32) ──────────
    "thaicucquyen8thuc": {
        "id": "thaicucquyen8thuc",
        "ten": "Thái Cực Quyền 8 thức cơ bản",
        "nhom_tuoi": "Người già",
        "thumbnail": _p("assets/fdai-gym-content/thumbnail/fdgym_thaicucquyen8thuc_thumbnail.png"),
        "video": _p("assets/fdai-gym-content/video/fdgym_thaicucquyen8thuc_video.mp4"),
        # Video tham khảo: https://www.youtube.com/watch?v=TG1gNfLbHuk (VA Long Beach Medical Center)
        # Timeline: Form 1 (02:27) → Form 2 (03:48) → Form 3 (06:02) → Form 4 (08:29)
        #           Form 5 (11:59) → Form 6 (14:04) → Form 7 (16:11) → Form 8 (18:14)

        "tong_quan": (
            "Thái Cực Quyền 8 thức là phiên bản rút gọn của bài quyền truyền thống châu Á, "
            "được hàng triệu người cao tuổi tập mỗi sáng trong công viên trên khắp Việt Nam, "
            "Trung Quốc và các nước châu Á. 8 thức gồm: Ôm bóng, Rẽ bờm ngựa hoang, "
            "Roi đơn, Vẫy tay như mây, Đẩy khỉ lùi, Quét gối, Thoi thợ dệt và Nắm đuôi chim công — "
            "tất cả đều chuyển động chậm rãi, nhịp nhàng như sóng nước, không bật nhảy, "
            "không cần dụng cụ. Bài tập đã được y khoa hiện đại xác nhận giúp cải thiện "
            "thăng bằng, tuần hoàn và sức khỏe tinh thần rõ rệt chỉ sau vài tuần tập đều đặn."
        ),

        "cac_buoc": [
            {
                "so": 1,
                "noi_dung": (
                    "Khởi động — đứng thẳng, 2 chân rộng bằng vai, đầu gối hơi chùng nhẹ. "
                    "Hai tay thả dọc thân, vai thả xuống tự nhiên. "
                    "Hít thở sâu 3 lần, thả lỏng toàn thân, mắt nhìn thẳng phía trước. "
                    "Đây là tư thế chuẩn bị — giữ 30 giây trước khi vào thức đầu tiên."
                ),
            },
            {
                "so": 2,
                "noi_dung": (
                    "Thức 1–2 (Ôm bóng & Rẽ bờm ngựa hoang): 2 tay đưa ra trước "
                    "tạo hình tròn như đang ôm bóng lớn, sau đó tay trái đẩy ra trước "
                    "và tay phải kéo về sau — chuyển trọng tâm nhẹ sang chân trước. "
                    "Đây là 2 thức nền tảng, học kỹ trước khi tiếp tục."
                ),
            },
            {
                "so": 3,
                "noi_dung": (
                    "Thức 3–4 (Roi đơn & Vẫy tay như mây): tay phải đưa ra ngang "
                    "như cầm roi, tay trái giữ trước ngực — sau đó 2 tay vẽ vòng tròn "
                    "ngang người từ trái sang phải nhịp nhàng như đám mây trôi. "
                    "Thở đều theo nhịp vẫy tay, không nín thở."
                ),
            },
            {
                "so": 4,
                "noi_dung": (
                    "Thức 5–6 (Đẩy khỉ lùi & Quét gối): bước chân ra sau chậm rãi "
                    "đồng thời tay đẩy về trước — lặp lại luân phiên 3–4 lần mỗi bên. "
                    "Sau đó tay đưa qua gối như quét nhẹ, trọng tâm chuyển sang chân trước. "
                    "Giữ lưng thẳng trong suốt cả 2 thức này."
                ),
            },
            {
                "so": 5,
                "noi_dung": (
                    "Thức 7–8 (Thoi thợ dệt & Nắm đuôi chim công): tay đẩy chéo "
                    "lên cao và sang ngang như người dệt vải — đổi bên nhịp nhàng. "
                    "Kết thúc bằng cả 2 tay đưa ra trước, nắm nhẹ rồi kéo về hông "
                    "như đang nắm đuôi chim công. Thở ra dài khi kết thúc thức cuối."
                ),
            },
            {
                "so": 6,
                "noi_dung": (
                    "Kết thúc — đưa 2 tay từ từ hạ xuống dọc thân, "
                    "đứng yên 30 giây, hít thở sâu 3 lần để cơ thể hạ nhiệt. "
                    "Tập 1–2 lượt mỗi buổi, tổng khoảng 8–10 phút. "
                    "Mới bắt đầu chỉ học thức 1–2 trước, tăng dần mỗi tuần thêm 1 thức."
                ),
            },
        ],

        "loi_ich": [
            (
                "Cải thiện thăng bằng và giảm nguy cơ té ngã rõ rệt: "
                "nhiều nghiên cứu y khoa xác nhận tập Thái Cực Quyền đều đặn 8–12 tuần "
                "giảm tỷ lệ té ngã ở người cao tuổi xuống 43–47%, hiệu quả hơn "
                "hầu hết các bài tập thông thường khác."
            ),
            (
                "Tốt cho tim mạch và tuần hoàn mà không gây mệt tim: "
                "chuyển động chậm liên tục kích thích tuần hoàn máu nhẹ nhàng, "
                "phù hợp người có huyết áp cao hoặc tim mạch yếu "
                "vì không tạo ra tăng nhịp tim đột ngột như các bài cardio thông thường."
            ),
            (
                "Giảm căng thẳng, đau khớp và cải thiện giấc ngủ: "
                "kết hợp chuyển động nhịp nhàng với hít thở sâu kích hoạt "
                "hệ thần kinh phó giao cảm, giảm cortisol, giảm viêm khớp nhẹ "
                "và giúp ngủ sâu hơn — đặc biệt khi tập vào buổi sáng sớm."
            ),
        ],

        "luu_y": [
            (
                "Học từng thức một, không cố học hết 8 thức ngay: "
                "Thái Cực Quyền cần thời gian để cơ thể ghi nhớ chuyển động cơ bắp. "
                "Học thức 1–2 thật thuần thục trong tuần đầu, "
                "mỗi tuần thêm 1–2 thức cho đến khi hoàn thành cả bài."
            ),
            (
                "Tập trên nền phẳng, không trơn — bắt buộc: "
                "nhiều thức có chuyển trọng tâm sang ngang và bước chân, "
                "sàn gạch men trơn rất nguy hiểm. Mang giày thể thao đế bằng "
                "hoặc đứng trên thảm tập — không tập chân trần trong nhà."
            ),
            (
                "Đứng gần tường khi mới bắt đầu học: "
                "người mới chưa quen chuyển trọng tâm dễ mất thăng bằng "
                "ở thức 5 (Đẩy khỉ lùi) và thức 7 (Thoi thợ dệt). "
                "Tựa tay vào tường khi cần — an toàn luôn quan trọng hơn đúng hình thức."
            ),
        ],
    },

}

# ── Helper: lấy danh sách theo nhóm tuổi ──────────────────────────────────────
def get_by_group(nhom_tuoi: str) -> list:
    """Trả về list các bài tập theo nhóm tuổi. nhom_tuoi='' hoặc 'Tất cả' → trả hết."""
    if not nhom_tuoi or nhom_tuoi == "Tất cả":
        return list(EXERCISE_MAP.values())
    return [v for v in EXERCISE_MAP.values() if v["nhom_tuoi"] == nhom_tuoi]


def get_by_id(exercise_id: str) -> dict | None:
    """Trả về dict bài tập theo id, None nếu không tìm thấy."""
    return EXERCISE_MAP.get(exercise_id)


# ── Helper: kiểm tra file asset ────────────────────────────────────────────────
# Dùng chung cho gym (thumbnail + video)
# Trả về dict với 2 key: "thumbnail" và "video"
# Giá trị mỗi key là FILE_FOUND hoặc FILE_NOT_FOUND
# Dùng trong page_gym.py trước khi load ảnh/video để tránh crash

FILE_FOUND     = "✓ Có file"
FILE_NOT_FOUND = "✗ Không tìm thấy file"

def check_assets(exercise: dict) -> dict:
    """
    Kiểm tra thumbnail và video của 1 bài tập có tồn tại không.

    Tham số:
        exercise : dict từ EXERCISE_MAP

    Trả về:
        {
            "thumbnail": "✓ Có file" | "✗ Không tìm thấy file",
            "video":     "✓ Có file" | "✗ Không tìm thấy file",
        }

    Dùng trong page_gym.py:
        _st = check_assets(exercise)
        if _st["thumbnail"] == FILE_FOUND:
            lbl.setPixmap(QPixmap(exercise["thumbnail"]))
        else:
            lbl.setText(_st["thumbnail"])   # hiện "✗ Không tìm thấy file"
    """
    return {
        "thumbnail": FILE_FOUND if _os.path.exists(exercise.get("thumbnail", "")) else FILE_NOT_FOUND,
        "video":     FILE_FOUND if _os.path.exists(exercise.get("video", ""))     else FILE_NOT_FOUND,
    }


def check_all_assets() -> dict:
    """
    Kiểm tra toàn bộ asset trong EXERCISE_MAP — dùng khi debug lúc khởi động app.

    Cách gọi trong fooderMain.py:
        from pages.gym_exercise_map import check_all_assets
        for bai_id, status in check_all_assets().items():
            print(f"{bai_id:20} | thumbnail={status['thumbnail']} | video={status['video']}")
    """
    return {ex_id: check_assets(ex) for ex_id, ex in EXERCISE_MAP.items()}