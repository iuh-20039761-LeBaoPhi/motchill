# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3

WORKDIR /usr/src/app
# Install pip requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt


COPY . .

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers


# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["sh", "-c", "sleep 60 && python -m scrapy runspider duanmoi/spiders/mysraper.py"]
