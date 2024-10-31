FROM python:3.12-slim
LABEL authors="codyjackson"
WORKDIR /app

COPY . .

ENTRYPOINT ["python"]
CMD ["Models/FuelFarm/components.py"]