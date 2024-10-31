FROM python:3.12-slim
LABEL authors="codyjackson"
WORKDIR /app

COPY ../../utility_formulas.py .
COPY ./PipingSystems/pump/pump.py .

ENTRYPOINT ["python"]
CMD ["pump.py"]