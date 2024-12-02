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

#Xóa dữ liệu
def delete_data():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Chọn dòng", "Vui lòng chọn ít nhất một dòng để xóa")
        return
    res = messagebox.askyesno('Xóa dữ liệu','Bạn có chắc chắn muốn xóa đòng này hay không?')
    if res:
        for i in range(len(selected_items)):
            item = selected_items[i]
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

# Tìm kiếm dữ liệu
def search_data():
    search_term = simpledialog.askstring("Tìm kiếm", "Nhập từ khóa tìm kiếm:")
    if search_term:
        # Lọc dữ liệu chứa từ khóa tìm kiếm
        filtered_df = df[df.apply(lambda row: search_term.lower() in row.astype(str).str.lower().values, axis=1)]
        if filtered_df.empty:
            messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy dữ liệu phù hợp.")
        else:
            # Tạo cửa sổ mới hiển thị kết quả tìm kiếm
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
 
    for row in tree.get_children():
        tree.delete(row)
    for _, row in filtered_df.iterrows():
        tree.insert("", tk.END, values=list(row))

# Sắp xếp
def sort_data(): 
    def sort():
        global df
        column_name = column_combobox.get()
        order = order_combobox.get()

        if column_name not in df.columns:
            messagebox.showerror("Lỗi", "Vui lòng chọn cột để sắp xếp")
            sort_window.lift()
        elif order not in ["Tăng dần", "Giảm dần"]:
            messagebox.showerror("Lỗi", "Vui lòng chọn kiểu sắp xếp")
            sort_window.lift()
        else:
            ascending = (order == "Tăng dần")
            df = df.sort_values(by=column_name, ascending = ascending)

            sort_window.destroy()
            df.to_csv("onlinesales_sorted.csv", index=False)
            display_data(current_page)
            messagebox.showinfo("Thông báo", "Sắp xếp dữ liệu thành công!")

    sort_window = tk.Toplevel(root)
    sort_window.title("Sắp xếp dữ liệu bán hàng trực tuyến")
    sort_window.geometry("400x300")

    tk.Label(sort_window, text="Chọn cột để sắp xếp:").pack(pady=10)
    column_combobox = ttk.Combobox(sort_window, values=list(df.columns), state="readonly")
    column_combobox.set("Chọn cột")
    column_combobox.pack(pady=10)

    tk.Label(sort_window, text="Chọn thứ tự sắp xếp:").pack(pady=10)
    order_combobox = ttk.Combobox(sort_window, values=["Tăng dần", "Giảm dần"], state="readonly")
    order_combobox.set("Chọn kiểu sắp xếp")
    order_combobox.pack(pady=10)

    tk.Button(sort_window, text="Sắp xếp", command=sort, bg="#00FFFF", width=20).pack(pady=20)
    tk.Button(sort_window, text="Thoát", command=sort_window.destroy, bg="#FF0000", width=20).pack(pady=10)

def filter_data():
    def apply_filter():
        try:
            # Lấy thông tin từ các ô nhập liệu
            column = column_choice.get()
            condition = condition_choice.get()
            value = input_value.get()

            # Kiểm tra điều kiện nhập
            if column not in ["Amount", "Profit", "Quantity"]:
                messagebox.showerror("Lỗi", "Chỉ hỗ trợ lọc theo Amount, Profit, hoặc Quantity!")
                return

            if not value.isdigit():
                messagebox.showerror("Lỗi", f"Giá trị nhập vào cho cột {column} phải là số nguyên!")
                return

            value = int(value)
            # Lọc dữ liệu dựa trên điều kiện
            if condition == "Lớn hơn":
                filtered_df = df[df[column] > value]
            elif condition == "Nhỏ hơn":
                filtered_df = df[df[column] < value]
            elif condition == "Bằng":
                filtered_df = df[df[column] == value]
            else:
                messagebox.showerror("Lỗi", "Điều kiện không hợp lệ!")
                return

            if filtered_df.empty:
                messagebox.showinfo("Kết quả", "Không có dữ liệu thỏa mãn điều kiện lọc.")
            else:
                # Lưu kết quả lọc vào tệp CSV
                filtered_df.to_csv("filter_data.csv", index=False)
                messagebox.showinfo("Thành công", "Dữ liệu lọc đã được lưu vào tệp 'filter_data.csv'.")
                # Hiển thị kết quả lọc
                display_search_results(filtered_df)

            filter_window.destroy()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

    # Tạo cửa sổ lọc dữ liệu
    filter_window = tk.Toplevel(root)
    filter_window.title("Lọc dữ liệu")
    filter_window.geometry("400x300")

    tk.Label(filter_window, text="Chọn cột:").pack(pady=5)
    column_choice = ttk.Combobox(filter_window, values=["Amount", "Profit", "Quantity"], state="readonly")
    column_choice.pack(pady=5)

    tk.Label(filter_window, text="Chọn điều kiện:").pack(pady=5)
    condition_choice = ttk.Combobox(filter_window, values=["Lớn hơn", "Nhỏ hơn", "Bằng"], state="readonly")
    condition_choice.pack(pady=5)

    tk.Label(filter_window, text="Nhập giá trị:").pack(pady=5)
    input_value = tk.Entry(filter_window)
    input_value.pack(pady=5)

    tk.Button(filter_window, text="Áp dụng lọc", command=apply_filter).pack(pady=20)

def search_data2():
    def apply_search():
        try:
            # Lấy thông tin từ các ô nhập liệu
            column1 = column1_choice.get()
            value1 = value1_entry.get()
            column2 = column2_choice.get()
            value2 = value2_entry.get()

            # Lọc dữ liệu dựa trên điều kiện nhập
            filtered_df = df

            if column1 and value1:
                if column1 in df.columns:
                    filtered_df = filtered_df[filtered_df[column1].astype(str).str.contains(value1, case=False, na=False)]

            if column2 and value2:
                if column2 in df.columns:
                    filtered_df = filtered_df[filtered_df[column2].astype(str).str.contains(value2, case=False, na=False)]

            if filtered_df.empty:
                messagebox.showinfo("Kết quả", "Không có dữ liệu thỏa mãn điều kiện tìm kiếm.")
            else:
                # Hiển thị kết quả tìm kiếm
                display_search_results(filtered_df)
                messagebox.showinfo("Kết quả", "Tìm kiếm thành công.")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

    # Tạo cửa sổ tìm kiếm
    search_window = tk.Toplevel(root)
    search_window.title("Tìm kiếm dữ liệu")
    search_window.geometry("500x300")

    tk.Label(search_window, text="Chọn cột 1:").pack(pady=5)
    column1_choice = ttk.Combobox(search_window, values=[col for col in df.columns if col not in ["Amount", "Quantity", "Profit"]], state="readonly")
    column1_choice.pack(pady=5)

    tk.Label(search_window, text="Nhập giá trị 1:").pack(pady=5)
    value1_entry = tk.Entry(search_window)
    value1_entry.pack(pady=5)

    tk.Label(search_window, text="Chọn cột 2:").pack(pady=5)
    column2_choice = ttk.Combobox(search_window, values=[col for col in df.columns if col not in ["Amount", "Quantity", "Profit"]], state="readonly")
    column2_choice.pack(pady=5)

    tk.Label(search_window, text="Nhập giá trị 2:").pack(pady=5)
    value2_entry = tk.Entry(search_window)
    value2_entry.pack(pady=5)

    tk.Button(search_window, text="Áp dụng tìm kiếm", command=apply_search).pack(pady=15)


# Vẽ biểu đồ
def chart(): 
    import All_of_Charts as chart

    # Tạo cửa sổ phụ (Toplevel) để chứa các nút sắp xếp
    chart_window = tk.Toplevel(root)
    chart_window.title("Vẽ biểu đồ dữ liệu bán hàng trực tuyến")
    
   # Tạo frame để chứa các nút sắp xếp
    # chart_window.config(height=15)
    frame_chart = tk.Frame(chart_window)
    frame_chart.pack(padx=10, pady=10)
       
    # Các nút vẽ biểu đồ
    button_width = 70
    tk.Button(frame_chart, text="Biểu đồ phân phối các phương thức thanh toán",bg="#FFCCCC", command= chart.paymentmode, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Biểu đồ phân phối số lượng giao dịch theo bang",bg="#FFFFFF", command=chart.state, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Biểu đồ phân phối danh mục",bg="#FFCCCC", command= chart.Category_distribution, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Biểu đồ tần số về số lượng và phân tán số lượng so với chỉ số",bg="#FFFFFF", command=chart.quantity, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Biểu đồ lợi nhuận theo danh mục sản phẩm",bg="#FFCCCC", command= chart.profit_category, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Biểu đồ lợi nhuận theo danh mục phụ sản phẩm",bg="#FFFFFF", command=chart.profit_subcategory, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Biểu đồ về khả năng sinh lời theo phương thức thanh toán",bg="#FFCCCC", command= chart.profit_paymenntmethod, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Biểu đồ xu hướng doanh số thay đổi theo thời gian",bg="#FFFFFF", command=chart.sale_trend, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Biểu đồ phân bố tần số của số lượng và sự phân tán của số lượng so với chỉ số",bg="#FFCCCC", command= chart.amount, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Biểu đồ phân bố tần suất của lợi nhuận và sự phân tán của lợi nhuận so với chỉ số",bg="#FFFFFF", command=chart.profit, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Tổng quan hiệu quả kinh doanh",bg="#FFCCCC",command=chart.Business_performance_overview, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Số lượng mua hàng theo danh mục và tháng trong năm",bg="#FFFFFF", command= chart.plot_monthly_sales_by_category, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text =" Top 10 thành phố và bang có lợi nhuận cao nhất",bg="#FFCCCC", command= chart.top_10_city_and_state_hightest_profit, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Tổng doanh thu theo sản phẩm của Electronics",bg="#FFFFFF", command= chart.most_sold_productst, width=button_width).pack(pady=5)
    tk.Button(frame_chart, text="Thoát !",bg="#FF0000",command=chart_window.destroy,width=button_width).pack(pady=5)

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
tk.Button(frame_controls, text="Tạo dữ liệu mới" ,bg= '#99FFFF' ,command=create_new_data).pack(side=tk.LEFT, padx=5)
tk.Button(frame_controls, text="Cập nhật dữ liệu",bg= '#FFCC99', command=update_data).pack(side=tk.LEFT, padx=5)
tk.Button(frame_controls, text="Xóa dữ liệu",bg= '#99FFFF', command=delete_data).pack(side=tk.LEFT, padx=5)
tk.Button(frame_controls, text="Tìm kiếm",bg= '#FFCC99', command=search_data).pack(side=tk.LEFT, padx=5)
tk.Button(frame_controls, text="Sắp xếp",bg= '#99FFFF',command=sort_data).pack(side=tk.LEFT, padx=5)
tk.Button(frame_controls, text="Vẽ biểu đồ",bg= '#FFCC99',command=chart).pack(side=tk.LEFT, padx=5)
tk.Button(frame_controls, text="Lọc dữ liệu", bg='#99FFFF', command=filter_data).pack(side=tk.LEFT, padx=5)
tk.Button(frame_controls, text="Tìm kiếm nâng cao", bg='#FFCC99', command=search_data2).pack(side=tk.LEFT, padx=5)

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