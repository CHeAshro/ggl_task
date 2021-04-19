FROM python:3.7
WORKDIR /app 
ADD . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["uwsgi", "--ini", "uwsgi.ini"]
