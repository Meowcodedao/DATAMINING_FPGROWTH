# DATAMINING_FPGROWTH

Dưới đây là một mẫu **README.md** ngắn gọn, chuẩn cấu trúc GitHub, mô tả rõ đề tài “Khai phá luật kết hợp bằng giải thuật FP-Growth với Python” — bạn chỉ cần copy và lưu thành file `README.md` ngay trong thư mục dự án của bạn nhé 👇

---

```markdown
# 🧠 DATAMINING_FPGROWTH

## 📘 Giới thiệu
Đề tài: **Khai phá luật kết hợp (Association Rule Mining)** sử dụng **giải thuật FP-Growth** được cài đặt bằng **Python**.  
Mục tiêu của dự án là **tìm ra các mối quan hệ tiềm ẩn** giữa các thuộc tính trong tập dữ liệu, giúp phát hiện các mẫu dữ liệu thường xuyên (frequent patterns) một cách **hiệu quả và tiết kiệm bộ nhớ** hơn so với Apriori.

---

## ⚙️ Mục tiêu chính
- Cài đặt **giải thuật FP-Growth** để khai phá tập mẫu phổ biến.  
- Sinh ra các **luật kết hợp** (association rules) từ dữ liệu đã xử lý.  
- So sánh kết quả với các thuật toán khác (nếu có).  
- Ứng dụng vào bài toán thực tế (ví dụ: dữ liệu sinh viên y khoa, mua hàng, hoặc hành vi người dùng).

---

## 📂 Cấu trúc thư mục
```

DATA_MINING/
│
├── medical_students_dataset.csv     # Bộ dữ liệu mẫu được sử dụng
├── main.py                          # Chương trình chính: cài đặt và chạy FP-Growth
├── fpgrowth.py                      # Thuật toán FP-Growth (nếu tách riêng)
├── utils.py                         # Hàm hỗ trợ xử lý dữ liệu (nếu có)
└── README.md                        # Tài liệu mô tả dự án

````

---

## 🚀 Cách chạy chương trình
### 1. Cài đặt môi trường
```bash
pip install pandas numpy
````

### 2. Chạy chương trình

```bash
python main.py
```

Kết quả sẽ hiển thị **các tập phổ biến (frequent itemsets)** và **luật kết hợp** được sinh ra từ dữ liệu.

---

## 📊 Giải thuật FP-Growth

FP-Growth hoạt động theo hai giai đoạn:

1. **Xây dựng cây FP-tree (Frequent Pattern Tree)** để nén dữ liệu.
2. **Duyệt cây đệ quy** để sinh ra các mẫu phổ biến mà không cần tạo các tập ứng viên (candidate sets).

Ưu điểm:

* Hiệu năng cao hơn Apriori.
* Giảm đáng kể số lần quét cơ sở dữ liệu.
* Phù hợp cho tập dữ liệu lớn.

---

## 🧩 Ứng dụng thực tế

* Phân tích hành vi khách hàng trong thương mại điện tử.
* Phát hiện mẫu hành vi y khoa trong dữ liệu bệnh nhân/sinh viên y.
* Đề xuất sản phẩm (Recommendation Systems).

---

## ✍️ Tác giả

* **Tên:** (Điền tên bạn)
* **Trường:** Trường Đại học Giao thông Vận tải (UTC)
* **Môn học:** Khai phá dữ liệu (Data Mining)

---

## 📜 Giấy phép

Dự án được chia sẻ cho mục đích học tập và nghiên cứu.

```

---

Bạn có muốn mình **viết thêm phần mô tả chi tiết cách hoạt động của FP-Growth bằng sơ đồ và ví dụ minh họa nhỏ** (có thể hiển thị đẹp trong README GitHub) không?  
Phần đó sẽ giúp bạn có README chuyên nghiệp hơn nếu cần nộp báo cáo hoặc demo cho giảng viên.
```

