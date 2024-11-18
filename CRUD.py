import pandas as pd
# Đọc tệp CSV
df_details = pd.read_csv("Details.csv")
df_orders = pd.read_csv("Orders.csv")

#Tham gia DataFrames dựa trên cột "ID đơn hàng"
df_merged = pd.merge(df_details, df_orders, on="Order ID")

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
                filtered_data.loc[row, 'Amount'] = int(input('Amount: '))
                filtered_data.loc[row, 'Profit'] = int(input('Profit: '))
                filtered_data.loc[row, 'Quantity'] = int(input('Quantity: '))
                filtered_data.loc[row, 'Category'] = input('Category: ')
                filtered_data.loc[row, 'Sub-Category'] = input('Sub-Category: ')
                filtered_data.loc[row, 'PaymentMode'] = input('PaymentMode: ')
                filtered_data.loc[row, 'Order Date'] = input('Order Date: ')
                filtered_data.loc[row, 'CustomerName'] = input('CustomerName: ')
                filtered_data.loc[row, 'State'] = input('State: ')
                filtered_data.loc[row, 'City'] = input('City: ')

                print('Information updated successfully')
                df_merged[df_merged['Order ID'] == ID] = filtered_data
                df_merged.to_csv('onlinesales_sorted.csv')
            else:
                print('Invalid row')
    except:
        print('Data type error')



def Delete():
    def delete_row_by_over_id(file_path, order_id):
        try:
            df = pd.read_csv(f"{file_path}")
            df_filtered = df[df['Order ID']!= order_id ]
            df_filtered.to_csv(f"{file_path}", index = False)
            if(len(df) > len(df_filtered)):
                print(f"The row with Order ID = {order_id} has been deleted")
            else:
                print(f"The row with Order ID = {order_id} does not exist")
        except KeyError:
            print(f"Column {order_id} does not exist in {file_path}.")
        except ValueError:
            print("An error occurred.")
    def execute():
        try:
            print('1.Delete row in Orders.csv by Order ID')
            print('2.Delete row in Details.csv by Order ID')
            print('3.Delete row in onlinesales_sorted.csv by Order ID')
            print('Enter selection')
            selection = int(input())
            order_id = input("Enter Order ID: ")
            if selection == 1:
                df_orders = delete_row_by_over_id('Orders.csv',order_id)
            elif selection == 2:
                df_details = delete_row_by_over_id('Details.csv',order_id)
            elif selection == 3:
                df_merged = delete_row_by_over_id('onlinesales_sorted.csv',order_id)
            else:
                print("Error! Please enter a valid number for the method.")
        except ValueError:
            print("Error! Please enter a valid number for the method.")
            
            
    execute()



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
