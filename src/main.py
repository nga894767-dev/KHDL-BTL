import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# =========================
# ĐỌC FILE ĐÃ LÀM SẠCH
# =========================

data = pd.read_csv(
    "data/creditcard_clean.csv"
)

# =========================
# INPUT / OUTPUT
# =========================

X = data.drop(columns=['Class'])

y = data['Class']

# =========================
# CHIA TRAIN / TEST
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =========================
# TẠO MODEL AI
# =========================

model = DecisionTreeClassifier(
    max_depth=4
)

# =========================
# TRAIN MODEL
# =========================

model.fit(X_train, y_train)

# =========================
# DỰ ĐOÁN
# =========================

y_pred = model.predict(X_test)

# =========================
# ĐỘ CHÍNH XÁC
# =========================

acc = accuracy_score(
    y_test,
    y_pred
)

print("\n===== KẾT QUẢ =====")

print("Accuracy:", acc)

# =========================
# THỐNG KÊ
# =========================

fraud_count = data['Class'].sum()

total_transactions = len(data)

normal_count = total_transactions - fraud_count

print("Tổng giao dịch:", total_transactions)

print("Giao dịch bình thường:", normal_count)

print("Giao dịch gian lận:", fraud_count)

# =========================
# BIỂU ĐỒ
# =========================

normal = data[
    data['Class'] == 0
]

fraud = data[
    data['Class'] == 1
]

plt.scatter(
    normal['Time'],
    normal['Amount'],
    label='Normal Transaction',
    alpha=0.5
)

plt.scatter(
    fraud['Time'],
    fraud['Amount'],
    label='Fraud Transaction',
    alpha=0.8
)

plt.xlabel("Time")

plt.ylabel("Amount")

plt.title(
    "Fraud Detection in Accounting Transactions"
)

plt.legend()

plt.show()
print("test github")