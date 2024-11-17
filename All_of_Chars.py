import pandas as pd
import matplotlib.pyplot as plt
# Đọc các tệp CSV
df_details = pd.read_csv("Details.csv")
df_orders = pd.read_csv("Orders.csv")
df_merged = pd.merge(df_details, df_orders, on="Order ID")
df_merged.head(30)
df_sorted = df_merged.sort_values(by="Order ID")
df_sorted.head(30)
df_sorted.to_csv("onlinesales_sorted.csv", index=False)
df_online_sales = pd.read_csv("onlinesales_sorted.csv")
df_online_sales

'''Biểu đồ của Điệp'''
# Biểu đồ tần suất của biến 'Quantity' (Số lượng)
def quantity():
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.hist(df_online_sales['Quantity'], bins=20, color='lightblue', edgecolor='black')
    plt.title('Histogram of Quantity')
    plt.xlabel('Quantity')
    plt.ylabel('Frequency')

    plt.subplot(1, 2, 2)
    plt.scatter(df_online_sales.index, df_online_sales['Quantity'], color='purple', alpha=0.7)
    plt.title('Scatter Plot of Quantity vs Index')
    plt.xlabel('Index')
    plt.ylabel('Quantity')

    plt.tight_layout()
    plt.show()

# Lợi nhuận theo danh mục sản phẩm
def profit_category():
    category_profit = df_online_sales.groupby('Category')['Profit'].sum()  # Nhóm theo danh mục sản phẩm và tính tổng lợi nhuận
    category_profit.plot(kind='bar', color='skyblue')  # Vẽ biểu đồ cột cho lợi nhuận theo danh mục sản phẩm
    plt.title('Profitability by Product Category')  # Thêm tiêu đề cho biểu đồ
    plt.xlabel('Category')  # Nhãn cho trục x
    plt.ylabel('Total Profit')  # Nhãn cho trục y
    plt.xticks(rotation=45, ha='right')  # Xoay nhãn trục x để dễ nhìn hơn
    plt.show()  # Hiển thị biểu đồ

# Lợi nhuận theo phụ danh mục sản phẩm
def profit_subcategory():
    subcategory_profit = df_online_sales.groupby('Sub-Category')['Profit'].sum()  # Nhóm theo phụ danh mục và tính tổng lợi nhuận
    subcategory_profit.plot(kind='bar', color='lightgreen')  # Vẽ biểu đồ cột cho lợi nhuận theo phụ danh mục
    plt.title('Profitability by Product Subcategory')  # Thêm tiêu đề cho biểu đồ
    plt.xlabel('Subcategory')  # Nhãn cho trục x
    plt.ylabel('Total Profit')  # Nhãn cho trục y
    plt.xticks(rotation=45, ha='right')  # Xoay nhãn trục x để dễ nhìn hơn
    plt.show()  # Hiển thị biểu đồ

# Lợi nhuận theo phương thức thanh toán
def profit_paymenntmethod():
    payment_profit = df_online_sales.groupby('PaymentMode')['Profit'].sum()  # Nhóm theo phương thức thanh toán và tính tổng lợi nhuận
    payment_profit.plot(kind='bar', color='salmon')  # Vẽ biểu đồ cột cho lợi nhuận theo phương thức thanh toán
    plt.title('Profitability by Payment Method')  # Thêm tiêu đề cho biểu đồ
    plt.xlabel('Payment Method')  # Nhãn cho trục x
    plt.ylabel('Total Profit')  # Nhãn cho trục y
    plt.xticks(rotation=45, ha='right')  # Xoay nhãn trục x để dễ nhìn hơn
    plt.show()  # Hiển thị biểu đồ

# # Phân nhóm khách hàng theo thành phố
# customer_segmentation = df_online_sales.groupby('City')

# # Phân tích hành vi mua sắm của mỗi nhóm
# for city, data in customer_segmentation:
#     print(f"Purchase Behavior in {city}:")  # Phân tích hành vi mua sắm tại thành phố
#     print("Number of Purchases:", data.shape[0])  # Số lượng đơn hàng đã thực hiện tại thành phố
#     print("Average Spending per Purchase:", data['Amount'].mean())  # Chi tiêu trung bình cho mỗi đơn hàng tại thành phố
#     print("Most Purchased Products:")  # Các sản phẩm được mua nhiều nhất
#     print(data['Sub-Category'].value_counts().head(3))  # Những nhóm sản phẩm phổ biến nhất trong thành phố
#     print()  # In một dòng trống để phân biệt giữa các thành phố



'''Biểu đồ của Thiên'''
# Trực quan hóa phân bố các phương thức thanh toán
def paymentmode():
    plt.figure(figsize=(10, 6)) #Kích thước của bảng
    payment_mode_count = df_online_sales['PaymentMode'].value_counts() #Số lượng các phươgn thức thanh toán
    plt.bar(payment_mode_count.index, payment_mode_count.values)
    plt.title('Distribution of Payment Methods')
    plt.xlabel('Payment Method')
    plt.ylabel('Count')
    plt.grid(True, linestyle = '--', alpha = 0.5) #Thêm lưới(tùy)
    plt.show()
# Trực quan hóa phân bố doanh số theo bang
def state():
    plt.figure(figsize=(12, 6))
    state_count = df_online_sales['State'].value_counts()
    plt.bar(state_count.index, state_count.values, width = 0.6)
    plt.title('Distribution of Sales by State')
    plt.xlabel('State')
    plt.ylabel('Number of Transactions')
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.3) #Điều chỉnh khảng trống ở dưới biểu đồ
    plt.show()


# '''Biểu đồ của Duy'''
def sale_trend():
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
def amount():
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

def profit():

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





# # '''Biểu đồ của Phú'''
# print("\nInformation general del DataFrame:")
# print(df_online_sales.info())


# # # Tổng hợp dữ liệu
# total_sales = df_online_sales['Amount'].sum()
# total_profit = df_online_sales['Profit'].sum()
# total_customers = df_online_sales['CustomerName'].nunique()
# total_oders = len(df_online_sales)


# # # Tổng doanh số (Total Sales)
# fig, ax = plt.subplots(2,2, figsize = (12,8))
# ax[0,0].bar('Total Sales' , total_sales, color = 'blue')
# ax[0,0].text('Total Sales', total_sales, str(total_sales), ha = 'center', va = 'bottom',fontsize = 10 ) 
# ax[0,0].set_ylabel('Amount')
# ax[0,0].set_title('Total Sales')

# # # Tổng lợi nhuận (Total Profitability)
# ax[0,1].bar('Total profitability', total_profit, color = 'green')
# ax[0,1].text('Total profitability', total_profit,str(total_profit), ha = 'center', va = 'bottom', fontsize = 10)
# ax[0,1].set_ylabel('Amount')
# ax[0,1].set_title('Total profitability')


# # #Số khách hàng duy nhất (Total Customers)
# ax[1,0].bar('Total customers', total_customers, color='orange')
# ax[1,0].text('Total customers', total_customers, str(total_customers), ha='center', va='bottom')
# ax[1,0].set_ylabel('Amount')  
# ax[1,0].set_title('Total customers')

# # #Số đơn hàng hoàn thành (Completed Sales)
# ax[1,1].bar('Completed Sales', total_oders, color = 'red' )
# ax[1,1].text('Completed Sales', total_oders, str(total_oders), ha = 'center', va = 'bottom', fontsize = 10)
# ax[1,1].set_ylabel('Amount')
# ax[1,1].set_title('Completed Sales')

# # # Điều chỉnh khoảng cách giữa các biểu đồ và hiển thị chúng.
# plt.tight_layout()
# plt.show()

# # # Đếm số lượng giao dịch theo thành phố và phương thức thanh toán, sau đó tìm phương thức phổ biến nhất ở mỗi thành phố.
# city_payment_counts = df_online_sales.groupby(['City', 'PaymentMode']).size().reset_index(name = 'Count')
# city_most_common_payment = city_payment_counts.loc[city_payment_counts.groupby('City')['Count'].idxmax()]
# print(city_most_common_payment)

# # Lọc dữ liệu về giao dịch thuộc danh mục "Clothing" và đếm số lượng giao dịch theo từng phương thức thanh toán.
# clothing_transactions = df_online_sales[df_online_sales['Category'] == 'Clothing']
# payment_mode_counts = clothing_transactions['PaymentMode'].value_counts()
# print(payment_mode_counts)

# # Nhóm và vẽ biểu đồ đường về số lượng mua hàng theo danh mục và từng tháng trong năm.

# sales_by_month_category = df_online_sales.groupby([df_online_sales['Order Date'].dt.month, 'Category']).size().unstack()

# sales_by_month_category.plot(kind='line', marker='o', figsize=(10, 6))
# plt.title('Number of Purchases by Category and Months')
# plt.xlabel('Months')
# plt.ylabel('Number of Purchases ')
# plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
# plt.legend(title='Categoría')
# plt.grid(True)
# plt.show()








