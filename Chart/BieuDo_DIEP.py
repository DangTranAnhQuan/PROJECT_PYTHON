import pandas as pd
df_online_sales = pd.read_csv("onlinesales_sorted.csv")
import matplotlib.pyplot as plt

# Biểu đồ tần suất của biến 'Quantity' (Số lượng)
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.hist(df_online_sales['Quantity'], bins=20, color='lightblue', edgecolor='black')
plt.title('Histogram of Quantity')
plt.xlabel('Quantity')
plt.ylabel('Frequency')

# Biểu đồ phân tán 'Quantity' vs. chỉ số
plt.subplot(1, 2, 2)
plt.scatter(df_online_sales.index, df_online_sales['Quantity'], color='purple', alpha=0.7)
plt.title('Scatter Plot of Quantity vs. Index')
plt.xlabel('Index')
plt.ylabel('Quantity')

plt.tight_layout()
plt.show()

# Lợi nhuận theo danh mục sản phẩm
category_profit = df_online_sales.groupby('Category')['Profit'].sum()  # Nhóm theo danh mục sản phẩm và tính tổng lợi nhuận
category_profit.plot(kind='bar', color='skyblue')  # Vẽ biểu đồ cột cho lợi nhuận theo danh mục sản phẩm
plt.title('Profitability by Product Category')  # Thêm tiêu đề cho biểu đồ
plt.xlabel('Category')  # Nhãn cho trục x
plt.ylabel('Total Profit')  # Nhãn cho trục y
plt.xticks(rotation=45, ha='right')  # Xoay nhãn trục x để dễ nhìn hơn
plt.show()  # Hiển thị biểu đồ

# Lợi nhuận theo phụ danh mục sản phẩm
subcategory_profit = df_online_sales.groupby('Sub-Category')['Profit'].sum()  # Nhóm theo phụ danh mục và tính tổng lợi nhuận
subcategory_profit.plot(kind='bar', color='lightgreen')  # Vẽ biểu đồ cột cho lợi nhuận theo phụ danh mục
plt.title('Profitability by Product Subcategory')  # Thêm tiêu đề cho biểu đồ
plt.xlabel('Subcategory')  # Nhãn cho trục x
plt.ylabel('Total Profit')  # Nhãn cho trục y
plt.xticks(rotation=45, ha='right')  # Xoay nhãn trục x để dễ nhìn hơn
plt.show()  # Hiển thị biểu đồ

# Lợi nhuận theo phương thức thanh toán
payment_profit = df_online_sales.groupby('PaymentMode')['Profit'].sum()  # Nhóm theo phương thức thanh toán và tính tổng lợi nhuận
payment_profit.plot(kind='bar', color='salmon')  # Vẽ biểu đồ cột cho lợi nhuận theo phương thức thanh toán
plt.title('Profitability by Payment Method')  # Thêm tiêu đề cho biểu đồ
plt.xlabel('Payment Method')  # Nhãn cho trục x
plt.ylabel('Total Profit')  # Nhãn cho trục y
plt.xticks(rotation=45, ha='right')  # Xoay nhãn trục x để dễ nhìn hơn
plt.show()  # Hiển thị biểu đồ



