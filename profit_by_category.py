import pandas as pd
import matplotlib.pyplot as plt
df_details = pd.read_csv('C:/Users/HP/Desktop/My_Chart/Details.csv')
df_orders = pd.read_csv('C:/Users/HP/Desktop/My_Chart/Orders.csv')
df_merged = pd.merge(df_details, df_orders, on="Order ID")
df_online_sales = pd.read_csv('C:/Users/HP/Desktop/My_Chart/onlinesales_sorted.csv')

category_profit = df_online_sales.groupby('Category')['Profit'].sum()  # Nhóm theo danh mục sản phẩm và tính tổng lợi nhuận
category_profit.plot(kind='bar', color='skyblue')  # Vẽ biểu đồ cột cho lợi nhuận theo danh mục sản phẩm
plt.title('Profitability by Product Category')  # Thêm tiêu đề cho biểu đồ
plt.xlabel('Category') 
plt.ylabel('Total Profit')
plt.xticks(rotation=0, ha='center')  # Xoay nhãn trục x để dễ nhìn hơn
plt.show()  # Hiển thị biểu đồ