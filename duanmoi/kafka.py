from kafka import KafkaProducer, KafkaConsumer
import pandas as pd
import json
import time
import os
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc file CSV
csv_file = "motchill.csv"
data = pd.read_csv(csv_file)

# Loại bỏ các giá trị thiếu (NaN)
data.dropna(inplace=True)

# Thay 'unknow' trong cột 'daodien' và 'quocgia' bằng None
data['daodien'] = data['daodien'].replace('unknow', None)
data['quocgia'] = data['quocgia'].replace('unknow', None)

# Tạo Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all',  # Đảm bảo dữ liệu đã được ghi vào Kafka
    retries=3  # Thử lại tối đa 3 lần nếu gửi thất bại
)

# Hàm gửi dữ liệu vào Kafka
def send_to_kafka(message):
    try:
        producer.send('movie_data', value=message).get(timeout=30)
        print(f"Sent: {message}")
        time.sleep(0.1)
    except Exception as e:
        print(f"Error sending data to Kafka: {e}")

# Sử dụng ThreadPoolExecutor để gửi dữ liệu nhanh hơn
with ThreadPoolExecutor(max_workers=5) as executor:
    for index, row in data.iterrows():
        message = row.to_dict()
        executor.submit(send_to_kafka, message)

# Tạo Kafka Consumer
consumer = KafkaConsumer(
    'movie_data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    group_id='movie_consumer_group'
)

# File CSV dùng để lưu dữ liệu đã xử lý
output_csv_file = "processed_tblmotchill.csv"
seen_messages = set()  # Để kiểm tra trùng lặp
batch_data = []  # Dữ liệu lưu tạm thời
batch_size = 100  # Kích thước batch

try:
    for message in consumer:
        data = message.value
        unique_id = data.get('tenphim')  # Thay thế 'tenphim' bằng cột đại diện duy nhất trong file của bạn

        if unique_id not in seen_messages:
            seen_messages.add(unique_id)
            batch_data.append(data)

            if len(batch_data) >= batch_size:
                df = pd.DataFrame(batch_data)

                # Thay 'unknow' trong cột 'daodien' và 'quocgia' bằng None
                df['daodien'] = df['daodien'].replace('unknow', None)
                df['quocgia'] = df['quocgia'].replace('unknow', None)

                # Ghi dữ liệu vào file CSV
                df.to_csv(output_csv_file, mode='a', index=False, header=not os.path.exists(output_csv_file))
                print(f"Appended {len(batch_data)} new records to {output_csv_file}.")
                
                # Reset batch_data
                batch_data = []

                # Commit offset sau khi xử lý batch
                consumer.commit()
except KeyboardInterrupt:
    print("Consumer stopped manually.")
except Exception as e:
    print(f"Error: {e}")
finally:
    consumer.close()
    print("Kafka Consumer stopped.")
