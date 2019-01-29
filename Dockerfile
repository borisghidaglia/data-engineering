FROM python:3.6

RUN mkdir /code
WORKDIR /code

COPY . .

RUN pip install --upgrade pip && pip install pipenv && pipenv install

CMD ["pipenv", "run", "python" , "run.py"]t
