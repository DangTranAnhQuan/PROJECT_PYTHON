import pandas as pd
from datetime import datetime

df_merged = pd.read_csv("onlinesales_sorted.csv")

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
    df = pd.DataFrame([new_data])
    # Lưu vào file CSV
    df.to_csv('onlinesales_sorted.csv',mode='a', header=False, index=False)

    print("New data has been created and saved to the file.")



def update():
    try:
        ID = input("Enter Order ID for update: ")
        filtered_data = df_merged[df_merged['Order ID'] == ID]
        if filtered_data.empty:
            print("ID not found")
        else:
            print(filtered_data)

            row = int(input('Select the row to update: '))
            if row in filtered_data.index:
                print(f'Enter the information for the row {row}')
                for col in df_merged.columns:
                    if col != "Order ID":    
                        if col == "Amount" or col == "Profit" or col == "Quantity":
                            df_merged.loc[row, col] = int(input(f'{col}: '))
                        else:
                            df_merged.loc[row, col] = input(f'{col}: ')

                print('Information updated successfully')
                df_merged.to_csv('onlinesales_sorted.csv', index = False)
            else:
                print('Invalid row')
    except:
        print('Error')


def Delete():
    try:
        ID = input("Enter Order ID for delete: ")
        filtered_data = df_merged[df_merged['Order ID'] == ID]
        if filtered_data.empty:
            print("ID not found")
        else:
            print(filtered_data)

            row = int(input('Select the row to delete: '))
            if row in filtered_data.index:
                df_merged.drop(row, inplace = True)

                print('Deleted successfully')
                df_merged.to_csv('onlinesales_sorted.csv', index = False)
            else:
                print('Invalid row')
    except:
        print('Error')



def Search_Filter():
    while True:
        try:
            print("Choose search method")
            print("1 : Search by ID ")
            print("2 : Search by Order Date")
            print("3 : Search by State ")
            print("4 : Search by Customer Name")
            print("0 : Exit ")
            choose = int(input("Select the method: "))
            if choose==0:
                break
            elif choose == 1:
                ID = input("Enter the Order ID: ")
                df_filtered = df_merged[df_merged['Order ID'] == ID]
                if df_filtered.empty:
                    print("No data found.")
                else:
                    print("Filtered data:")
                    print(df_filtered)
            elif choose == 2:
                day = input("Enter day (dd): ")
                month = input("Enter month (mm): ")
                year = input("Enter year (yyyy): ")
                order_date = f"{day}-{month}-{year}"
                df_filtered = df_merged[df_merged['Order Date'] == order_date]
                if df_filtered.empty:
                    print("No data found.")
                else:
                    print("Filtered data:") 
                    print(df_filtered)
            elif choose == 3:
                state = input("Enter the State: ")
                df_filtered = df_merged[df_merged['State'] == state]
                if df_filtered.empty:
                    print("No data found.")
                else:
                    print("Filtered data:")
                    print(df_filtered)
            elif choose == 4:
                customer_name = input("Enter the Customer Name: ")
                df_filtered = df_merged[df_merged['CustomerName'] == customer_name]
                if df_filtered.empty:
                    print("No data found.")
                else:
                    print("Filtered data:")
                    print(df_filtered)
            else:
                print("Error! Invalid choice. Please select the method again.")
        except ValueError:
            print("Error! Please enter a valid number for the method.")


def Sort():
    def create_menu():
        print("Columns can be rearranged:")
        for i, col in enumerate(df_merged.columns):
            print(f"{i+1}. {col}")

    # Hàm sắp xếp dữ liệu
    def sort_data(column_index):
        column_name = df_merged.columns[column_index - 1]
        sorted_df = df_merged.sort_values(by=column_name)
        sorted_df.to_csv("onlinesales_sorted.csv", index=False)
        print(sorted_df)

    # Hiển thị menu và cho phép người dùng lựa chọn
    create_menu()
    choice = int(input("Choose a column to sort (enter number): "))
    sort_data(choice)


def New():
    def CreateColumn():
        # Đọc dữ liệu từ file đã ghép trước đó
        df_online_sales = pd.read_csv("onlinesales_sorted.csv")

        # Thêm cột Profit Margin
        df_online_sales['Profit Margin (%)'] = round((df_online_sales['Profit'] / df_online_sales['Amount']) * 100,2)

        # Xử lý trường hợp dữ liệu không hợp lệ (Amount = 0)
        df_online_sales['Profit Margin (%)'] = df_online_sales['Profit Margin (%)'].fillna(0)

        # Lưu lại vào file mới
        df_online_sales.to_csv("onlinesales_sorted.csv", index=False)

        print("File đã được lưu tại onlinesales_sortedn.csv")
    CreateColumn()

def filter_data():
    while True:
        try:
            print("\nChọn cột để lọc dữ liệu:")
            print("1. Amount")
            print("2. Profit")
            print("3. Quantity")
            print("0. Thoát")
            
            column_choice = int(input("Nhập số tương ứng với cột: "))
            
            if column_choice == 0:
                break
            
            columns = ["Amount", "Profit", "Quantity"]
            
            if 1 <= column_choice <= 3:
                selected_column = columns[column_choice - 1]
                
                print("\nChọn điều kiện:")
                print("1. Lớn hơn")
                print("2. Nhỏ hơn")
                print("3. Bằng")
                
                condition_choice = int(input("Nhập số tương ứng với điều kiện: "))
                
                if condition_choice not in [1, 2, 3]:
                    print("Điều kiện không hợp lệ. Vui lòng thử lại.")
                    continue
                
                if selected_column in ["Amount", "Profit", "Quantity"]:
                    value = int(input(f"Nhập giá trị so sánh cho cột {selected_column}: "))
                
                # Lọc dữ liệu
                if condition_choice == 1:  # Lớn hơn
                    filtered_data = df_merged[df_merged[selected_column] > value]
                elif condition_choice == 2:  # Nhỏ hơn
                    filtered_data = df_merged[df_merged[selected_column] < value]
                elif condition_choice == 3:  # Bằng
                    filtered_data = df_merged[df_merged[selected_column] == value]
                
                if filtered_data.empty:
                    print("Không có dữ liệu thỏa mãn điều kiện lọc.")
                else:
                    filtered_data.to_csv("filter_data.csv", index=False)
                    print(f"Dữ liệu sau khi lọc đã được lưu vào tệp 'filter_data.csv'.")
                    print("Dữ liệu sau khi lọc:")
                    print(filtered_data)
            else:
                print("Lựa chọn cột không hợp lệ. Vui lòng thử lại.")
        except ValueError:
            print("Lỗi: Vui lòng nhập số hợp lệ.")
        except Exception as e:
            print(f"Lỗi không xác định: {e}")
