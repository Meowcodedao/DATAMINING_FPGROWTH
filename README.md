# FP-Growth Algorithm - Medical Students Data Analysis

## 📋 Mô tả dự án

Dự án này sử dụng thuật toán **FP-Growth (Frequent Pattern Growth)** để phân tích dữ liệu sinh viên y khoa và tìm ra các mẫu thường xuyên (frequent patterns) cũng như các luật kết hợp (association rules) giữa các đặc điểm sức khỏe.

---

## 🧠 Thuật toán FP-Growth

### Khái niệm

**FP-Growth** là một thuật toán khai phá tập phổ biến (frequent itemset mining) hiệu quả hơn thuật toán Apriori truyền thống. Thay vì sinh ra các tập ứng viên (candidate generation), FP-Growth sử dụng cấu trúc dữ liệu **FP-Tree** để nén cơ sở dữ liệu và khai thác trực tiếp các tập phổ biến.

### Ưu điểm
- ✅ **Hiệu quả cao**: Không cần sinh tập ứng viên
- ✅ **Tiết kiệm bộ nhớ**: Sử dụng FP-Tree để nén dữ liệu
- ✅ **Chỉ quét database 2 lần**: Một lần để đếm support, một lần để xây FP-Tree
- ✅ **Phù hợp với dữ liệu lớn**: Xử lý tốt với datasets có nhiều transactions

### Quy trình hoạt động

1. **Quét lần 1**: Đếm tần suất xuất hiện của mỗi item và loại bỏ items không đạt min_support
2. **Sắp xếp**: Sắp xếp items theo thứ tự tần suất giảm dần
3. **Xây FP-Tree**: Quét lần 2 để xây dựng FP-Tree (cây tiền tố chung)
4. **Khai phá**: Đệ quy khai phá các pattern từ FP-Tree

### Các tham số quan trọng

- **min_support**: Ngưỡng support tối thiểu (0-1). Item/itemset phải xuất hiện ít nhất bao nhiêu % transactions
- **min_confidence**: Ngưỡng confidence tối thiểu cho association rules (0-1)
- **lift**: Đo lường mức độ phụ thuộc giữa antecedent và consequent

---

## 📊 Dữ liệu

### File đầu vào: `medical_students_FP_ready.csv`

Dataset chứa thông tin về **98,976 sinh viên y khoa** với các đặc điểm:

| Cột | Mô tả | Giá trị |
|-----|-------|---------|
| Student ID | Mã sinh viên | Unique ID |
| Age | Nhóm tuổi | Age_18_22, Age_23_27, Age_28_34, Age_35+ |
| Gender | Giới tính | Male, Female |
| Height | Nhóm chiều cao (cm) | Height_150_160, Height_160_170, Height_170_180, Height_180_190, Height_190_200 |
| Weight | Nhóm cân nặng (kg) | Weight_40_50, Weight_50_60, Weight_60_70, Weight_70_80, Weight_80_90, Weight_90_100 |
| Blood Type | Nhóm máu | A, B, AB, O |
| BMI | Chỉ số BMI | BMI_Underweight, BMI_Normal, BMI_Overweight, BMI_Obese |
| Temperature | Nhiệt độ cơ thể | Temp_Low, Temp_Normal, Temp_High |
| Heart Rate | Nhịp tim | HR_Low, HR_Normal, HR_High |
| Blood Pressure | Huyết áp | BP_Low, BP_Normal, BP_High |
| Cholesterol | Cholesterol | Chol_Normal, Chol_Borderline, Chol_High |
| Diabetes | Tiểu đường | Yes, No |
| Smoking | Hút thuốc | Yes, No |

**Đặc điểm dữ liệu:**
- Dữ liệu đã được tiền xử lý và chuyển thành dạng categorical
- Mỗi giá trị đã được gán nhãn rõ ràng (ví dụ: `Age_18_22`, `BMI_Normal`)
- Không có giá trị missing

---

## 🔧 Logic xử lý dữ liệu

### 1. Đọc và chuẩn bị dữ liệu

```python
# Đọc CSV
df = pd.read_csv('medical_students_FP_ready.csv')

# Loại bỏ cột Student ID (không cần cho phân tích pattern)
df_analysis = df.drop(['Student ID'], axis=1, errors='ignore')
```

### 2. Chuyển đổi thành Transactions

Mỗi dòng dữ liệu được chuyển thành một **transaction** - danh sách các items:

```python
# Ví dụ transaction:
['Age_Age_18_22', 'Gender_Female', 'Height_Height_160_170', 
 'Weight_Weight_70_80', 'Blood Type_O', 'BMI_BMI_Overweight', 
 'Temperature_Temp_Normal', 'Heart Rate_HR_High', ...]
```

**Logic:** Kết hợp tên cột và giá trị để tạo item có nghĩa (`{column}_{value}`)

### 3. One-Hot Encoding

Sử dụng `TransactionEncoder` để chuyển transactions thành ma trận binary:

```
Item              Transaction1  Transaction2  Transaction3
Age_18_22              1             0             1
Gender_Female          1             1             0
BMI_Normal             0             1             1
...
```

**Tối ưu:** Sử dụng sparse matrix để tiết kiệm bộ nhớ với datasets lớn

### 4. Áp dụng FP-Growth

```python
frequent_itemsets = fpgrowth(df_encoded, 
                             min_support=0.1,  # 10%
                             use_colnames=True)
```

Tìm tất cả itemsets xuất hiện ≥ 10% transactions

### 5. Sinh Association Rules

```python
rules = association_rules(frequent_itemsets, 
                         metric="confidence", 
                         min_threshold=0.5)  # 50%
```

Tạo rules dạng: `IF {antecedents} THEN {consequents}`

**Metrics:**
- **Support**: P(A ∩ B) - Tần suất cả A và B cùng xuất hiện
- **Confidence**: P(B|A) = P(A ∩ B) / P(A) - Xác suất B xuất hiện khi có A
- **Lift**: P(A ∩ B) / (P(A) × P(B)) - Mức độ phụ thuộc (>1: có liên quan, =1: độc lập, <1: loại trừ)

---

## 📁 Các file đầu ra

### 1. `frequent_itemsets.csv`

Danh sách các itemsets phổ biến tìm được.

**Cấu trúc:**
| Cột | Mô tả |
|-----|-------|
| itemsets | Tập các items (dạng string, phân cách bởi dấu phẩy) |
| support | Tỷ lệ xuất hiện trong toàn bộ transactions (0-1) |
| length | Số lượng items trong itemset |

**Ví dụ:**
```csv
itemsets,support,length
"Diabetes_No",0.891115,1
"Smoking_No, Diabetes_No",0.705545,2
"Temperature_Temp_Normal, Heart Rate_HR_Normal",0.587234,2
```

**Ý nghĩa:**
- Itemsets có 1 item (length=1): Các đặc điểm phổ biến nhất
- Itemsets có nhiều items: Các tổ hợp đặc điểm thường xuất hiện cùng nhau

### 2. `association_rules.csv`

Danh sách các luật kết hợp (IF-THEN rules).

**Cấu trúc:**
| Cột | Mô tả |
|-----|-------|
| antecedents | Điều kiện (IF) |
| consequents | Kết quả (THEN) |
| support | Support của toàn bộ rule |
| confidence | Độ tin cậy: P(consequents \| antecedents) |
| lift | Mức độ liên kết |
| leverage | support(A∪B) - support(A)×support(B) |
| conviction | Mức độ ràng buộc của rule |

**Ví dụ:**
```csv
antecedents,consequents,support,confidence,lift
"Weight_Weight_40_50","BMI_BMI_Underweight, Smoking_No",0.113179,0.688295,3.096154
```

**Đọc hiểu:** 
- **Nếu** sinh viên có cân nặng 40-50kg 
- **Thì** 68.8% khả năng họ có BMI Underweight và không hút thuốc
- **Lift = 3.1**: Tổ hợp này xuất hiện cùng nhau gấp 3.1 lần so với ngẫu nhiên

### 3. `fpgrowth_itemsets_analysis.png`

Biểu đồ trực quan phân tích frequent itemsets.

**Gồm 2 sub-plots:**

#### a) Phân bố Support
- **Trục X**: Giá trị support (0-1)
- **Trục Y**: Số lượng itemsets
- **Ý nghĩa**: Cho thấy phân bố tần suất của các itemsets
  - Phần lớn itemsets có support thấp
  - Một số ít có support cao (rất phổ biến)

#### b) Itemsets theo độ dài
- **Trục X**: Độ dài itemset (số items trong set)
- **Trục Y**: Số lượng itemsets
- **Ý nghĩa**: 
  - Itemsets đơn (1 item): Nhiều nhất
  - Itemsets lớn hơn: Giảm dần (ít tổ hợp lớn thỏa mãn min_support)

### 4. `fpgrowth_rules_analysis.png`

Biểu đồ phân tích association rules.

**Gồm 2 sub-plots:**

#### a) Support vs Confidence (màu = Lift)
- **Trục X**: Support của rule
- **Trục Y**: Confidence của rule  
- **Màu sắc**: Giá trị Lift (gradient)
- **Ý nghĩa**: 
  - Rules ở góc trên phải: Support cao + Confidence cao → Rất có giá trị
  - Màu sáng (lift cao): Rules có liên kết mạnh

#### b) Top 15 Rules theo Lift
- **Biểu đồ cột ngang** hiển thị 15 rules có lift cao nhất
- **Ý nghĩa**: Các rules có mối liên hệ mạnh nhất
- **Cách sử dụng**: Tham khảo file `association_rules.csv` với Rule ID tương ứng

---

## 🚀 Cách chạy

### Yêu cầu

```bash
pip install pandas mlxtend matplotlib seaborn
```

### Chạy phân tích

```bash
python fpgrowth_analysis.py
```

### Tùy chỉnh tham số

Sửa các biến trong file `fpgrowth_analysis.py`:

```python
MIN_SUPPORT = 0.1      # Tăng để giảm số itemsets (chạy nhanh hơn)
MIN_CONFIDENCE = 0.5   # Tăng để lọc rules chất lượng cao hơn
SAMPLE_SIZE = None     # Đặt số (vd: 20000) để lấy mẫu, None = toàn bộ
```

**Gợi ý:**
- Dữ liệu nhỏ (<20k rows): `MIN_SUPPORT = 0.05`, `SAMPLE_SIZE = None`
- Dữ liệu lớn (>50k rows): `MIN_SUPPORT = 0.1`, `SAMPLE_SIZE = 30000`
- Tìm patterns hiếm: Giảm `MIN_SUPPORT` xuống 0.01-0.03

---

## 📈 Kết quả phân tích

### Thống kê tổng quan (toàn bộ dataset)

- **Số transactions**: 98,976
- **Số items khác nhau**: 53
- **Frequent itemsets tìm được**: 938 (với min_support=10%)
- **Association rules**: 3,084 (với min_confidence=50%)

### Top Frequent Items

| Item | Support | Ý nghĩa |
|------|---------|---------|
| Diabetes_No | 89.1% | Đa số sinh viên không có tiểu đường |
| Smoking_No | 79.2% | Đa số sinh viên không hút thuốc |
| Temperature_Temp_Normal | 77.8% | Nhiệt độ cơ thể bình thường là phổ biến |
| Heart Rate_HR_Normal | 74.2% | Nhịp tim bình thường chiếm đa số |

### Top Association Rules (Lift cao nhất)

1. **Weight_40_50 → BMI_Underweight + Smoking_No**
   - Confidence: 68.8%
   - Lift: 3.10
   - Ý nghĩa: Cân nặng thấp liên quan mạnh với BMI thấp và không hút thuốc

2. **BMI_Underweight + Smoking_No → Weight_40_50**
   - Confidence: 50.9%
   - Lift: 3.10
   - Ý nghĩa: Ngược lại cũng đúng - người có BMI thấp và không hút thuốc thường có cân nặng 40-50kg

3. **Weight_40_50 + Diabetes_No → BMI_Underweight + Smoking_No**
   - Confidence: 68.9%
   - Lift: 3.10
   - Ý nghĩa: Kết hợp cân nặng thấp và không tiểu đường dự đoán tốt BMI thấp + không hút thuốc

---

## 🎯 Ứng dụng thực tế

### 1. Y tế công cộng
- Nhận diện các nhóm sinh viên có nguy cơ sức khỏe
- Thiết kế chương trình can thiệp dựa trên patterns

### 2. Nghiên cứu
- Khám phá mối liên hệ giữa các yếu tố sức khỏe
- Xác định các tổ hợp đặc điểm cần nghiên cứu sâu hơn

### 3. Dự đoán
- Sử dụng rules để dự đoán đặc điểm sức khỏe chưa biết
- Hệ thống cảnh báo sức khỏe

---

## 📝 Lưu ý

### Về dữ liệu
- Dữ liệu đã được tiền xử lý và phân loại
- Kết quả phản ánh mẫu dữ liệu cụ thể này, không nhất thiết đại diện cho tổng thể

### Về kết quả
- **Correlation ≠ Causation**: Lift cao không có nghĩa là quan hệ nhân quả
- Rules với support thấp có thể không có ý nghĩa thống kê
- Cần chuyên gia y tế để diễn giải kết quả

### Tối ưu hóa
- Với datasets lớn (>100k rows), nên sử dụng `SAMPLE_SIZE` hoặc tăng `MIN_SUPPORT`
- Sparse matrix giúp tiết kiệm bộ nhớ đáng kể
- Vectorized operations (apply) nhanh hơn nhiều so với vòng lặp

---

## 📚 Tài liệu tham khảo

- [FP-Growth Algorithm Paper](https://dl.acm.org/doi/10.1145/335191.335372) - Han et al., 2000
- [mlxtend Documentation](http://rasbt.github.io/mlxtend/)
- [Association Rule Learning](https://en.wikipedia.org/wiki/Association_rule_learning)

---

## 👨‍💻 Tác giả

Data Mining Project - UTC
- **Repository**: DATAMINING_FPGROWTH
- **Date**: November 2025

---

## 📄 License

Educational project - UTC Data Mining Course
