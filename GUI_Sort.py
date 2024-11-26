import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import numpy as np

# Đọc và chuẩn bị dữ liệu
def load_data():
    df_details = pd.read_csv("Details.csv")
    df_orders = pd.read_csv("Orders.csv")
    df_merged = pd.merge(df_details, df_orders, on="Order ID")
    df_sorted = df_merged.sort_values(by="Order ID")
    df_sorted.to_csv("onlinesales_sorted.csv", index=False)
    df_online_sales = pd.read_csv("onlinesales_sorted.csv")
    
    return df_online_sales

df = load_data()
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y')
df.to_csv("onlinesales_sorted.csv", index=False)
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

#Xóa dữ liệu
def delete_data():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Chọn dòng", "Vui lòng chọn ít nhất một dòng để xóa")
        return
    res = messagebox.askyesno('Xóa dữ liệu','Bạn có chắc chắn muốn xóa đòng này hay không?')
    if res:
        item = selected_items[0]
        values = tree.item(item)['values']
        index = df.index[
                (df['Order ID'] == str(values[0])) &
                (df['Amount'] == values[1]) &
                (df['Profit'] == values[2]) &
                (df['Quantity'] == values[3]) &
                (df['Category'] == str(values[4])) &
                (df['Sub-Category'] == str(values[5])) &
                (df['PaymentMode'] == str(values[6])) &
                (df['Order Date'] == str(values[7])) &
                (df['CustomerName'] == str(values[8])) &
                (df['State'] == str(values[9])) &
                (df['City'] == str(values[10]))]
        df.drop(index, inplace=True)
        df.to_csv("onlinesales_sorted.csv", index=False)
        
        global current_page
        max_pages = (len(df) - 1) // items_per_page
        if current_page > max_pages:
            current_page = max_pages
        display_data(current_page)
        messagebox.showinfo("Thông báo", "Xóa dữ liệu thành công!")

# Sắp xếp
def sort_data(): 
    def sort(column_index):
        global df
        column_name = df.columns[column_index]

        if column_name == "Amount" or column_name == "Profit" or column_name == "Quantity":
            df[column_name] = df[column_name].astype(int)
        df = df.sort_values(by=column_name)

        sort_window.destroy()     
        df.to_csv("onlinesales_sorted.csv", index=False)
        display_data(current_page)
        messagebox.showinfo("Thông báo", "Sắp xếp dữ liệu thành công!")

    # Tạo cửa sổ phụ (Toplevel) để chứa các nút sắp xếp
    sort_window = tk.Toplevel(root)
    sort_window.title("Sắp xếp dữ liệu bán hàng trực tuyến")
    sort_window.config(height=11)

    # Tạo frame để chứa các nút sắp xếp
    frame_sort = tk.Frame(sort_window)
    frame_sort.pack(padx=10, pady=10)

    # Các nút sắp xếp
    button_width = 30
    tk.Button(frame_sort, text="Sắp xếp theo ID", command=lambda: sort(0), width=button_width).pack(pady=5)
    tk.Button(frame_sort, text="Sắp xếp theo Amount", command=lambda: sort(1), width=button_width).pack(pady=5)
    tk.Button(frame_sort, text="Sắp xếp theo Profit", command=lambda: sort(2), width=button_width).pack(pady=5)
    tk.Button(frame_sort, text="Sắp xếp theo Quantity", command=lambda: sort(3), width=button_width).pack(pady=5)
    tk.Button(frame_sort, text="Sắp xếp theo Category", command=lambda: sort(4), width=button_width).pack(pady=5)
    tk.Button(frame_sort, text="Sắp xếp theo Sub-Category", command=lambda: sort(5), width=button_width).pack(pady=5)
    tk.Button(frame_sort, text="Sắp xếp theo PaymentMode", command=lambda: sort(6), width=button_width).pack(pady=5)
    tk.Button(frame_sort, text="Sắp xếp theo Order date", command=lambda: sort(7), width=button_width).pack(pady=5)
    tk.Button(frame_sort, text="Sắp xếp theo CustomerName", command=lambda: sort(8), width=button_width).pack(pady=5)
    tk.Button(frame_sort, text="Sắp xếp theo State", command=lambda: sort(9), width=button_width).pack(pady=5)
    tk.Button(frame_sort, text="Sắp xếp theo City", command=lambda: sort(10), width=button_width).pack(pady=5)
    tk.Button(frame_sort, text="Thoát", command=sort_window.destroy , width=button_width).pack(pady=5)


# Vẽ biểu đồ
def chart(): 
    import All_of_Charts as chart

    # Tạo cửa sổ phụ (Toplevel) để chứa các nút sắp xếp
    chart_window = tk.Toplevel(root)
    chart_window.title("Vẽ biểu đồ dữ liệu bán hàng trực tuyến")
    chart_window.config(height = 13)

    # Tạo frame để chứa các nút sắp xếp
    frame_chart = tk.Frame(chart_window)
    frame_chart.pack(padx=10, pady=10)
       
    # Các nút vẽ biểu đồ
    button_width = 70
    tk.Button(frame_chart, text="Biểu đồ phân phối các phương thức thanh toán", command= chart.paymentmode, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Biểu đồ phân phối số lượng giao dịch theo bang", command=chart.state, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Biểu đồ phân phối danh mục", command= chart.Category_distribution, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Biểu đồ tần số về số lượng và phân tán số lượng so với chỉ số", command=chart.quantity, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Biểu đồ lợi nhuận theo danh mục sản phẩm", command= chart.profit_category, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Biểu đồ lợi nhuận theo danh mục phụ sản phẩm", command=chart.profit_subcategory, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Biểu đồ về khả năng sinh lời theo phương thức thanh toán", command= chart.profit_paymenntmethod, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Biểu đồ xu hướng doanh số thay đổi theo thời gian", command=chart.sale_trend, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Biểu đồ phân bố tần số của số lượng và sự phân tán của số lượng so với chỉ số", command= chart.amount, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Biểu đồ phân bố tần suất của lợi nhuận và sự phân tán của lợi nhuận so với chỉ số", command=chart.profit, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Tổng quan hiệu quả kinh doanh", command= chart.Business_performance_overview, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Số lượng mua hàng theo danh mục và tháng trong năm", command=chart.plot_monthly_sales_by_category, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Thoát", command=chart_window.destroy , width=button_width).pack(pady=5)

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
tk.Button(frame_controls, text="Xóa dữ liệu", command=delete_data).pack(side=tk.LEFT, padx=5)
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