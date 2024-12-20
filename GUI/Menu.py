from CRUD import create_new_data, update, Delete, Search_Filter, Sort, New, filter_data
from Sort import sort_file
print("Select the action")
print("0.Stop program execution")
print("1.Create new data in new row")
print("2.Update selected data")
print("3.Delete data (one row)")
print("4.Search and Filter on data")
print("5.Sort on data")
print("6.New data generation")
print("7.Filter data")
while True:
    choice = int(input("Input the selection: "))
    if choice == 1:
        create_new_data()
    elif choice == 2:
        update()
    elif choice == 3:
        Delete()
    elif choice == 4:
        Search_Filter()
    elif choice == 5:
        Sort()
    elif choice == 6:
        New()
    elif choice == 7:
        filter_data()
        sort_file()
    elif choice == 0:
        break
    else:
        raise ValueError("Invalid selection")