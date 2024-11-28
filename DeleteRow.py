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