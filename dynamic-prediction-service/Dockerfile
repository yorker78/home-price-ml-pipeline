FROM python:3.12-slim

WORKDIR /app
COPY home_event.py /app/
COPY prediction_service.py /app/
COPY transformers.py /app/

RUN pip3 install -U pip wheel
RUN pip3 install "psycopg[binary]" flask marshmallow scikit-learn==1.8.0 dill pandas

CMD ["python3", "prediction_service.py"]