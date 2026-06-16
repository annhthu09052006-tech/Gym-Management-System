import tkinter as tk
from tkinter import ttk, messagebox
from Services.membership_service import MembershipService
from Services.trainer_service import TrainerService
from Services.report_service import ReportService
from Models.standard import StandardMembership
from Models.premium import PremiumMembership
from Models.vip import VIPMembership
from Models.trainer import Trainer
from Models.schedule import Schedule

class ManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HỆ THỐNG QUẢN LÝ TRUNG TÂM GYM NÂNG CAO")
        self.root.geometry("1000x650")
        
        # Khởi tạo các dịch vụ tầng Services
        self.mem_service = MembershipService()
        self.train_service = TrainerService()
        self.rep_service = ReportService(self.mem_service)
        
        # Khởi tạo hệ thống quản lý các Tab (Notebook)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tạo các phân vùng giao diện cho từng tab
        self.tab_member = tk.Frame(self.notebook)
        self.tab_trainer = tk.Frame(self.notebook)
        self.tab_schedule = tk.Frame(self.notebook)
        
        self.notebook.add(self.tab_member, text=" Quản Lý Hội Viên ")
        self.notebook.add(self.tab_trainer, text=" Quản Lý Huấn Luyện Viên ")
        self.notebook.add(self.tab_schedule, text=" Xếp Lịch Tập (PT) ")
        
        # Vẽ giao diện cho từng phân vùng
        self.setup_member_tab()
        self.setup_trainer_tab()
        self.setup_schedule_tab()

    # ==========================================
    # 1. TAB HỘI VIÊN (Đầy đủ chức năng cũ )
    # ==========================================
    def setup_member_tab(self):
        main_frame = tk.Frame(self.tab_member)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Form nhập bên trái
        form_frame = tk.LabelFrame(main_frame, text=" Thông tin Hội Viên ", padx=10, pady=10, font=("Helvetica", 10, "bold"))
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        tk.Label(form_frame, text="Mã Hội Viên (ID):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ent_id = tk.Entry(form_frame, width=22)
        self.ent_id.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Tên Khách Hàng:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.ent_name = tk.Entry(form_frame, width=22)
        self.ent_name.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Số Điện Thoại:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.ent_phone = tk.Entry(form_frame, width=22)
        self.ent_phone.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Hạng Thẻ Tập:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.cbo_tier = ttk.Combobox(form_frame, values=["Standard", "Premium", "VIP"], width=19, state="readonly")
        self.cbo_tier.current(0)
        self.cbo_tier.grid(row=3, column=1, pady=5)

        # Cụm nút bấm hội viên
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
        tk.Button(btn_frame, text="Thêm Mới", width=10, bg="#4CAF50", fg="white", command=self.add_member).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Sửa SĐT/Tên", width=10, bg="#2196F3", fg="white", command=self.update_member).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Xóa", width=10, bg="#F44336", fg="white", command=self.delete_member).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Làm Trống", width=10, bg="#9E9E9E", fg="white", command=self.clear_member_entries).grid(row=1, column=1, padx=5, pady=5)

        # Công cụ nâng cao
        tool_frame = tk.LabelFrame(form_frame, text=" Tiện ích mở rộng ", padx=5, pady=5)
        tool_frame.grid(row=5, column=0, columnspan=2, sticky=tk.EW, pady=10)
        self.ent_search = tk.Entry(tool_frame, width=12)
        self.ent_search.grid(row=0, column=0, padx=2, pady=5)
        tk.Button(tool_frame, text="Tìm kiếm", command=self.search_member, bg="#FF9800", fg="white").grid(row=0, column=1, padx=2, pady=5)
        tk.Button(tool_frame, text="Xếp A-Z", command=self.sort_members, width=8).grid(row=0, column=2, padx=2, pady=5)
        tk.Button(tool_frame, text="Báo Cáo Doanh Thu & Xuất CSV", bg="#9C27B0", fg="white", command=self.show_statistics).grid(row=1, column=0, columnspan=3, sticky=tk.EW, pady=5)

        # Bảng dữ liệu bên phải
        data_frame = tk.LabelFrame(main_frame, text=" Danh Sách Hội Viên Hiện Có ", padx=5, pady=5, font=("Helvetica", 10, "bold"))
        data_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        columns = ("id", "name", "phone", "tier", "fee")
        self.tree_member = ttk.Treeview(data_frame, columns=columns, show="headings")
        self.tree_member.heading("id", text="Mã Hội Viên")
        self.tree_member.heading("name", text="Tên Khách Hàng")
        self.tree_member.heading("phone", text="Số Điện Thoại")
        self.tree_member.heading("tier", text="Hạng Thẻ")
        self.tree_member.heading("fee", text="Học Phí (VND)")
        
        self.tree_member.column("id", width=90, anchor=tk.CENTER)
        self.tree_member.column("name", width=140)
        self.tree_member.column("phone", width=100, anchor=tk.CENTER)
        self.tree_member.column("tier", width=80, anchor=tk.CENTER)
        self.tree_member.column("fee", width=100, anchor=tk.E)

        sb = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, command=self.tree_member.yview)
        self.tree_member.configure(yscrollcommand=sb.set)
        self.tree_member.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_member.bind("<<TreeviewSelect>>", self.on_member_select)
        self.load_member_data()

    # Logic xử lý Tab Hội viên
    def load_member_data(self, member_list=None):
        for item in self.tree_member.get_children(): self.tree_member.delete(item)
        if member_list is None: member_list = self.mem_service.get_all_members()
        for m in member_list:
            t = m.__class__.__name__.replace("Membership", "")
            self.tree_member.insert("", tk.END, values=(m.member_id, m.name, m.phone, t, f"{m.calculate_fee():,}"))

    def on_member_select(self, event):
        selected = self.tree_member.focus()
        if not selected: return
        val = self.tree_member.item(selected, "values")
        self.clear_member_entries()
        self.ent_id.insert(0, val[0])
        self.ent_name.insert(0, val[1])
        self.ent_phone.insert(0, val[2])
        self.cbo_tier.set(val[3])

    def add_member(self):
        m_id, name, phone, tier = self.ent_id.get().strip(), self.ent_name.get().strip(), self.ent_phone.get().strip(), self.cbo_tier.get()
        if not m_id or not name or not phone:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        if tier == "Standard": m = StandardMembership(m_id, name, phone)
        elif tier == "Premium": m = PremiumMembership(m_id, name, phone)
        elif tier == "VIP": m = VIPMembership(m_id, name, phone)
        self.mem_service.add_member(m)
        messagebox.showinfo("Thành công", "Đã thêm hội viên mới!")
        self.load_member_data()
        self.clear_member_entries()

    def update_member(self):
        m_id, name, phone = self.ent_id.get().strip(), self.ent_name.get().strip(), self.ent_phone.get().strip()
        if self.mem_service.update_member(m_id, name, phone):
            messagebox.showinfo("Thành công", "Cập nhật thành công!")
            self.load_member_data()
            self.clear_member_entries()
        else: messagebox.showerror("Lỗi", "Không tìm thấy mã hội viên!")

    def delete_member(self):
        m_id = self.ent_id.get().strip()
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa hội viên này không?"):
            if self.mem_service.delete_member(m_id):
                messagebox.showinfo("Thành công", "Đã xóa hội viên!")
                self.load_member_data()
                self.clear_member_entries()
            else: messagebox.showerror("Lỗi", "Mã không tồn tại!")

    def search_member(self):
        kw = self.ent_search.get().strip()
        self.load_member_data(self.mem_service.search_member(kw) if kw else None)

    def sort_members(self):
        self.load_member_data(self.mem_service.sort_members_by_name())

    def show_statistics(self):
        # 1. Tính toán số liệu doanh thu từ Service
        stats, total = self.rep_service.get_revenue_by_tier()
        
        # 2. Tự động xuất file báo cáo CSV (Excel) vào thư mục Data
        path = self.rep_service.export_csv()
        
        # 3. Tạo một cửa sổ phụ nổi lên (Toplevel) để hiển thị bảng Excel
        excel_win = tk.Toplevel(self.root)
        excel_win.title("XEM TRƯỚC BẢO CÁO EXCEL (CSV)")
        excel_win.geometry("700x400")
        excel_win.grab_set() # Giữ cửa sổ này luôn ở trên cùng
        
        # Tiêu đề cửa sổ phụ
        tk.Label(excel_win, text="DANH SÁCH XUẤT BÁO CÁO DOANH THU", font=("Helvetica", 12, "bold"), fg="green").pack(pady=10)
        
        # Tạo bảng Treeview để mô phỏng lại file Excel
        cols = ("col1", "col2", "col3", "col4", "col5")
        preview_tree = ttk.Treeview(excel_win, columns=cols, show="headings")
        
        preview_tree.heading("col1", text="Mã Hội Viên")
        preview_tree.heading("col2", text="Tên Khách Hàng")
        preview_tree.heading("col3", text="Số Điện Thoại")
        preview_tree.heading("col4", text="Hạng Thẻ")
        preview_tree.heading("col5", text="Giá Gói Tập (VND)")
        
        preview_tree.column("col1", width=100, anchor=tk.CENTER)
        preview_tree.column("col2", width=150)
        preview_tree.column("col3", width=110, anchor=tk.CENTER)
        preview_tree.column("col4", width=90, anchor=tk.CENTER)
        preview_tree.column("col5", width=130, anchor=tk.E)
        
        preview_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 4. ĐỌC DỮ LIỆU TỪ FILE CSV VỪA XUẤT ĐỂ ĐỔ LÊN BẢNG
        try:
            import csv
            with open(path, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader) # Bỏ qua dòng tiêu đề cột đầu tiên
                
                for row in reader:
                    if row: # Nếu dòng không bị trống
                        # Nếu gặp dòng tổng kết doanh thu ở cuối file
                        if "TỔNG DOANH THU" in row[0]:
                            preview_tree.insert("", tk.END, values=(row[0], "", "", "", row[4]))
                        else:
                            preview_tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file Excel để hiển thị: {e}")

        # Thêm dòng thông báo lưu trữ ở dưới cùng cửa sổ phụ
        tk.Label(excel_win, text=f"📂 File đã được lưu vĩnh viễn tại: {path}", fg="gray", font=("Helvetica", 9, "italic")).pack(pady=10)
    def clear_member_entries(self):
        self.ent_id.delete(0, tk.END); self.ent_name.delete(0, tk.END); self.ent_phone.delete(0, tk.END)

    # ==========================================
    # 2. TAB HUẤN LUYỆN VIÊN 
    # ==========================================
    def setup_trainer_tab(self):
        main_frame = tk.Frame(self.tab_trainer)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        form_frame = tk.LabelFrame(main_frame, text=" Đăng ký Huấn Luyện Viên (PT) ", padx=10, pady=10, font=("Helvetica", 10, "bold"))
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        tk.Label(form_frame, text="Mã Trainer (ID):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ent_t_id = tk.Entry(form_frame, width=22)
        self.ent_t_id.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Tên Trainer:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.ent_t_name = tk.Entry(form_frame, width=22)
        self.ent_t_name.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Chuyên Môn:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.ent_t_spec = tk.Entry(form_frame, width=22)
        self.ent_t_spec.grid(row=2, column=1, pady=5)

        tk.Button(form_frame, text="Thêm Trainer", bg="#4CAF50", fg="white", width=18, command=self.add_trainer).grid(row=3, column=0, columnspan=2, pady=15)

        data_frame = tk.LabelFrame(main_frame, text=" Đội Ngũ Huấn Luyện Viên ", padx=5, pady=5, font=("Helvetica", 10, "bold"))
        data_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        self.tree_trainer = ttk.Treeview(data_frame, columns=("id", "name", "spec"), show="headings")
        self.tree_trainer.heading("id", text="Mã PT")
        self.tree_trainer.heading("name", text="Họ Và Tên")
        self.tree_trainer.heading("spec", text="Chuyên Môn Giảng Dạy")
        self.tree_trainer.pack(fill=tk.BOTH, expand=True)
        self.load_trainer_data()

    def load_trainer_data(self):
        for item in self.tree_trainer.get_children(): self.tree_trainer.delete(item)
        for t in self.train_service.get_all_trainers():
            self.tree_trainer.insert("", tk.END, values=(t.trainer_id, t.name, t.specialty))

    def add_trainer(self):
        t_id, name, spec = self.ent_t_id.get().strip(), self.ent_t_name.get().strip(), self.ent_t_spec.get().strip()
        if not t_id or not name or not spec:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đủ thông tin Trainer!")
            return
        self.train_service.add_trainer(Trainer(t_id, name, spec))
        messagebox.showinfo("Thành công", f"Đã thêm Huấn luyện viên {name}!")
        self.load_trainer_data()
        self.ent_t_id.delete(0, tk.END); self.ent_t_name.delete(0, tk.END); self.ent_t_spec.delete(0, tk.END)

    # ==========================================
    # 3. TAB XẾP LỊCH TẬP 
    # ==========================================
    def setup_schedule_tab(self):
        main_frame = tk.Frame(self.tab_schedule)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        form_frame = tk.LabelFrame(main_frame, text=" Xếp Lịch Hướng Dẫn ", padx=10, pady=10, font=("Helvetica", 10, "bold"))
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        tk.Label(form_frame, text="Mã Lịch Tập:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ent_s_id = tk.Entry(form_frame, width=22)
        self.ent_s_id.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Mã Hội Viên:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.ent_s_mid = tk.Entry(form_frame, width=22)
        self.ent_s_mid.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Mã Trainer (PT):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.ent_s_tid = tk.Entry(form_frame, width=22)
        self.ent_s_tid.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Khung Giờ Tập:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.ent_s_slot = tk.Entry(form_frame, width=22)
        self.ent_s_slot.grid(row=3, column=1, pady=5)

        tk.Button(form_frame, text="Sắp Xếp Lịch Tập", bg="#2196F3", fg="white", width=18, command=self.add_schedule).grid(row=4, column=0, columnspan=2, pady=15)

        data_frame = tk.LabelFrame(main_frame, text=" Nhật Ký Lịch Tập Trung Tâm ", padx=5, pady=5, font=("Helvetica", 10, "bold"))
        data_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        self.tree_schedule = ttk.Treeview(data_frame, columns=("sid", "mid", "tid", "slot"), show="headings")
        self.tree_schedule.heading("sid", text="Mã Lịch")
        self.tree_schedule.heading("mid", text="Mã Hội Viên")
        self.tree_schedule.heading("tid", text="Mã PT")
        self.tree_schedule.heading("slot", text="Giờ Tập Khớp")
        self.tree_schedule.pack(fill=tk.BOTH, expand=True)
        self.load_schedule_data()

    def load_schedule_data(self):
        for item in self.tree_schedule.get_children(): self.tree_schedule.delete(item)
        for s in self.train_service.get_all_schedules():
            self.tree_schedule.insert("", tk.END, values=(s.schedule_id, s.member_id, s.trainer_id, s.time_slot))

    def add_schedule(self):
        s_id, m_id, t_id, slot = self.ent_s_id.get().strip(), self.ent_s_mid.get().strip(), self.ent_s_tid.get().strip(), self.ent_s_slot.get().strip()
        if not s_id or not m_id or not t_id or not slot:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin xếp lịch lịch!")
            return
        self.train_service.add_schedule(Schedule(s_id, m_id, t_id, slot))
        messagebox.showinfo("Thành công", "Đã lên lịch hẹn tập thành công!")
        self.load_schedule_data()
        self.ent_s_id.delete(0, tk.END); self.ent_s_mid.delete(0, tk.END); self.ent_s_tid.delete(0, tk.END); self.ent_s_slot.delete(0, tk.END)