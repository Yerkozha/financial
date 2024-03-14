FROM python:3.10-slim

RUN mkdir /app

COPY ./ ./app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip && pip3 install -r ./app/requirements.txt --no-cache-dir

WORKDIR /app

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh


ENTRYPOINT ["/app/entrypoint.sh"]

