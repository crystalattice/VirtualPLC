FROM python:3.12-slim
LABEL authors="codyjackson"
WORKDIR /app

COPY pump.py .

ENV PUMP_NAME="Generic pump"
ENV FLOW_RATE_OUT=0.0
ENV PUMP_HEAD_IN=0.0
ENV DISPLACEMENT=0.0

ENTRYPOINT ["python"]
CMD ["pump.py"]