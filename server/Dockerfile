FROM python:3.8.17-alpine3.17
RUN apk update && apk add --no-cache git
ARG GITHUB_TOKEN
RUN git clone https://JonathanRSinuco:${GITHUB_TOKEN}@github.com/JonathanRSinuco/agfzb-CloudAppDevelopment_Capstone.git /app
WORKDIR /app/server
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python3","manage.py","runserver","0.0.0.0:8000"]