FROM python:3.7.2-alpine
WORKDIR /api
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]