FROM python:3.12-slim
LABEL authors="codyjackson"
WORKDIR /app

COPY ../../utility_formulas.py .
COPY ./PipingSystems/valve/valve.py .

ENTRYPOINT ["python"]
CMD ["valve.py"]