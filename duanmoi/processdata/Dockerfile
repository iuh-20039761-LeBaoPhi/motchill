# Sử dụng Python base image
FROM python:3.12-slim

# Cài đặt các công cụ cơ bản
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Jupyter Notebook
RUN pip install --upgrade pip && pip install \
    jupyter \
    pandas \
    numpy \
    matplotlib

# Tạo thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt và cài đặt thư viện
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt


# Sao chép toàn bộ nội dung dự án vào container
COPY . .

# Mở cổng 8888 cho Jupyter Notebook
EXPOSE 8888

# Lệnh khởi động Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
