FROM python:3.6

RUN apt-get update && apt-get install mongodb -y
RUN service mongodb start

COPY . ./app

WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 5000

CMD gunicorn -w 1 -b 0.0.0.0 surveys.app