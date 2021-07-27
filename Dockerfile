FROM python:3.8-slim-buster

ENV FLASK_APP=prognoz
WORKDIR /app

COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 5555

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5555"]
