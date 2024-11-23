
#Docker sẽ sử dụng image chính là python:3, phiên bản Python 3, làm nền tảng để xây dựng container.
FROM python:3

#Thiết lập thư mục làm việc mặc định trong container
WORKDIR /usr/src/app
# Install pip requirements

#Sao chép file requirements.txt từ thư mục cục bộ (local) vào thư mục làm việc của container
COPY requirements.txt .

#Chạy lệnh cài đặt các gói Python từ file requirements.txt bằng pip3
RUN pip3 install --no-cache-dir -r requirements.txt

#Sao chép toàn bộ nội dung từ thư mục cục bộ vào thư mục làm việc của container
COPY . .

#Lệnh CMD chỉ định lệnh sẽ được thực thi khi container khởi chạy.
CMD ["sh", "-c", "sleep 60 && python -m scrapy runspider duanmoi/spiders/mysraper.py"]
