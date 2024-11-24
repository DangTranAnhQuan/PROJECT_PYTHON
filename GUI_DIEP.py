import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import numpy as np
from datetime import datetime

# Đọc và chuẩn bị dữ liệu
def load_data():
        # Nếu không tồn tại, thực hiện merge từ các file gốc và lưu kết quả
        df_details = pd.read_csv("Details.csv")
        df_orders = pd.read_csv("Orders.csv")
        df_merged = pd.merge(df_details, df_orders, on="Order ID")
        df_sorted = df_merged.sort_values(by="Order ID")
        df_sorted.to_csv("onlinesales_sorted.csv", index=False)
        df_online_sales = pd.read_csv("onlinesales_sorted.csv")
        df_online_sales = df_sorted

        return df_online_sales

df = load_data()
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y')
# Biến toàn cục
current_page = 0
items_per_page = 20

# Phân trang
def get_num_pages():
    return (len(df) - 1) // items_per_page + 1

def display_data(page=0):
    global current_page
    num_pages = get_num_pages()
    if page < 0 or page >= num_pages:
        messagebox.showwarning("Cảnh báo", "Số trang không hợp lệ!")
        return
    current_page = page
    start_idx = page * items_per_page
    end_idx = min(start_idx + items_per_page, len(df))
    df_page = df.iloc[start_idx:end_idx]

    if items_per_page <= 30: 
        tree.config(height = items_per_page)
    else: 
        tree.config(height = 20)


    # Xóa dữ liệu cũ trong tree
    for row in tree.get_children():
        tree.delete(row)
    
    # Thêm dữ liệu mới vào tree
    for _, row in df_page.iterrows():
        tree.insert("", tk.END, values=list(row))
    
    # Cập nhật thông tin trang
    label_page_info.config(text=f"Trang {current_page + 1} / {num_pages}")
    entry_page.delete(0, tk.END)
    entry_page.insert(0, str(current_page + 1))
# Kiểm tra ngày tháng hợp lệ
def validate_date(date_str):
    try:
        parts = []
        # Chuyển đổi ngày thành định dạng dd-mm-yyyy nếu cần
        if date_str.find(" ") != -1:
            date_str = date_str[:date_str.find(" ")]            
        parts = date_str.split("-")
        
        if len(parts) == 3:
            if len(parts[0]) == 4:
                date_str = f"{parts[2]}-{parts[1]}-{parts[0]}"
            else:
                date_str = f"{parts[0]}-{parts[1]}-{parts[2]}"
        # Kiểm tra định dạng chuẩn dd-mm-yyyy
        datetime.strptime(date_str, "%d-%m-%Y")
        return True, date_str
    except ValueError:
        return False, date_str
    
def is_valid_number(value):
    try:
        a = int(value)  # Kiểm tra xem giá trị có phải là số không
        if float(value) == a:
            return True
        else:
            return False
    except ValueError:
        return False

def create_new_data():
    # Tạo cửa sổ nhập liệu cho dữ liệu mới
    update_window = tk.Toplevel(root)
    update_window.title("Thêm dữ liệu mới")

    # Tạo các ô nhập liệu cho từng cột trong DataFrame
    entry_fields = {}
    for i, column in enumerate(df.columns):
        tk.Label(update_window, text=column).grid(row=i, column=0)
        entry = tk.Entry(update_window)
        entry.grid(row=i, column=1)
        entry_fields[column] = entry
    # Hàm lưu dữ liệu mới
    def save_new_data():
        global df
        try:
            # Lấy dữ liệu mới từ các ô nhập liệu
            new_data = {column: entry.get() for column, entry in entry_fields.items()}
            
            for column, value in new_data.items():
                if not value:  # Nếu giá trị cột đó trống
                    messagebox.showerror("Lỗi", f"Cột '{column}' không được bỏ trống!")
                    return
                
            check_date, new_data["Order Date"] = validate_date(new_data["Order Date"])
            
            if 'Order Date' in new_data:
                if not check_date:
                    messagebox.showerror("Lỗi", "Ngày tháng không hợp lệ! Định dạng: dd-mm-yyyy")
                    return 
            for col in ["Amount", "Profit", "Quantity"]:
                if col in new_data and not is_valid_number(new_data[col]):
                    messagebox.showerror("Lỗi", f"{col} phải là số nguyên hợp lệ!")
                    return
            
            # Tạo một dòng dữ liệu mới dưới dạng DataFrame
            new_row_df = pd.DataFrame([new_data])
            new_row_df['Order Date'] = pd.to_datetime(new_row_df['Order Date'], format='%d-%m-%Y')

            # Thêm dữ liệu mới vào DataFrame chính
            df = pd.concat([df, new_row_df], ignore_index=True)

            df[['Amount', 'Profit', 'Quantity']] = df[['Amount', 'Profit', 'Quantity']].astype(int)

            # Ghi toàn bộ dữ liệu mới vào tệp CSV
            df.to_csv("onlinesales_sorted.csv", index=False)
        
            # Cập nhật giao diện hiển thị
            display_data(current_page)  
        
            # Đóng cửa sổ thêm dữ liệu
            update_window.destroy()
            messagebox.showinfo("Thông báo", "Thêm dữ liệu thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")


    # Tạo nút "Lưu" để lưu dữ liệu
    tk.Button(update_window, text="Lưu", command=save_new_data).grid(row=len(df.columns), columnspan=2)



def update_data():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Chọn dòng", "Vui lòng chọn một dòng để cập nhật")
        return

    # Lấy ID dòng được chọn trong Treeview
    item_id = selected_item[0]
    values = tree.item(item_id)['values']
    
    try:
        # Tìm dòng trong DataFrame (giả sử 'Order ID' là cột đầu tiên)
        item_id_value = str(values[0])  # Cột 'Order ID'
        category_value = str(values[4])  # Cột 'Category'
        amount_value = values[1]
        profit_value = values[2]
        quantity_value = values[3]
        sub_category_value = str(values[5])  # Cột 'Sub-Category'
        payment_mode_value = str(values[6])  # Cột 'PaymentMode'
        order_date_value = values[7]
        customer_name_value = str(values[8])  # Cột 'CustomerName'
        state_value = str(values[9])  # Cột 'State'
        city_value = str(values[10])  # Cột 'City'

        # Lọc DataFrame theo các cột cụ thể
        filtered_df = df[
            (df['Order ID'] == item_id_value) &
            (df['Amount'] == amount_value) &
            (df['Profit'] == profit_value) &
            (df['Quantity'] == quantity_value) &
            (df['Category'] == category_value) &
            (df['Sub-Category'] == sub_category_value) &
            (df['PaymentMode'] == payment_mode_value) &
            (df['Order Date'] == order_date_value) &
            (df['CustomerName'] == customer_name_value) &
            (df['State'] == state_value) &
            (df['City'] == city_value)
        ]
        
        if filtered_df.empty:
            messagebox.showwarning("Không tìm thấy", "Không tìm thấy dữ liệu có Order ID tương ứng để cập nhật.")
            return
        index = filtered_df.index[0]  # Lấy chỉ số dòng cần cập nhật

        # Mở cửa sổ cập nhật dữ liệu
        update_window = tk.Toplevel(root)
        update_window.title("Cập nhật dữ liệu")

        entry_fields = {}
        for i, column in enumerate(df.columns):
            tk.Label(update_window, text=column).grid(row=i, column=0)
            entry = tk.Entry(update_window)
            entry.insert(0, values[i])  # Gán giá trị ban đầu vào ô nhập
            entry.grid(row=i, column=1)
            entry_fields[column] = entry

        def save_update():
            global df
            try:
                res = messagebox.askyesno('Cập nhật dữ liệu','Bạn có chắc chắn muốn lưu chỉnh sửa không ?')
                if res:
                    # Lấy dữ liệu cập nhật từ các ô nhập
                    updated_data = {column: entry.get() for column, entry in entry_fields.items()}

                    for column, value in updated_data.items():
                        if not value:  # Nếu giá trị cột đó trống
                            messagebox.showerror("Lỗi", f"Cột '{column}' không được bỏ trống!")
                            return
                    
                    check_date, updated_data["Order Date"] = validate_date(updated_data["Order Date"])

                    if 'Order Date' in updated_data:
                        if not check_date:
                            messagebox.showerror("Lỗi", "Ngày tháng không hợp lệ! Định dạng: dd-mm-yyyy")
                            return
                    
                    for col in ["Amount", "Profit", "Quantity"]:
                        if col in updated_data and not is_valid_number(updated_data[col]):
                            messagebox.showerror("Lỗi", f"{col} phải là số nguyên hợp lệ!")
                            return
                    
                    # Cập nhật dữ liệu trong DataFrame
                    for column, value in updated_data.items():
                        if column == 'Order Date':
                            df.at[index, column] = pd.to_datetime(value, format = "%d-%m-%Y")
                        elif column in ('Amount', 'Profit', 'Quantity'):
                            df.at[index, column] = int(value)
                        else:
                            df.at[index, column] = value
                    
                    # Lưu lại DataFrame vào file CSV
                    df.to_csv("onlinesales_sorted.csv", index=False)    
                    
                    # Cập nhật Treeview hiển thị
                    tree.item(item_id, values=list(df.loc[index]))
                    display_data(current_page) 
                    
                    # Đóng cửa sổ cập nhật
                    update_window.destroy()
                    messagebox.showinfo("Thông báo", "Cập nhật dữ liệu thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

        # Nút lưu
        tk.Button(update_window, text="Lưu", command=save_update).grid(row=len(df.columns), columnspan=2)

    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")


# Tạo giao diện chính
root = tk.Tk()
root.title("Quản lý dữ liệu")

tree = ttk.Treeview(root, columns=list(df.columns), show="headings")
for col in df.columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor="w")
tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Khung điều khiển
frame_controls = tk.Frame(root)
frame_controls.pack(pady=10)

# Nút chức năng
tk.Button(frame_controls, text="Tạo dữ liệu mới", command=create_new_data).pack(side=tk.LEFT, padx=5)
tk.Button(frame_controls, text="Cập nhật dữ liệu", command=update_data).pack(side=tk.LEFT, padx=5)

# Phân trang
frame_pagination = tk.Frame(root)
frame_pagination.pack(pady=10)

def go_to_page():
    try:
        page = int(entry_page.get()) - 1
        display_data(page)
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập một số hợp lệ!")

def go_to_previous_page():
    if current_page > 0:
        display_data(page=current_page - 1)

def go_to_next_page():
    if current_page < get_num_pages() - 1:
        display_data(page=current_page + 1)

tk.Button(frame_pagination, text="<< Trước", command=go_to_previous_page).pack(side=tk.LEFT, padx=10)
entry_page = tk.Entry(frame_pagination, width=5, justify='center')
entry_page.insert(0, "1")
entry_page.pack(side=tk.LEFT)
entry_page.bind("<Return>", lambda event: go_to_page())
tk.Button(frame_pagination, text="Sau >>", command=go_to_next_page).pack(side=tk.LEFT, padx=10)
label_page_info = tk.Label(frame_pagination, text="")
label_page_info.pack(side=tk.LEFT, padx=10)

# Hiển thị dữ liệu trang đầu tiên
display_data(0)

root.mainloop()