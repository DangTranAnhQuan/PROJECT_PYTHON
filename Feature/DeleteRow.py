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
            df_online_sales = delete_row_by_over_id('onlinesales_sorted.csv',order_id)
        else:
            print("Error! Please enter a valid number for the method.")
    except ValueError:
        print("Error! Please enter a valid number for the method.")
        
        
execute()