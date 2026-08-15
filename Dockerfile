FROM python:3.12-slim

WORKDIR /lab
COPY . .

CMD ["python", "evaluate.py", "reference/cache.py"]
