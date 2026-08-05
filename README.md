# Gym Assistant Chatbot

Đồ án Giới thiệu ngành AI

Đây là một trợ lý ảo thông minh chuyên tư vấn về thể hình, dinh dưỡng, và phương pháp tập luyện. Chatbot được huấn luyện hoàn toàn bằng tiếng Việt và đi kèm với một giao diện Web hiện đại, đẹp mắt.

---

## 🛠 Công nghệ và Kiến thức sử dụng

Dự án áp dụng nhiều công nghệ từ xây dựng mô hình Học Máy (Machine Learning) đến Phát triển Web (Web Development):

| Công nghệ / Thư viện | Vai trò trong dự án |
|---|---|
| **Rasa Open Source (3.x)** | Framework AI cốt lõi (NLU & Dialogue Management) quản lý luồng hội thoại và hiểu ngôn ngữ tự nhiên. |
| **DIET Classifier** | Mô hình Deep Learning đa nhiệm bên trong Rasa dùng để phân loại ý định (Intent Classification) và trích xuất thực thể (Entity Recognition). |
| **CountVectorsFeaturizer** | Kỹ thuật trích xuất đặc trưng văn bản dựa trên `char_wb` n-grams, giúp mô hình hoạt động cực kỳ hiệu quả với ngôn ngữ tiếng Việt (kể cả không có dấu) mà không cần mô hình ngôn ngữ khổng lồ. |
| **Flask (Python)** | Web framework đóng vai trò làm Backend trung gian, nhận yêu cầu từ người dùng và giao tiếp với Rasa API. |
| **HTML / CSS / Vanilla JS** | Giao diện Frontend hiện đại theo phong cách **Dark Mode** & **Glassmorphism** (hiệu ứng kính mờ). Tích hợp hiệu ứng "đang gõ" (typing indicator), thiết kế màu sắc bong bóng chat tách biệt và bộ icon từ **FontAwesome**. |
| **Deep-Translator** | Sử dụng thư viện dịch thuật để viết Script tự động hóa (`translate_bot.py`), tự động chuyển đổi kho dữ liệu hàng ngàn dòng từ Tiếng Anh sang Tiếng Việt mà không làm hỏng định dạng file YAML. |
| **Rule & Memoization Policy** | Chính sách học ghi nhớ và xử lý theo quy tắc cố định (ví dụ: luôn chào hỏi khi người dùng say "hi"). |
| **LLM Fallback (Groq API)** | Tích hợp Large Language Model để xử lý các câu hỏi nằm ngoài kịch bản đã huấn luyện của mô hình. |
| **SentenceTransformer & DBSCAN** | Ứng dụng trong các kịch bản tiền xử lý, mã hóa câu (embedding) và phân cụm dữ liệu chưa gán nhãn để tự động mở rộng kiến thức. |

---

## 📁 Cấu trúc thư mục

```
source/
├── README.md
├── requirements.txt
├── translate_bot.py        # Script tự động dịch dữ liệu NLU & Domain sang tiếng Việt
├── fix_rules.py            # Script hỗ trợ chuẩn hóa cú pháp file rules.yml
│
├── # ── Rasa (bắt buộc ở root) ──────────────────
├── config.yml              # Cấu hình Pipeline NLU và policies (Bộ não của Rasa)
├── domain.yml              # Khai báo Intents, entities, actions, và toàn bộ câu trả lời
├── endpoints.yml           # Kết nối với Action Server
├── credentials.yml         # Thông tin xác thực
│
├── config/                 # Cấu hình ứng dụng
│   └── api_keys.json       # Khóa API (Ví dụ: Groq)
│
├── data/                   # Kho dữ liệu để Rasa học (Training Data)
│   ├── nlu.yml             # Dữ liệu dạy bot hiểu (Người dùng nói gì)
│   ├── rules.yml           # Các quy tắc phản xạ cứng của bot
│   ├── stories.yml         # Các kịch bản hội thoại mẫu
│   └── test_stories.yml
│
├── actions/                # Custom Actions (Code xử lý logic bằng Python)
│   ├── __init__.py
│   └── actions.py
│
├── webapp/                 # Giao diện Web (Flask)
│   ├── app.py              # Backend Server
│   └── templates/
│       └── index.html      # Giao diện Frontend UI/UX
│
├── scripts/                # Các script tiền xử lý dữ liệu khác
│   ├── __init__.py
│   ├── data_prepare.py
│   ├── save_data.py
│   └── clustering_intents.py
│
├── dataset/                # Dữ liệu thô ban đầu
│
└── models/                 # Chứa các mô hình AI đã được compile (.tar.gz) sau khi train
```

---

## 🚀 Hướng dẫn cài đặt và chạy sản phẩm

### 1. Cài đặt môi trường

Lưu ý quan trọng: Yêu cầu **Python 3.8 – 3.10** để tương thích tốt nhất với Rasa 3.6.

```bash
# 1. Tạo và kích hoạt môi trường ảo (Virtual Environment) trên Windows
py -3.10 -m venv venv
.\venv\Scripts\activate

# 2. Cài đặt các gói thư viện cơ bản
pip install -r requirements.txt

# 3. [LƯU Ý]: Fix lỗi xung đột của thư viện apscheduler với setuptools mới
pip install "setuptools<70.0.0"
```

### 2. Khởi chạy hệ thống

Sản phẩm hoạt động bằng cách chạy song song 3 tiến trình. Bạn hãy mở **3 cửa sổ Terminal** riêng biệt, kích hoạt môi trường ảo (chạy `.\venv\Scripts\activate`) ở cả 3 cửa sổ, rồi chạy lần lượt:

**Terminal 1 — Rasa Action Server** *(Chạy mã logic - port 5055)*
```bash
rasa run actions
```

**Terminal 2 — Rasa API Server** *(Chạy não bộ AI - port 5005)*
```bash
rasa run -m models --enable-api --cors "*"
```

**Terminal 3 — Flask Web Server** *(Chạy giao diện Web - port 5000)*
```bash
python webapp/app.py
```

### 3. Trải nghiệm sản phẩm

Sau khi cả 3 server khởi động thành công (không có lỗi màu đỏ), mở trình duyệt web và truy cập:

👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

Tại đây, bạn có thể nhập các câu hỏi tiếng Việt như: *"Làm sao để giảm cân"*, *"Tập tạ có lợi ích gì"*, *"Có nên ăn trước khi tập không"*...

---

## 🧠 Hướng dẫn huấn luyện lại mô hình (Retrain)

Chatbot sẽ càng thông minh nếu được cung cấp thêm nhiều câu hỏi đa dạng. 
Nếu bạn chỉnh sửa hoặc bổ sung thêm dữ liệu vào thư mục `data/` (như `nlu.yml` hay `rules.yml`), bạn **bắt buộc phải huấn luyện (train) lại mô hình**:

```bash
rasa train
```

Quá trình này mất khoảng 2-3 phút. Sau khi hoàn tất thành công, mô hình mới sẽ được lưu vào thư mục `models/`. Bạn chỉ cần **Tắt (Ctrl + C)** và chạy lại lệnh ở **Terminal 2** để load mô hình vừa mới học xong.