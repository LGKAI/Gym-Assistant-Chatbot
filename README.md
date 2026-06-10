# Gym Assistant Chatbot

Đây là sản phẩm Chatbot hỗ trợ tư vấn Gym, được xây dựng bằng Rasa cho backend và Flask cho giao diện người dùng.

## Cấu trúc thư mục
- `actions/`: Chứa mã nguồn cho các Custom Actions của Rasa.
- `data/`: Chứa dữ liệu huấn luyện cho Rasa (nlu, stories, rules).
- `models/`: Chứa các mô hình Rasa đã được huấn luyện.
- `scripts/`: Các file mã nguồn phụ trợ dùng để tiền xử lý và chuẩn bị dữ liệu.
- `templates/`: File HTML giao diện web.
- `app.py`: Mã nguồn Flask app (Frontend).
- `config.yml`, `domain.yml`, `endpoints.yml`, `credentials.yml`: Các file cấu hình hệ thống của Rasa.

## Hướng dẫn cài đặt và chạy sản phẩm

### 1. Cài đặt môi trường
Khuyến khích sử dụng môi trường ảo (virtual environment). Yêu cầu Python từ 3.8 đến 3.10 để tương thích tốt nhất với Rasa.

```bash
# Tạo và kích hoạt môi trường ảo (venv) trên Windows
python -m venv venv
.\venv\Scripts\activate

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### 2. Khởi chạy ứng dụng

Sản phẩm bao gồm 3 tiến trình hoạt động độc lập cần chạy song song. Bạn hãy mở **3 cửa sổ Terminal (hoặc Command Prompt / PowerShell) riêng biệt**, đảm bảo đã kích hoạt môi trường ảo ở cả 3 cửa sổ và chạy lần lượt các lệnh sau:

**Terminal 1: Chạy Rasa Action Server**
```bash
rasa run actions
```
*(Server này chạy ở port mặc định 5055, có nhiệm vụ xử lý các custom actions)*

**Terminal 2: Chạy Rasa API Server**
```bash
rasa run -m models --enable-api --cors "*"
```
*(Server này chạy ở port 5005, đóng vai trò là não bộ của Chatbot)*

**Terminal 3: Chạy Flask Web Server (Giao diện người dùng)**
```bash
python app.py
```
*(Giao diện web chạy ở port 5000)*

### 3. Trải nghiệm sản phẩm
Sau khi cả 3 server trên đều khởi động thành công, bạn mở trình duyệt web và truy cập vào đường dẫn:
👉 **[http://localhost:5000](http://localhost:5000)**

---

## Hướng dẫn huấn luyện lại mô hình (Tùy chọn)
Nếu bạn có bổ sung thêm dữ liệu (vào thư mục `data/`) hoặc thay đổi file `domain.yml`, bạn cần huấn luyện lại mô hình Rasa bằng lệnh:
```bash
rasa train
```
Sau khi huấn luyện xong, mô hình mới sẽ được lưu vào thư mục `models/`. Bạn cần tắt (Ctrl+C) và khởi động lại **Terminal 2** để áp dụng mô hình mới.