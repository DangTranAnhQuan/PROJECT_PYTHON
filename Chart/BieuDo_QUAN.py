# Trực quan hóa dữ liệu
# Xem sự phân bổ của các danh mục
import matplotlib.pyplot as plt
from begin import df_online_sales
plt.figure(figsize=(10, 6))
df_online_sales['Category'].value_counts().plot(kind='bar')
plt.title('Category Distribution')
plt.xlabel('Category')
plt.ylabel('Amount')
plt.xticks(rotation = 0)
plt.subplots_adjust(bottom = 0.2)
plt.show()