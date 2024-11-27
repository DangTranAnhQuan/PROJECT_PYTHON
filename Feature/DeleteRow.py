import pandas as pd 
# Đọc các tệp CSV
df_details = pd.read_csv("Details.csv")
df_orders = pd.read_csv("Orders.csv")
df_merged = pd.merge(df_details, df_orders, on="Order ID")
df_merged.head(30)
df_sorted = df_merged.sort_values(by="Order ID")
df_sorted.head(30)
df_sorted.to_csv("onlinesales_sorted.csv", index=False)
df_online_sales = pd.read_csv("onlinesales_sorted.csv")
def deleteOneRow(file_path, order_id):
    
    try:
        df = pd.read_csv(f"{file_path}")
        amount_value = float(input("Nhập amount "))
        profit_value = float(input("Nhập Profit "))
        quantity_value = float(input("Nhập quantity "))
        category_value = input("Nhập Category ")
        sub_category_value = input("Nhập Sub-Category ")
        payment_mode_value = input("Nhập PaymentMode ")
                      
        condition = (
            (df['Order ID'] == order_id) &
            (df['Amount'] == amount_value) &
            (df['Profit'] == profit_value) &
            (df['Quantity'] == quantity_value) &
            (df['Category'] == category_value) &
            (df['Sub-Category'] == sub_category_value) &
            (df['PaymentMode'] == payment_mode_value) 
        )
        df_filtered = df[~condition]
        df_filtered.to_csv(file_path, index=False)
        if(len(df) > len(df_filtered)):
            print(f"The row has been deleted")
        else:
            print(f"The row does not exist")
    except KeyError:
        print(f"Column {order_id} does not exist in {file_path}.")
    except ValueError:
        print("An error occurred.")
def execute():
        order_id = input("Enter Order ID: ")
        deleteOneRow('onlinesales_sorted.csv',order_id)
        
execute()