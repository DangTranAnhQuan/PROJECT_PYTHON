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

# Trực quan hóa phân bố các phương thức thanh toán
def chart_paymentmode():
    plt.figure(figsize=(10, 6)) #Kích thước của bảng
    payment_mode_count = df_online_sales['PaymentMode'].value_counts() #Số lượng các phươgn thức thanh toán
    plt.bar(payment_mode_count.index, payment_mode_count.values)
    plt.title('Distribution of Payment Methods')
    plt.xlabel('Payment Method')
    plt.ylabel('Count')
    plt.grid(True, linestyle = '--', alpha = 0.5) #Thêm lưới(tùy)
    plt.show()
# Trực quan hóa phân bố doanh số theo bang
def chart_state():
    plt.figure(figsize=(12, 6))
    state_count = df_online_sales['State'].value_counts()
    plt.bar(state_count.index, state_count.values, width = 0.6)
    plt.title('Distribution of Sales by State')
    plt.xlabel('State')
    plt.ylabel('Number of Transactions')
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.3) #Điều chỉnh khảng trống ở dưới biểu đồ
    plt.show()