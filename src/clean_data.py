import pandas as pd
from sklearn.preprocessing import StandardScaler

# =========================
# ĐỌC DỮ LIỆU
# =========================

data = pd.read_csv("data/creditcard.csv")

# =========================
# KIỂM TRA DỮ LIỆU
# =========================

print("===== KIỂM TRA DỮ LIỆU =====")

print("\nKích thước dữ liệu:")
print(data.shape)

print("\nThông tin dữ liệu:")
print(data.info())

print("\nDữ liệu thiếu:")
print(data.isnull().sum())

print("\nDữ liệu trùng:")
print(data.duplicated().sum())

# =========================
# XÓA DỮ LIỆU TRÙNG
# =========================

data = data.drop_duplicates()

print("\nSau khi xóa dữ liệu trùng:")
print(data.shape)

# =========================
# CHUẨN HÓA DỮ LIỆU
# =========================

scaler = StandardScaler()

data['Amount'] = scaler.fit_transform(
    data[['Amount']]
)

data['Time'] = scaler.fit_transform(
    data[['Time']]
)

print("\nĐã chuẩn hóa dữ liệu.")

# =========================
# LƯU FILE MỚI
# =========================

data.to_csv(
    "data/creditcard_clean.csv",
    index=False
)

print("\nĐã lưu file sạch:")
print("data/creditcard_clean.csv")