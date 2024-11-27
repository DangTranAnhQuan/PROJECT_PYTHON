import pandas as pd
from datetime import datetime

# Tạo một dòng dữ liệu mới về đơn hàng
def create_new_data():
    # Nhập dữ liệu từ người dùng
    order_id = input("Enter Order ID: ")
    while True:
        try:
            amount = int(input("Enter the amount (Amount): "))
            break  # Thoát khỏi vòng lặp khi nhập hợp lệ
        except ValueError:
            print("Invalid input for amount. Please enter a valid number.") 
    while True:
        try:
            profit = int(input("Enter the profit (Profit): "))
            break
        except ValueError:
            print("Invalid input for profit. Please enter a valid number.")

    while True:
        try:
            quantity = int(input("Enter quantity (Quantity): "))
            break
        except ValueError:
            print("Invalid input for quantity. Please enter a valid number.")
    category = input("Enter catalog category (Category): ")
    sub_category = input("Enter Sub-Category (Sub-Category): ")
    payment_mode = input("Enter a payment method (PaymentMode): ")
    while True:
        order_date = input("Enter Order Date (dd-mm-yyyy): ")
        try:
            # Kiểm tra định dạng ngày tháng
            datetime.strptime(order_date, "%d-%m-%Y")
            break  
        except ValueError:
            print("Invalid date format. Please enter the date in dd-mm-yyyy format.")

    customer_name = input("Enter Customer Name: ")
    state = input("Enter State: ")
    city = input("Enter City: ")

    # Tạo dữ liệu mới dưới dạng dictionary
    new_data = {
        "Order ID": order_id,
        "Amount": amount,
        "Profit": profit,
        "Quantity": quantity,
        "Category": category,
        "Sub-Category": sub_category,
        "PaymentMode": payment_mode,
        "Order Date": order_date,
        "CustomerName": customer_name,
        "State": state,
        "City": city
    }

    return new_data

# Tạo dữ liệu mới và lưu vào DataFrame
new_data = create_new_data()
df = pd.DataFrame([new_data])

# Lưu vào file CSV
df.to_csv('onlinesales_sorted.csv',mode='a', header=False, index=False)

print("New data has been created and saved to the file.")

