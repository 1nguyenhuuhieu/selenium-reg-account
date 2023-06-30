# Tự động đăng kí tài khoản sử dụng selenium và python v1.0
## 1. Giới thiệu
Tool tự động đăng kí tài khoản tại các trang web chơi game. Tool sẽ lấy thông tin tài khoản ở file excel và địa chỉ các trang web muốn đăng kí tại file txt sau đó lần lượt đăng kí từng tài khoản lên tất cả các trang web. Thông tin tài khoản sau khi đăng kí xong sẽ được lưu vào database.db. Danh sách trang web đã test có trong file webs.txt
## 2. Yêu cầu hệ thống
* Tool được test trên windows 11, 16GB RAM, CPU INTEL CORE I5
* Có thể cài đặt và chạy tốt trên các hệ điều hành khác như MacOS hay Ubuntu
## 3. Cài đặt
* Download và cài đặt [Python phiên bản mới nhất](https://www.python.org/downloads/). Lúc cài đặt check vào mục "Add python to path". Hoặc có thể cài đặt từ thư mục install kèm theo source code này.
* Donwload và cài đặt [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki). Hoặc có thể cài đặt từ thư mục install kèm theo source code này.
* Cài đặt các thư viện cần thiết. Mở Terminal(hoặc CMD), truy cập vào thư mục chứa mã nguồn. Chạy câu lệnh: `pip install -r requirements.txt`. Chờ tới khi quá trình cài đặt hoàn tất
## 4. Sử dụng tool
* Thêm thông tin tài khoản cần đăng kí vào file users.xlsx, **không chỉnh sửa định dạng và hàng đầu tiên**.
* Chỉnh sửa địa chỉ các trang web muốn đăng kí ở file webs.txt, những máy tính cấu hình yếu nên chia nhỏ thành nhiều file. Mỗi lần chỉ nên đăng kí 4-5 trang.
* Mở giao diện bằng cách chạy file tool.
* Điền API KEY mua tại https://tmproxy.com/proxy vào ô API KEY, Chọn file thông tin tài khoản và danh sách trang web tại hai ô kế tiếp. Nhấp Save
* Ấn Run Main để chạy tool
* Để xem kết quả sau khi chạy tool, sử dụng DB Browers, [Download](https://sqlitebrowser.org/dl/). Hoặc có thể cài đặt từ thư mục install kèm theo source code này. Mở phần mềm DB browser và mở file: database.db trong thư mục sourcode để xem thông tin các tài khoản đã được đăng kí thành công

Mọi thắc mắc thêm có thể liên hệ trực tiếp. Hiếu - 1nguyenhuuhieu@gmail.com