import pandas as pd

# Tạo một dòng dữ liệu mới về đơn hàng
def create_new_data():
    # Nhập dữ liệu từ người dùng
    order_id = input("Enter Order ID: ")
    amount = float(input("Enter the amount (Amount): "))
    profit = float(input("Enter the profit (Profit): "))
    quantity = int(input("Enter quantity (Quantity): "))
    category = input("Enter catalog category (Category): ")
    sub_category = input("Enter Sub-Category (Sub-Category): ")
    payment_mode = input("Enter a payment method (PaymentMode): ")

    # Nhập thêm thông tin bổ sung
    order_date = input("Enter Order Date (dd/mm/yyyy): ")
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

