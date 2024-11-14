import pandas as pd
import matplotlib.pyplot as plt
df_details = pd.read_csv("Details.csv")
df_orders = pd.read_csv("Orders.csv")
df_merged = pd.merge(df_details, df_orders, on="Order ID")
df_merged.head(30)
df_sorted = df_merged.sort_values(by="Order ID")
df_sorted.head(30)
df_sorted.to_csv("onlinesales_sorted.csv",index =False)
df_online_sales = pd.read_csv("onlinesales_sorted.csv") 

df_online_sales['Order Date'] = pd.to_datetime(df_online_sales['Order Date'], format='%d-%m-%Y')
df_online_sales['Order Month'] = df_online_sales['Order Date'].dt.to_period('M')
monthly_sales = df_online_sales.groupby('Order Month')['Amount'].sum()
plt.figure(figsize=(10, 6))
monthly_sales.plot(marker='o', color='b', linestyle='-')
# biểu đồ xu hướng doanh số thay đổi theo thời gian
plt.title('Sales trend chart over time')
plt.xlabel('Month')
# tổng doanh số
plt.ylabel('Total sales')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.hist(df_online_sales['Amount'], bins=20, color='skyblue', edgecolor='black')
# Biểu đồ phân bố tần số của số lượng
plt.title('Histogram of Amount')
plt.xlabel('Amount')
# Tần suất
plt.ylabel('Frequency')
plt.subplot(1, 2, 2)
plt.scatter(df_online_sales.index, df_online_sales['Amount'], color='salmon', alpha=0.7)
# Biểu đồ phân tán số lượng so với chỉ số
plt.title('Scatter plot of amount versus index') 
plt.xlabel('Index')
plt.ylabel('Amount')
plt.tight_layout()
plt.show()



plt.figure(figsize=(10, 5))
plt.subplot(1,2,1)
plt.hist(df_online_sales['Profit'], bins=20, color='lightgreen', edgecolor='black')
plt.title('Frequency distribution chart of profit') #Biểu đồ phần bổ tần suất của lợi nhuận
plt.xlabel('Profit')
plt.ylabel('Frequency')
plt.subplot(1, 2, 2)
plt.scatter(df_online_sales.index, df_online_sales['Profit'], color='orange', alpha=0.7)
plt.title('Scatter plot of profit versus index') #Biểu đồ phân tán lợi nhuận so với chỉ số
plt.xlabel('Index')
plt.ylabel('Profit')
plt.tight_layout()
plt.show()