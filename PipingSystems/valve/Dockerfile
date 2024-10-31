FROM python:3.12-slim
LABEL authors="codyjackson"
WORKDIR /app

COPY valve.py .

ENV VALVE_NAME="Generic valve"
ENV INLET_PRESSURE=0
ENV OUTLET_PRESSURE=0
ENV FLOW_COEFFICIENT=0

ENTRYPOINT ["python"]
CMD ["valve.py"]