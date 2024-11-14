import pandas as pd
import matplotlib.pyplot as plt
df_details = pd.read_csv("Details.csv")
df_orders = pd.read_csv("Orders.csv")
df_merged = pd.merge(df_details, df_orders, on="Order ID")
df_merged.head(30)
df_sorted = df_merged.sort_values(by="Order ID")
df_sorted.head(30)
df_sorted.to_csv("onlinesales_sorted.csv",index =False)
df_online_sales = pd.read_csv("onlinesales_sorted.csv") 

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
            df_filtered = df_online_sales[df_online_sales['Order ID'] == ID]
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
            df_filtered = df_online_sales[df_online_sales['Order Date'] == order_date]
            if df_filtered.empty:
                print("No data found.")
            else:
                print("Filtered data:") 
                print(df_filtered)
        elif choose == 3:
            state = input("Enter the State: ")
            df_filtered = df_online_sales[df_online_sales['State'] == state]
            if df_filtered.empty:
                print("No data found.")
            else:
                print("Filtered data:")
                print(df_filtered)
        elif choose == 4:
            customer_name = input("Enter the Customer Name: ")
            df_filtered = df_online_sales[df_online_sales['CustomerName'] == customer_name]
            if df_filtered.empty:
                print("No data found.")
            else:
                print("Filtered data:")
                print(df_filtered)
        else:
            print("Error! Invalid choice. Please select the method again.")
    except ValueError:
        print("Error! Please enter a valid number for the method.")

        
