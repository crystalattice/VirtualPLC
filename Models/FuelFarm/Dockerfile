# Start with a basic Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy only the components.py file, if it has no dependencies
COPY ./Models/FuelFarm/components.py .
COPY ./PipingSystems /app/PipingSystems

# Optionally, copy utility_formulas.py if needed
COPY utility_formulas.py .

# Default command
ENTRYPOINT ["python"]
CMD ["components.py"]
