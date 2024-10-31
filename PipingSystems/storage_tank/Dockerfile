FROM python:3.12-slim
LABEL authors="codyjackson"
WORKDIR /app

COPY ../../utility_formulas.py .
COPY ./PipingSystems/storage_tank/tank.py .

ENTRYPOINT ["python"]
CMD ["tank.py"]