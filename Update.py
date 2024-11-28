import pandas as pd
# Đọc các tệp CSV
df_details = pd.read_csv("Details.csv")
df_orders = pd.read_csv("Orders.csv")
df_merged = pd.merge(df_details, df_orders, on="Order ID")
df_sorted = df_merged.sort_values(by="Order ID")
df_sorted.to_csv("onlinesales_sorted.csv", index=False)
df_online_sales = pd.read_csv("onlinesales_sorted.csv")

def update():
    try:
        ID = input("Enter Order ID for update: ")
        filtered_data = df_online_sales[df_online_sales['Order ID'] == ID]
        if filtered_data.empty:
            print("ID not found")
        else:
            print(filtered_data)

            row = int(input('Select the row to update: '))
            if row in filtered_data.index:
                print(f'Enter the information for the row {row}')
                for col in df_online_sales.columns:
                    if col != "Order ID":
                        if col == "Amount" or col == "Profit" or col == "Quantity":
                            df_online_sales.loc[row, col] = int(input(f'{col}: '))
                        else:
                            df_online_sales.loc[row, col] = input(f'{col}: ')

                print('Information updated successfully')
                df_online_sales.to_csv('onlinesales_sorted.csv', index = False)
            else:
                print('Invalid row')
    except:
        print('Error')