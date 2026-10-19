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
| **Deep-Translator** | Sử dụng thư viện dịch thuật để viết Script tự động hóa (`scripts/translate_bot.py`), tự động chuyển đổi kho dữ liệu hàng ngàn dòng từ Tiếng Anh sang Tiếng Việt mà không làm hỏng định dạng file YAML. |
| **Rule & Memoization Policy** | Chính sách học ghi nhớ và xử lý theo quy tắc cố định (ví dụ: luôn chào hỏi khi người dùng say "hi"). |
| **LLM Fallback (Groq API)** | Tích hợp Large Language Model để xử lý các câu hỏi nằm ngoài kịch bản đã huấn luyện của mô hình. |
| **SentenceTransformer & DBSCAN** | Ứng dụng trong các kịch bản tiền xử lý, mã hóa câu (embedding) và phân cụm dữ liệu chưa gán nhãn để tự động mở rộng kiến thức. |

---

## 📁 Cấu trúc thư mục

```
source/
├── README.md               # Tài liệu hướng dẫn chi tiết về dự án và cách triển khai
├── requirements.txt        # Danh sách các thư viện Python phụ thuộc (Rasa, Flask, Groq, ...)
│
├── # ── Rasa Core & Pipeline (bắt buộc ở root) ──
├── config.yml              # Cấu hình Pipeline NLU (DIET, Featurizer) và chính sách đối thoại (Policies)
├── domain.yml              # Khai báo Intents, Entities, Slots, Responses và danh sách Custom Actions
├── endpoints.yml           # Cấu hình kết nối Action Server (port 5055) và Tracker Store
├── credentials.yml         # Thiết lập các kênh giao tiếp đầu vào (REST API webhook, Rasa Enterprise, ...)
│
├── config/                 # Cấu hình ứng dụng và bảo mật
│   └── api_keys.json       # Lưu trữ khóa API cho các dịch vụ ngoài (Groq API LLaMA 3)
│
├── data/                   # Kho dữ liệu để Rasa học (Training Data)
│   ├── nlu.yml             # Dữ liệu NLU: Danh sách các câu mẫu theo từng ý định (Intents & Examples)
│   ├── rules.yml           # Các quy tắc phản xạ logic cố định (Chào hỏi, tạm biệt, kích hoạt fallback)
│   ├── stories.yml         # Kịch bản hội thoại mẫu theo ngữ cảnh nhiều lượt (Stories)
│   └── test_stories.yml    # Bộ kịch bản kiểm thử (Test Stories) để tự động đánh giá độ chính xác (rasa test)
│
├── actions/                # Custom Actions Server (Xử lý logic nghiệp vụ bằng Python)
│   ├── __init__.py         # Khởi tạo Python module cho actions
│   └── actions.py          # Logic gợi ý bài tập theo cơ bắp (kèm link YouTube), Fallback qua Groq LLM
│
├── webapp/                 # Ứng dụng Giao diện Web tương tác với Chatbot (Flask Web App)
│   ├── app.py              # Backend Server Flask nhận tin nhắn từ giao diện và gọi Rasa API (port 5005)
│   └── templates/
│       └── index.html      # Giao diện Frontend UI/UX hiện đại (Dark Mode, Glassmorphism, hiệu ứng gõ)
│
├── scripts/                # Bộ công cụ tự động hóa và tiền xử lý dữ liệu (Data Pipeline)
│   ├── __init__.py         # Khởi tạo Python module cho scripts
│   ├── translate_bot.py    # Dịch tự động tập dữ liệu NLU & Domain sang tiếng Việt (giữ nguyên chuẩn YAML)
│   ├── clustering_intents.py # Gom cụm câu hỏi chưa gán nhãn bằng SentenceTransformer & thuật toán DBSCAN
│   ├── data_prepare.py     # Tự động chèn intents/responses mới vào nlu.yml, domain.yml, rules.yml
│   └── save_data.py        # Cập nhật intent và câu hỏi mới vào dataset thô, dọn dẹp file tạm
│
├── dataset/                # Kho dữ liệu thô ban đầu phục vụ nghiên cứu và mở rộng
│   ├── Intents.json        # Dữ liệu phân loại ý định thô dạng JSON (mapping intent và questions)
│   ├── Questions.txt       # Danh sách câu hỏi thu thập từ người dùng
│   └── Responses.json      # Danh sách câu trả lời tương ứng với từng intent
│
└── models/                 # Thư mục lưu các mô hình AI đã huấn luyện thành công (file nén .tar.gz)
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