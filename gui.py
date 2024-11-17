import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import numpy as np

# Đọc và chuẩn bị dữ liệu
def load_data():
        # Nếu không tồn tại, thực hiện merge từ các file gốc và lưu kết quả
        df_details = pd.read_csv("Details.csv")
        df_orders = pd.read_csv("Orders.csv")
        df_merged = pd.merge(df_details, df_orders, on="Order ID")
        df_sorted = df_merged.sort_values(by="Order ID")
        df_sorted.to_csv("onlinesales_sorted.csv", index=False)
        df_online_sales = pd.read_csv("onlinesales_sorted.csv")
        df_online_sales['Order Date'] = pd.to_datetime(df_online_sales['Order Date'], format='%d-%m-%Y')
        df_online_sales = df_sorted

        return df_online_sales

df = load_data()

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
    # Hàm lưu dữ liệu mới
    def save_new_data():
        global df
        try:
            # Lấy dữ liệu mới từ các ô nhập liệu
            new_data = {column: entry.get() for column, entry in entry_fields.items()}
        
            # Tạo một dòng dữ liệu mới dưới dạng DataFrame
            new_row_df = pd.DataFrame([new_data])
        
            # Thêm dữ liệu mới vào DataFrame chính
            df = pd.concat([df, new_row_df], ignore_index=True)
    
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
        item_id_value = str(values[0])
        filtered_df = df[df['Order ID'] == item_id_value]

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
                # Lấy dữ liệu cập nhật từ các ô nhập
                updated_data = {column: entry.get() for column, entry in entry_fields.items()}

                # Cập nhật dữ liệu trong DataFrame
                for column, entry in entry_fields.items():
                    value = entry.get()
                    if pd.api.types.is_numeric_dtype(df[column]):
                        value = pd.to_numeric(value, errors='coerce')  # Chuyển đổi giá trị sang kiểu số nếu cần
                    df.at[index, column] = value

                # Lưu lại DataFrame vào file CSV
                df.to_csv("onlinesales_sorted.csv", index=False)

                # Cập nhật Treeview hiển thị
                tree.item(item_id, values=list(df.loc[index]))
                
                # Đóng cửa sổ cập nhật
                update_window.destroy()
                messagebox.showinfo("Thông báo", "Cập nhật dữ liệu thành công!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

        # Nút lưu
        tk.Button(update_window, text="Lưu", command=save_update).grid(row=len(df.columns), columnspan=2)

    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

def delete_data():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Chọn dòng", "Vui lòng chọn một dòng để xóa")
        return

    item_id = selected_item[0]
    values = tree.item(item_id)['values']

    try:
        # Lấy chỉ số dòng từ Treeview
        item_index = df.index[df['Order ID'] == str(values[0])].tolist()
        if not item_index:
            messagebox.showwarning("Không tìm thấy", "Không tìm thấy dòng để xóa.")
            return

        # Xóa dòng trong DataFrame
        df.drop(item_index[0], inplace=True)

        # Lưu lại DataFrame vào file CSV
        df.to_csv("onlinesales_sorted.csv", index=False)

        # Cập nhật Treeview
        tree.delete(item_id)
        messagebox.showinfo("Thông báo", "Dữ liệu đã được xóa thành công!")

    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")


# Tìm kiếm dữ liệu
def search_data():
    search_term = simpledialog.askstring("Tìm kiếm", "Nhập từ khóa tìm kiếm:")
    if search_term:
        filtered_df = df[df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().values, axis=1)]
        if filtered_df.empty:
            messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy dữ liệu phù hợp.")
        else:
            display_filtered_data(filtered_df)

def display_filtered_data(filtered_df):
    for row in tree.get_children():
        tree.delete(row)
    
    for _, row in filtered_df.iterrows():
        tree.insert("", tk.END, values=list(row))

# Sắp xếp
def sort_data(): 
    def sort(column_index):
        global df
        column_name = df.columns[column_index]

        # Trường hợp đặc biệt khi sắp xếp theo cột "Amount"
        if column_name == "Amount" or column_name == "Profit" or column_name == "Quantity":
            # Chuyển tất cả các giá trị trong cột Amount thành chuỗi
            df[column_name] = df[column_name].astype(int)

        # Sắp xếp dữ liệu theo cột đã chọn
        df = df.sort_values(by=column_name)

        # Đóng cửa sổ sắp xếp
        sort_window.destroy()

        # Lưu dữ liệu đã sắp xếp vào file CSV
        df.to_csv("onlinesales_sorted.csv", index=False)

        # Cập nhật giao diện
        display_data(current_page)

        # Thông báo thành công
        messagebox.showinfo("Thông báo", "Sắp xếp dữ liệu thành công!")

    # Tạo cửa sổ phụ (Toplevel) để chứa các nút sắp xếp
    sort_window = tk.Toplevel(root)
    sort_window.title("Sắp xếp dữ liệu bán hàng trực tuyến")
    sort_window.config(height=10)

    # Tạo frame để chứa các nút sắp xếp
    frame_sort = tk.Frame(sort_window)
    frame_sort.pack(padx=10, pady=10)

    # Các nút sắp xếp
    button_width = 30
    tk.Button(frame_sort, text="Sắp xếp theo Amount", command=lambda: sort(1), width=button_width).pack(padx=5)
    tk.Button(frame_sort, text="Sắp xếp theo Profit", command=lambda: sort(2), width=button_width).pack(padx=5)
    tk.Button(frame_sort, text="Sắp xếp theo Quantity", command=lambda: sort(3), width=button_width).pack(padx=5)
    tk.Button(frame_sort, text="Sắp xếp theo Category", command=lambda: sort(4), width=button_width).pack(padx=5)
    tk.Button(frame_sort, text="Sắp xếp theo Sub-Category", command=lambda: sort(5), width=button_width).pack(padx=5)
    tk.Button(frame_sort, text="Sắp xếp theo PaymentMode", command=lambda: sort(6), width=button_width).pack(padx=5)
    tk.Button(frame_sort, text="Sắp xếp theo Order date", command=lambda: sort(7), width=button_width).pack(padx=5)
    tk.Button(frame_sort, text="Sắp xếp theo CustomerName", command=lambda: sort(8), width=button_width).pack(padx=5)
    tk.Button(frame_sort, text="Sắp xếp theo State", command=lambda: sort(9), width=button_width).pack(padx=5)
    tk.Button(frame_sort, text="Sắp xếp theo City", command=lambda: sort(10), width=button_width).pack(padx=5)


# Vẽ biểu đồ
def chart(): 
    import All_of_Chars as chart

    # Tạo cửa sổ phụ (Toplevel) để chứa các nút sắp xếp
    chart_window = tk.Toplevel(root)
    chart_window.title("Vẽ biểu đồ dữ liệu bán hàng trực tuyến")
    chart_window.config(height = 10)

    # Tạo frame để chứa các nút sắp xếp
    frame_chart = tk.Frame(chart_window)
    frame_chart.pack(padx=10, pady=10)
       
    # Các nút vẽ biểu đồ
    button_width = 50
    tk.Button(frame_chart, text="Biểu đồ phân phối các phương thức thanh toán", command= chart.paymentmode, width=button_width).pack(padx=5)
    tk.Button(frame_chart, text="Biểu đồ phân phối số lượng giao dịch theo bang", command=chart.state, width=button_width).pack(padx=5)
    tk.Button(frame_chart, text="Biểu đồ Điệp 1", command= chart.quantity, width=button_width).pack(padx=5)
    tk.Button(frame_chart, text="Biểu đồ Điệp 2", command= chart.profit_category, width=button_width).pack(padx=5)
    tk.Button(frame_chart, text="Biểu đồ Điệp 3", command= chart.profit_subcategory, width=button_width).pack(padx=5)
    tk.Button(frame_chart, text="Biểu đồ Điệp 4", command= chart.profit_paymenntmethod, width=button_width).pack(padx=5)
    tk.Button(frame_chart, text="Biểu đồ Duy 1", command= chart.sale_trend, width=button_width).pack(padx=5)
    tk.Button(frame_chart, text="Biểu đồ Duy 2", command= chart.amount, width=button_width).pack(padx=5)
    tk.Button(frame_chart, text="Biểu đồ Duy 3", command= chart.profit, width=button_width).pack(padx=5)
    # tk.Button(frame_sort, text="Biểu đồ phân phối", command=lambda: sort(10), width=button_width).pack(padx=5)

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
tk.Button(frame_controls, text="Xóa dữ liệu", command=delete_data).pack(side=tk.LEFT, padx=5)
tk.Button(frame_controls, text="Tìm kiếm", command=search_data).pack(side=tk.LEFT, padx=5)
tk.Button(frame_controls, text="Sắp xếp", command=sort_data).pack(side=tk.LEFT, padx=5)
tk.Button(frame_controls, text="Vẽ biểu đồ", command=chart).pack(side=tk.LEFT, padx=5)

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