# lightweight python
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# workdir
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt copy
COPY requirements.txt .

# install python deps
RUN pip install --no-cache-dir -r requirements.txt

# copy rest
COPY . .

# expose  flask
EXPOSE 5000

# run :)
CMD ["pyrhon", "app.py"]
