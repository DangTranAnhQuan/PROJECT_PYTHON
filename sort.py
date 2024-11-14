import pandas as pd

# Đọc từ file đã thực hiện các thao tác thêm xóa sửa ở trên

# Đọc dữ liệu từ các file CSV
df_details = pd.read_csv("Details.csv")
df_orders = pd.read_csv("Orders.csv")

# Kết hợp hai DataFrame dựa trên cột "Order ID"
df_merged = pd.merge(df_details, df_orders, on="Order ID")

# Tạo menu lựa chọn cột để sắp xếp
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