import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import numpy as np
from datetime import datetime
from tkinter import scrolledtext
def load_data():
    df_details = pd.read_csv("Details.csv")
    df_orders = pd.read_csv("Orders.csv")
    df_merged = pd.merge(df_details, df_orders, on="Order ID")
    df_sorted = df_merged.sort_values(by="Order ID")
    df_sorted.to_csv("onlinesales_sorted.csv", index=False)
    df_online_sales = pd.read_csv("onlinesales_sorted.csv")
    df_online_sales['Order Date'] = pd.to_datetime(df_online_sales['Order Date'], format='%d-%m-%Y')
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
def search_data():
    search_term = simpledialog.askstring("Tìm kiếm", "Nhập từ khóa tìm kiếm:")
    if search_term:
        filtered_df = df[df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().values, axis=1)]
        if filtered_df.empty:
            messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy dữ liệu phù hợp.")
        else:
            display_search_results(filtered_df)
            
def display_search_results(filtered_df):
   # Tạo cửa sổ mới
    new_window = tk.Toplevel()
    new_window.title("Kết quả tìm kiếm")
    
    # Tạo Frame chứa Treeview và Scrollbar
    frame = tk.Frame(new_window)
    frame.pack(fill=tk.BOTH, expand=True)

    # Tạo Scrollbar
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Tạo Treeview
    tree = ttk.Treeview(frame, yscrollcommand=scrollbar.set,height=30)
    tree.pack(fill=tk.BOTH, expand=True)

    # Cấu hình Scrollbar
    scrollbar.config(command=tree.yview)

    # Thêm cột vào Treeview
    tree["columns"] = list(filtered_df.columns)
    tree["show"] = "headings"

    for column in filtered_df.columns:
        tree.heading(column, text=column)
        tree.column(column, width=120)
        
    # Thêm dữ liệu vào Treeview
    for _, row in filtered_df.iterrows():
        tree.insert("", tk.END, values=list(row))

# Tạo giao diện chính
root = tk.Tk()
root.title("Quản lý dữ liệu")
tree = ttk.Treeview(root, columns=list(df.columns), show="headings")
for col in df.columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor="w")
tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Khung điều khiển
frame_controls = tk.Frame(root)
frame_controls.pack(pady=10)

tk.Button(frame_controls, text="Tìm kiếm",bg= '#FFCC99', command=search_data).pack(side=tk.LEFT, padx=5)

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

tk.Button(frame_pagination, text="<< Trước",bg='#EE0000', command=go_to_previous_page).pack(side=tk.LEFT, padx=10)
entry_page = tk.Entry(frame_pagination, width=5, justify='center')
entry_page.insert(0, "1")
entry_page.pack(side=tk.LEFT)
entry_page.bind("<Return>", lambda event: go_to_page())
tk.Button(frame_pagination, text="Sau >>",bg='#EE0000', command=go_to_next_page).pack(side=tk.LEFT, padx=10)
label_page_info = tk.Label(frame_pagination, text="")
label_page_info.pack(side=tk.LEFT, padx=10)

# Hiển thị dữ liệu trang đầu tiên
display_data(0)

root.mainloop()
