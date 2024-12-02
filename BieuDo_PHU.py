import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt


df_details = pd.read_csv(r"D:\Python\New\python\project\Details.csv", sep=",", header = 0)
df_orders = pd.read_csv(r"D:\Python\New\python\project\Orders.csv", sep=",", header = 0)
df_merged = pd.merge(df_details, df_orders, on = 'Order ID', how = 'left')

df_sorted = df_merged.sort_values(by="Order ID")
df_sorted.head(30)
df_merged.head(30)
df_sorted.to_csv(r"D:\Python\New\python\project\onlinesales_sorted.csv", index=False)

df_online_sales = pd.read_csv(r"D:\Python\New\python\project\onlinesales_sorted.csv")


print("\nInformation general del DataFrame:")
print(df_online_sales.info())


# # Tổng hợp dữ liệu
total_sales = df_online_sales['Amount'].sum()
total_profit = df_online_sales['Profit'].sum()
total_customers = df_online_sales['CustomerName'].nunique()
total_oders = len(df_online_sales)


# # Tổng doanh số (Total Sales)
fig, ax = plt.subplots(2,2, figsize = (12,8))
ax[0,0].bar('Total Sales' , total_sales, color = 'blue')
ax[0,0].text('Total Sales', total_sales, str(total_sales), ha = 'center', va = 'bottom',fontsize = 10 ) 
ax[0,0].set_ylabel('Amount')
ax[0,0].set_title('Total Sales')

# # Tổng lợi nhuận (Total Profitability)
ax[0,1].bar('Total profitability', total_profit, color = 'green')
ax[0,1].text('Total profitability', total_profit,str(total_profit), ha = 'center', va = 'bottom', fontsize = 10)
ax[0,1].set_ylabel('Amount')
ax[0,1].set_title('Total profitability')


# #Số khách hàng duy nhất (Total Customers)
ax[1,0].bar('Total customers', total_customers, color='orange')
ax[1,0].text('Total customers', total_customers, str(total_customers), ha='center', va='bottom')
ax[1,0].set_ylabel('Amount')  
ax[1,0].set_title('Total customers')

# #Số đơn hàng hoàn thành (Completed Sales)
ax[1,1].bar('Completed Sales', total_oders, color = 'red' )
ax[1,1].text('Completed Sales', total_oders, str(total_oders), ha = 'center', va = 'bottom', fontsize = 10)
ax[1,1].set_ylabel('Amount')
ax[1,1].set_title('Completed Sales')

# # Điều chỉnh khoảng cách giữa các biểu đồ và hiển thị chúng.
plt.tight_layout()
plt.show()

# # Đếm số lượng giao dịch theo thành phố và phương thức thanh toán, sau đó tìm phương thức phổ biến nhất ở mỗi thành phố.
city_payment_counts = df_online_sales.groupby(['City', 'PaymentMode']).size().reset_index(name = 'Count')
city_most_common_payment = city_payment_counts.loc[city_payment_counts.groupby('City')['Count'].idxmax()]
print(city_most_common_payment)

# Lọc dữ liệu về giao dịch thuộc danh mục "Clothing" và đếm số lượng giao dịch theo từng phương thức thanh toán.
clothing_transactions = df_online_sales[df_online_sales['Category'] == 'Clothing']
payment_mode_counts = clothing_transactions['PaymentMode'].value_counts()
print(payment_mode_counts)

# Nhóm và vẽ biểu đồ đường về số lượng mua hàng theo danh mục và từng tháng trong năm.

sales_by_month_category = df_online_sales.groupby([df_online_sales['Order Date'].dt.month, 'Category']).size().unstack()

sales_by_month_category.plot(kind='line', marker='o', figsize=(10, 6))
plt.title('Number of Purchases by Category and Months')
plt.xlabel('Months')
plt.ylabel('Number of Purchases ')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend(title='Category')
plt.grid(True)
plt.show()






fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))

# Vẽ đồ thị cho 10 thành phố có lợi nhuận cao nhất
city = df_online_sales.groupby('City')['Profit'].sum().reset_index()
top_10_city = city.nlargest(10, 'Profit')
ax1.bar(top_10_city['City'], top_10_city['Profit'])
ax1.set_xlabel('City')
ax1.set_ylabel('Profit')
ax1.set_title('Max Profits Generated from Top 10 Cities')

# Xoay các nhãn trục X trên ax1
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)

# Vẽ đồ thị cho 10 tiểu bang có lợi nhuận cao nhất
state = df_online_sales.groupby('State')['Profit'].sum().reset_index()
top_10_state = state.nlargest(10, 'Profit')
ax2.bar(top_10_state['State'], top_10_state['Profit'])
ax2.set_xlabel('State')
ax2.set_ylabel('Profit')
ax2.set_title('Max Profits Generated from Top 10 States')

# Xoay các nhãn trục X trên ax2
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)

plt.tight_layout()
plt.show()


# Tạo khung hình
plt.figure(figsize=(12,6))
electronics_df = df_online_sales[df_online_sales["Category"]=="Electronics"]
subcategory_sales = electronics_df.groupby("Sub-Category")["Amount"].sum().reset_index()
most_sold_products = subcategory_sales.sort_values(by="Amount",ascending=False)
#Vẽ đồ thị được bán nhiều nhất trong loại Electronic
plt.bar(most_sold_products["Sub-Category"],most_sold_products["Amount"])
plt.title("Total sales by products")
plt.xlabel("Products")
plt.ylabel("Total Sales Amount")
plt.show()










