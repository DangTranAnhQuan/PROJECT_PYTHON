import pandas as pd

# Đọc tệp CSV
df_details = pd.read_csv("Details.csv")
df_orders = pd.read_csv("Orders.csv")

#Tham gia DataFrames dựa trên cột "ID đơn hàng"
df_merged = pd.merge(df_details, df_orders, on="Order ID")
     
df_merged.head(30)
# Sắp xếp cột "ID đơn hàng" từ nhỏ nhất đến lớn nhất
df_sorted = df_merged.sort_values(by="Order ID")

df_sorted.head(30)
     
# Lưu dữ liệu đã cập nhật vào tệp CSV mới
df_sorted.to_csv("onlinesales_sorted.csv", index=False)
     
df_online_sales = pd.read_csv("onlinesales_sorted.csv")
     
df_online_sales

# Tổng quan về khung dữ liệu
print("\nDataFrame Overview:")
print(df_online_sales.info())

# Tóm tắt thống kê DataFrame
print("\nDataFrame Statistical Summary:")
print(df_online_sales.describe())

# Phân tích các biến phân loại
print("\nAnalysis of categorical variables:")
print("Category:")
print(df_online_sales['Category'].value_counts())
print("\nSub-Category:")
print(df_online_sales['Sub-Category'].value_counts())
print("\nPayment Method:")
print(df_online_sales['PaymentMode'].value_counts())
print("\nState:")
print(df_online_sales['State'].value_counts())
print("\nCity:")
print(df_online_sales['City'].value_counts())

# Số lượng tiểu bang
num_states = df_online_sales['State'].nunique()
print("Number of states:", num_states)

# Số lượng thành phố
num_cities = df_online_sales['City'].nunique()
print("Number of cities:", num_cities)
