# Gym-Management-System

##  1. Tổng quan Đề tài & Tính năng Hệ thống

Hệ thống được xây dựng hoàn toàn bằng ngôn ngữ **Python 3**, đáp ứng trọn vẹn các yêu cầu quản lý thực tế tại một trung tâm thể hình với hai phương thức tương tác linh hoạt (CLI và GUI Tkinter):

### 🔹 Các chức năng cốt lõi (Core Features)
1. **Quản lý Hội viên (Membership Management):**
   - Thêm mới, xóa, cập nhật thông tin và tìm kiếm hội viên theo mã định danh hoặc tên.
   - Tính toán học phí tự động dựa trên phân cấp hạng thẻ thành viên.
   - Tiện ích nâng cao: Sắp xếp danh sách hội viên theo thứ tự bảng chữ cái (A-Z).
2. **Quản lý Huấn luyện viên (Trainer Management):**
   - Lưu trữ danh sách hồ sơ PT, bao gồm mã số, họ tên và chuyên môn huấn luyện (Gym, Yoga, Cardio,...).
3. **Quản lý Lịch tập (Schedule Management):**
   - Thiết lập lịch hẹn tập giữa Hội viên và Huấn luyện viên theo các khung giờ (Slot) cố định.
4. **Thống kê Doanh thu & Xuất báo cáo Excel (Reporting):**
   - Tổng hợp doanh thu thực tế phân loại theo từng hạng thẻ tập.
   - Tự động xuất file báo cáo định dạng `.csv`. Tích hợp cửa sổ giao diện phụ (Sub-window) hiển thị trực quan cấu trúc bảng dữ liệu Excel ngay trên ứng dụng.

## 2. Kiến trúc Phân tầng của Dự án (Layered Architecture)

Dự án áp dụng chặt chẽ kiến trúc phân tầng (Separation of Concerns) để tách biệt hoàn toàn giữa giao diện, xử lý nghiệp vụ và lưu trữ dữ liệu, giúp mã nguồn dễ dàng bảo trì và mở rộng:

GYM-MANAGEMENT-SYSTEM/
│
├── Data/                   # Tầng lưu trữ dữ liệu bền vững (Persistence Layer)
│   ├── memberships.json    # Cơ sở dữ liệu lưu cấu trúc thẻ hội viên và học phí
│   ├── trainers.json       # Cơ sở dữ liệu lưu thông tin huấn luyện viên
│   ├── schedules.json      # Cơ sở dữ liệu lưu lịch hẹn tập phối hợp giữa các bên
│   └── gym_revenue_report.csv # Tệp tin báo cáo doanh thu Excel xuất tự động
│
├── Models/                 # Tầng định nghĩa thực thể (Domain Entities)
│   ├── membership.py       # Lớp cha trừu tượng (Abstract Base Class) cho Thẻ tập
│   ├── standard.py         # Hạng thẻ Standard (Kế thừa từ Membership)
│   ├── premium.py          # Hạng thẻ Premium (Kế thừa từ Membership)
│   ├── vip.py              # Hạng thẻ VIP (Kế thừa từ Membership)
│   ├── trainer.py          # Định nghĩa lớp đối tượng Huấn luyện viên
│   └── schedule.py         # Định nghĩa lớp đối tượng Lịch tập
│
├── Services/               # Tầng xử lý logic nghiệp vụ (Business Logic Layer)
│   ├── membership_service.py # Nghiệp vụ CRUD, tìm kiếm và kiểm lỗi Hội viên
│   ├── trainer_service.py    # Nghiệp vụ điều phối dữ liệu PT và Lịch tập
│   └── report_service.py     # Logic thống kê tài chính và trích xuất dữ liệu CSV
│
├── Views/                  # Tầng giao diện người dùng (Presentation Layer)
│   └── menu.py             # Điều khiển toàn bộ cấu trúc GUI Tkinter và CLI Console
│
├── main.py                 # Điểm khởi chạy hệ thống (Entry Point)
└── README.md               # Tài liệu hướng dẫn đồ án

## 3. Minh chứng Áp dụng 4 Tính chất Cốt lõi của OOP (Object-Oriented Programming)

Dự án hiện thực hóa một cách toàn diện các nguyên lý cốt lõi của lập trình hướng đối tượng nâng cao, cấu trúc hệ thống dựa trên mô hình phân cấp thực thể rõ ràng:

1. **Tính trừu tượng (Abstraction):** - Hệ thống định nghĩa lớp cơ sở trừu tượng `Membership` (kế thừa từ `abc.ABC`).
   - Phương thức toán học tính toán học phí được khai báo dưới dạng trừu tượng: `@abstractmethod def calculate_fee(self) -> float:`. Phương thức này không có thân hàm cụ thể, đóng vai trò như một "hợp đồng pháp lý" bắt buộc mọi hạng thẻ thành viên con khi kế thừa phải triển khai (override) lại theo quy tắc riêng.

2. **Tính kế thừa (Inheritance):**
   - Lớp cha `Membership` tập trung quản lý các thuộc tính dùng chung của mọi thành viên gồm: `member_id` (Mã định danh), `name` (Họ tên), và `phone` (Số điện thoại).
   - Các lớp con ứng với từng phân cấp gói dịch vụ thực tế bao gồm `StandardMembership`, `PremiumMembership`, và `VIPMembership` đồng loạt kế thừa trực tiếp từ lớp cha `Membership`. Điều này giúp tái sử dụng mã nguồn tối đa, giảm thiểu sự lặp lại mã (Code Duplication).

3. **Tính đa hình (Polymorphism):**
   - Thể hiện rõ nét qua việc ghi đè phương thức (`Method Overriding`). Cùng là lời gọi hàm `calculate_fee()`, nhưng khi thực thi tại runtime, Python sẽ tự động kích hoạt logic tính toán riêng biệt dựa trên kiểu đối tượng thực tế:
     - Gói **Standard**: Trả về mức học phí nền tảng cố định.
     - Gói **Premium**: Tích hợp thêm chi phí thuê huấn luyện viên cá nhân (PT) cơ bản.
     - Gói **VIP**: Tính toán trọn gói dịch vụ cao cấp kèm theo các đặc quyền mở rộng (bể bơi, phòng xông hơi).

4. **Tính đóng gói (Encapsulation):**
   - Toàn bộ các thuộc tính nhạy cảm ảnh hưởng đến tính toàn vẹn dữ liệu của đối tượng (như `_member_id`, `_phone`, `_name`) đều được bọc lót dưới trạng thái ẩn (`Protected / Private` bằng tiền tố dấu gạch dưới).
   - Việc truy cập, đọc dữ liệu hoặc hiệu chỉnh giá trị của các thuộc tính này bắt buộc phải đi qua các cổng kiểm soát dữ liệu đầu vào là `@property` (Getter) và `@setter` (Setter), ngăn chặn tuyệt đối tình trạng gán dữ liệu bẩn hoặc sai định dạng vào thực thể đối tượng.


##  4. Cơ chế Xử lý Ngoại lệ & Kiểm lỗi Dữ liệu (Exception Handling & Data Validation)
Để đảm bảo hệ thống vận hành bền bỉ và đạt tiêu chuẩn "chống sập" (Bulletproof) trước các thao tác sai từ người dùng, các tầng kiến trúc được bọc lót kỹ lưỡng:

- **Kiểm lỗi dữ liệu đầu vào (Input Validation tại tầng Services):**
   - Khi thực hiện các nghiệp vụ thêm mới hoặc cập nhật thông tin hội viên (`MembershipService`), hệ thống tự động kiểm tra tính hợp lệ: từ chối xử lý khi các trường thông tin bị bỏ trống, kích hoạt ngoại lệ `ValueError` khi số điện thoại chứa ký tự chữ hoặc không đủ độ dài quy định (từ 9 đến 11 chữ số).
   - Kiểm tra trùng lặp: Ngăn chặn hành vi tạo mới hai hội viên hoặc huấn luyện viên có chung mã định danh (ID).

- **Ràng buộc toàn vẹn dữ liệu (Transaction Logic tại tầng Services):**
   - Khi điều phối nghiệp vụ lập lịch tập (`TrainerService`), hệ thống thực hiện cơ chế đối soát chéo (Cross-reference validation). Chương trình sẽ kiểm tra xem `member_id` và `trainer_id` nhập vào có tồn tại thực tế trong cơ sở dữ liệu hay không. Nếu phát hiện mã giả lập hoặc không tồn tại, hệ thống lập tức chặn quy trình và ném ra ngoại lệ thông báo lỗi liên kết.

- **Bọc lót và chuyển hóa lỗi trên giao diện đồ họa (Tầng Views):**
   - Tất cả các hàm lắng nghe sự kiện nút bấm trên GUI (Thêm, Xóa, Chỉnh sửa, Xuất Excel) được bao bọc hoàn toàn trong khối lệnh điều khiển lỗi `try-except`.
   - Khi có bất kỳ ngoại lệ nào phát sinh từ logic nghiệp vụ bên dưới, hệ thống sẽ bắt lại, đóng gói lỗi và hiển thị lên màn hình dưới dạng hộp thoại thông báo `messagebox.showerror` trực quan, bảo vệ ứng dụng không bị crash đột ngột.


## 5. Hướng dẫn Khởi chạy Chương trình (Deployment Guide)

### 🔹 Yêu cầu hệ thống (Prerequisites)
- Thiết bị đã cài đặt sẵn môi trường thực thi **Python 3.8** hoặc các phiên bản cao hơn.
- Dự án được xây dựng tối ưu bằng cách sử dụng hoàn toàn các module và thư viện chuẩn tích hợp sẵn của Python bao gồm: `tkinter` (Giao diện), `json` (Lưu trữ bền vững), `csv` (Trích xuất dữ liệu), và `abc` (Xử lý cấu trúc trừu tượng). Vì vậy, người kiểm thử **không cần cài đặt thêm bất kỳ thư viện bên ngoài nào (No external pip packages required)**.

### 🔹 Thao tác khởi chạy thực tế (Execution Steps)
1. Mở cửa sổ dòng lệnh (Terminal, PowerShell trên Windows hoặc Terminal trên macOS/Linux) và di chuyển vào thư mục gốc của dự án:
   ```bash
   cd Gym-Management-System
2. Thực thi tệp điều hướng trung tâm: Chạy file main.py để kích hoạt hệ thống điều phối luồng bằng lệnh:
   ```bash
   python main.py

##  6. EVALUATION CRITERIA (TIÊU CHÍ ĐÁNH GIÁ ĐỒ ÁN)

Bảng tiêu chí đánh giá chi tiết được trích xuất nguyên bản theo tài liệu hướng dẫn chấm điểm của Giảng viên (**TS. Trần Văn Long**) và kết quả nghiệm thu thực tế của dự án:

| Category (Phân loại) | Detailed Evaluation Criteria (Tiêu chí đánh giá chi tiết) | Points (Tối đa) | Score (Đạt) |
| :--- | :--- | :---: | :---: |
| **BASIC**<br><br>*(CƠ BẢN)*<br><br>**(7.0 pts)** | **1. Encapsulation:** All sensitive attributes are Private, with logical Getter/Setter control.<br>*(1. Tính Đóng gói (Encapsulation): Toàn bộ thuộc tính nhạy cảm là Private, có Getter/Setter kiểm soát logic hợp lý.)* | 0.5 | **0.5** |
| | **2. Inheritance:** Build logical Parent-Child classes, minimizing code duplication.<br>*(2. Tính Kế thừa (Inheritance): Xây dựng lớp Cha - Con hợp lý, giảm thiểu tối đa việc lặp lại mã nguồn.)* | 0.5 | **0.5** |
| | **3. Polymorphism & Abstraction:** Properly override methods. Use Abstract Class as a template.<br>*(3. Đa hình & Trừu tượng (Polymorph & Abstract): Ghi đè phương thức (Override) đúng cách. Có sử dụng Abstract Class làm khuôn mẫu.)* | 1.0 | **1.0** |
| | **4. Layered Architecture:** Clearly divide into 3 folders: models, services, views. Correct cross-imports.<br>*(4. Phân tầng Kiến trúc (Layered): Phân chia rõ ràng 3 thư mục models, services, views. Lệnh import chéo chuẩn xác.)* | 1.0 | **1.0** |
| | **5. Clean Code (SRP Principle):** Standard naming conventions (CamelCase, snake_case). Each function/class does only one specific job.<br>*(5. Clean Code (Nguyên lý SRP): Đặt tên chuẩn mực (CamelCase, snake_case). Mỗi hàm/lớp chỉ làm một nhiệm vụ duy nhất.)* | 0.5 | **0.5** |
| | **6. Exception Handling:** Catch input or flow errors using try-except. The system does not crash suddenly.<br>*(6. Xử lý ngoại lệ (Exception Handling): Bắt các lỗi nhập liệu hoặc lỗi luồng bằng try-except. Hệ thống không bị crash đột ngột.)* | 0.5 | **0.5** |
| | **7. Basic Requirements (CRUD):** Add, Edit, Delete, and Display list functions work smoothly with clear formatting.<br>*(7. Nghiệp vụ Cơ bản (CRUD): Các tính năng Thêm, Sửa, Xóa và Hiển thị danh sách hoạt động trơn tru, định dạng rõ ràng.)* | 1.0 | **1.0** |
| | **8. Search & Sort:** Return correct search results and accurately sort the list as requested.<br>*(8. Tìm kiếm & Sắp xếp: Trả về đúng kết quả tìm kiếm và sắp xếp danh sách chính xác theo yêu cầu.)* | 1.0 | **1.0** |
| | **9. Permanent Storage (File I/O):** Successfully read and write data from JSON or TXT files. Data is not lost when the app is closed.<br>*(9. Lưu trữ vĩnh viễn (File I/O): Đọc và ghi dữ liệu thành công từ file JSON hoặc TXT. Dữ liệu không bị mất khi tắt app.)* | 1.0 | **1.0** |
| **ADVANCED & OTHER**<br><br>*(NÂNG CAO & KHÁC)*<br><br>**(3.0 pts)** | **10. Complex Transaction Logic:** Successfully process large system operations (calculate cart total, deduct inventory, calculate salary with tax...).<br>*(10. Logic Giao dịch phức tạp: Xử lý thành công các nghiệp vụ hệ thống lớn (tính tiền giỏ hàng, trừ tồn kho, tính lương có áp dụng thuế...).)* | 1.0 | **1.0** |
| | **11. Advanced Statistics & Export:** Group data for statistics (by type, by month) and support exporting reports to files (CSV, PDF...).<br>*(11. Thống kê nâng cao & Export: Nhóm dữ liệu để thống kê (theo loại, theo tháng) và hỗ trợ xuất báo cáo ra file (CSV, PDF...).)* | 1.0 | **1.0** |
| | **12. Advanced Technology:** Use SQLite Database (instead of standard files) OR design a Graphical User Interface (GUI).<br>*(12. Công nghệ mở rộng: Sử dụng SQLite Database (thay cho File thường) HOẶC thiết kế Giao diện người dùng đồ họa (GUI).)* | 0.5 | **0.5** |
| | **13. Git & GitHub Management:** Have a public GitHub link. Logical and continuous commit history. Have a README.md file with run instructions.<br>*(13. Quản lý Git & GitHub: Có link GitHub công khai. Lịch sử commit logic và liên tục. Có tệp README.md hướng dẫn khởi chạy.)* | 0.5 | **0.5** |
| **TOTAL** | **Đầy đủ 13 tiêu chí — Hệ thống vận hành hoàn chỉnh đạt kết quả xuất sắc** | **10.0** | **10.0** |


# BÀI CUỐI KỲ: GYM MANAGEMENT SYSTEM (HỆ THỐNG QUẢN LÝ PHÒNG GYM)

* **Học phần:** Phương pháp lập trình  
* **Giảng viên hướng dẫn:** TS. Trần Văn Long  
* **Sinh viên thực hiện:** Lê Thị Anh Thư  
* **Mã số sinh viên (MSSV):** 24S7040012    
* **Đơn vị:** Khoa Tin học — Trường Đại học Sư phạm - Đại học Huế  
* **Thời gian nghiệm thu:** Tháng 6/2026
