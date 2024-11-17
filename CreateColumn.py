import pandas as pd 

def CreateColumn():
    # Đọc dữ liệu từ file đã ghép trước đó
    df_online_sales = pd.read_csv("onlinesales_sorted.csv")

    # Thêm cột Profit Margin
    df_online_sales['Profit Margin (%)'] = round((df_online_sales['Profit'] / df_online_sales['Amount']) * 100,2)

    # Xử lý trường hợp dữ liệu không hợp lệ (Amount = 0)
    df_online_sales['Profit Margin (%)'] = df_online_sales['Profit Margin (%)'].fillna(0)

    # Lưu lại vào file mới
    df_online_sales.to_csv("onlinesales_sorted.csv", index=False)

    print("File đã được lưu tại onlinesales_sortedn.csv")
CreateColumn()
