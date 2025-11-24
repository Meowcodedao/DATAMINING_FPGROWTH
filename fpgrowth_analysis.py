import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules
import matplotlib.pyplot as plt

# ---------- Cấu hình ----------
INPUT_FILE = 'medical_students_FP_ready.csv'
MIN_SUPPORT = 0.1     # thử nghiệm trước để giảm số lượng itemsets
MIN_CONFIDENCE = 0.5  # confidence tối thiểu cho rules
TOP_ITEMSETS = 5       # số lượng itemsets hiển thị
TOP_RULES = 10         # số lượng rules hiển thị
CREATE_PLOTS = True    # True nếu muốn tạo hình
SAMPLE_SIZE = None     # Lấy mẫu bao nhiêu dòng (None = lấy hết). Giảm để chạy nhanh hơn

# ---------- Đọc dữ liệu ----------
print("Đang đọc dữ liệu...")
df = pd.read_csv(INPUT_FILE)
print(f"Kích thước dữ liệu gốc: {df.shape}")

# Lấy mẫu nếu SAMPLE_SIZE được set
if SAMPLE_SIZE is not None and len(df) > SAMPLE_SIZE:
    print(f"⚡ Lấy mẫu {SAMPLE_SIZE} dòng để chạy nhanh hơn...")
    df = df.sample(n=SAMPLE_SIZE, random_state=42)
    print(f"✓ Kích thước sau khi lấy mẫu: {df.shape}")

# Loại bỏ cột Student ID
df_analysis = df.drop(['Student ID'], axis=1, errors='ignore')

# ---------- Chuyển dữ liệu thành transactions ----------
print("Đang chuyển đổi dữ liệu thành transactions...")
transactions = df_analysis.apply(
    lambda row: [f"{col}_{row[col]}" for col in df_analysis.columns if pd.notna(row[col])],
    axis=1
).tolist()

print(f"Số lượng transactions: {len(transactions)}")
print(f"Ví dụ transaction đầu tiên: {transactions[0]}")

# ---------- TransactionEncoder với sparse ----------
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions, sparse=True)
df_encoded = pd.DataFrame.sparse.from_spmatrix(te_ary, columns=te.columns_)
print(f"Dữ liệu đã encode (sparse): {df_encoded.shape}")

# ---------- FP-Growth ----------
print(f"\nÁp dụng FP-Growth với min_support={MIN_SUPPORT}...")
frequent_itemsets = fpgrowth(df_encoded, min_support=MIN_SUPPORT, use_colnames=True)
frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
frequent_itemsets = frequent_itemsets.sort_values('support', ascending=False)
print(f"Số lượng frequent itemsets: {len(frequent_itemsets)}")
print("Top itemsets:")
print(frequent_itemsets.head(TOP_ITEMSETS))

# ---------- Association Rules ----------
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=MIN_CONFIDENCE)
rules = rules.sort_values('lift', ascending=False)
print(f"Số lượng rules với confidence >= {MIN_CONFIDENCE}: {len(rules)}")
print("Top rules:")
print(rules.head(TOP_RULES)[['antecedents','consequents','support','confidence','lift']])

# ---------- Lưu kết quả ----------
# Format Frequent Itemsets - dễ nhìn hơn
frequent_itemsets_to_save = frequent_itemsets.copy().reset_index(drop=True)
frequent_itemsets_to_save.insert(0, 'Rank', range(1, len(frequent_itemsets_to_save) + 1))
frequent_itemsets_to_save['itemsets'] = frequent_itemsets_to_save['itemsets'].apply(lambda x: ', '.join(sorted(list(x))))
frequent_itemsets_to_save['support'] = frequent_itemsets_to_save['support'].round(4)
frequent_itemsets_to_save['support_percent'] = (frequent_itemsets_to_save['support'] * 100).round(2).astype(str) + '%'
# Sắp xếp cột cho dễ đọc
frequent_itemsets_to_save = frequent_itemsets_to_save[['Rank', 'itemsets', 'support', 'support_percent', 'length']]
frequent_itemsets_to_save.columns = ['Rank', 'Items', 'Support', 'Support (%)', 'Length']
frequent_itemsets_to_save.to_csv('frequent_itemsets.csv', index=False, encoding='utf-8-sig')
print("✓ Đã lưu frequent_itemsets.csv")

# Format Association Rules - dễ nhìn hơn
if len(rules) > 0:
    rules_to_save = rules.copy().reset_index(drop=True)
    rules_to_save.insert(0, 'Rule_ID', range(1, len(rules_to_save) + 1))
    rules_to_save['antecedents'] = rules_to_save['antecedents'].apply(lambda x: ', '.join(sorted(list(x))))
    rules_to_save['consequents'] = rules_to_save['consequents'].apply(lambda x: ', '.join(sorted(list(x))))
    # Làm tròn các số
    rules_to_save['support'] = rules_to_save['support'].round(4)
    rules_to_save['confidence'] = rules_to_save['confidence'].round(4)
    rules_to_save['lift'] = rules_to_save['lift'].round(4)
    # Thêm cột phần trăm
    rules_to_save['confidence_percent'] = (rules_to_save['confidence'] * 100).round(2).astype(str) + '%'
    # Chọn các cột quan trọng và đổi tên
    rules_to_save = rules_to_save[['Rule_ID', 'antecedents', 'consequents', 'support', 'confidence', 'confidence_percent', 'lift']]
    rules_to_save.columns = ['Rule ID', 'IF (Antecedents)', 'THEN (Consequents)', 'Support', 'Confidence', 'Confidence (%)', 'Lift']
    rules_to_save.to_csv('association_rules.csv', index=False, encoding='utf-8-sig')
    print("✓ Đã lưu association_rules.csv")

# ---------- Visualization nhẹ ----------
if CREATE_PLOTS:
    fig, ax = plt.subplots(1, 2, figsize=(12,5))

    # Phân bố support
    ax[0].hist(frequent_itemsets['support'], bins=20, edgecolor='black', alpha=0.7)
    ax[0].set_xlabel('Support')
    ax[0].set_ylabel('Frequency')
    ax[0].set_title('Phân bố Support')

    # Itemsets theo độ dài
    frequent_itemsets['length'].value_counts().sort_index().plot(kind='bar', ax=ax[1], edgecolor='black', alpha=0.7)
    ax[1].set_xlabel('Độ dài Itemset')
    ax[1].set_ylabel('Số lượng')
    ax[1].set_title('Itemsets theo độ dài')
    ax[1].tick_params(axis='x', rotation=0)

    plt.tight_layout()
    plt.savefig('fpgrowth_itemsets_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Đã lưu fpgrowth_itemsets_analysis.png")

    if len(rules) > 0:
        fig, ax = plt.subplots(figsize=(6,5))
        ax.scatter(rules['support'], rules['confidence'], alpha=0.6, c=rules['lift'], cmap='viridis', s=50)
        ax.set_xlabel('Support')
        ax.set_ylabel('Confidence')
        ax.set_title('Rules: Support vs Confidence (color=Lift)')
        plt.colorbar(ax.collections[0], label='Lift')
        plt.tight_layout()
        plt.savefig('fpgrowth_rules_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("✓ Đã lưu fpgrowth_rules_analysis.png")

print("\n✓ Hoàn thành!")
