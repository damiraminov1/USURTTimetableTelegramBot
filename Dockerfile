FROM python:3.11-slim-buster
WORKDIR /usurt_timetable_telegram_bot
COPY . .
RUN pip install poetry==1.5.0
RUN poetry install
ENTRYPOINT ["bash", "entrypoint.sh"]