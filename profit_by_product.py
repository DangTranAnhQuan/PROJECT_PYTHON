import pandas as pd
import matplotlib.pyplot as plt

df_details = pd.read_csv('C:/Users/HP/Desktop/My_Chart/Details.csv')
df_orders = pd.read_csv('C:/Users/HP/Desktop/My_Chart/Orders.csv')
df_merged = pd.merge(df_details, df_orders, on="Order ID")
df_online_sales = pd.read_csv('C:/Users/HP/Desktop/My_Chart/onlinesales_sorted.csv')

plt.scatter(df_online_sales.index, df_online_sales['Profit'], color='orange', alpha=0.7)
plt.title('Scatter plot of profit by count of product') #Biểu đồ phân tán lợi nhuận so với chỉ số
plt.xlabel('Index')
plt.ylabel('Profit')
plt.tight_layout()
plt.show()