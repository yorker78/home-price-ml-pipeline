FROM python:3.12-slim

WORKDIR /app
COPY *.py /app/

RUN pip3 install -U pip wheel
RUN pip3 install "psycopg[binary]" apscheduler pandas dill scikit-learn==1.8.0

CMD ["python3", "job_runner.py"]