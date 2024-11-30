import pandas as pd

# Đọc dữ liệu từ các file CSV
df_filter_data = pd.read_csv("filter_data.csv")

def sort_file():
    
    # Tạo menu lựa chọn cột để sắp xếp
    print("Columns can be rearranged:")
    print("1. Order ID")
    print("2. Amount")
    print("3. Profit")
    print("4. Quantity")
    print("5. Category")
    print("6. Sub-Category")
    print("7. PaymentMode")
    print("8. Order Date")
    print("9. CustomerName")
    print("10. State")
    print("11. City")

    select = int(input("Choose a column to sort (enter number): "))

    column_name = df_filter_data.columns[select - 1]
    sorted_df = df_filter_data.sort_values(by=column_name)
    sorted_df.to_csv("filter_data.csv", index=False)
    print(sorted_df)

    