FROM python:3.6
WORKDIR /app
COPY . /app/

RUN pip3 install --requirement ./requirements.txt
EXPOSE 5000

CMD [ "python3", "./app/app.py", "--host"]