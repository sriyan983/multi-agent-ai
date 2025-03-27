FROM python:3.10
WORKDIR /app

COPY workflow /app

RUN pip install --no-cache-dir -r requirements.txt
#RUN apt update && apt install -y postgresql-client

# Set FLASK_APP
ENV FLASK_APP=main.py

EXPOSE 5000
#CMD ["python", "main.py"]
CMD tail -f /dev/null