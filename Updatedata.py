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
                df_online_sales.loc[row, 'Amount'] = int(input('Amount: '))
                df_online_sales.loc[row, 'Profit'] = int(input('Profit: '))
                df_online_sales.loc[row, 'Quantity'] = int(input('Quantity: '))
                df_online_sales.loc[row, 'Category'] = input('Category: ')
                df_online_sales.loc[row, 'Sub-Category'] = input('Sub-Category: ')
                df_online_sales.loc[row, 'PaymentMode'] = input('PaymentMode: ')
                df_online_sales.loc[row, 'Order Date'] = input('Order Date: ')
                df_online_sales.loc[row, 'CustomerName'] = input('CustomerName: ')
                df_online_sales.loc[row, 'State'] = input('State: ')
                df_online_sales.loc[row, 'City'] = input('City: ')

                print('Information updated successfully')
                df_online_sales.to_csv('onlinesales_sorted.csv', index = False)
            else:
                print('Invalid row')
    except:
        print('Error')
update()