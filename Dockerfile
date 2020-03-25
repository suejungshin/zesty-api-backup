FROM python:3.8.2

RUN mkdir -p /src/app

WORKDIR /src/app

COPY . /src/app

COPY wait-for-it.sh wait-for-it.sh

RUN chmod +x wait-for-it.sh

RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD ["./wait-for-it.sh", "postgres:5432", "--", "python3", "index.py"]



