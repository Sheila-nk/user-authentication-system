FROM python:3.9-slim

COPY . /user-authenticator

WORKDIR /user-authenticator

RUN pip install -r requirements.txt --default-timeout=100

ENV FLASK_APP=run.py

EXPOSE 5001

RUN ["chmod", "+x", "./commands.sh"]

ENTRYPOINT ["./commands.sh"]