import tkinter as tk
from Views.menu import ManagementGUI

def main():
    # Khởi tạo cửa sổ gốc của thư viện Tkinter
    root = tk.Tk()
    
    # Gắn giao diện Quản lý vào cửa sổ hệ thống
    app = ManagementGUI(root)
    
    # Giữ cho cửa sổ GUI hiển thị liên tục cho đến khi nhấn dấu X thoát app
    root.mainloop()

if __name__ == "__main__":
    main()