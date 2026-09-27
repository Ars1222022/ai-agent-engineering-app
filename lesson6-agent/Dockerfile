FROM python:3.12-slim

WORKDIR /workspace

COPY requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY . /workspace

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LMSTUDIO_BASE_URL=http://host.docker.internal:1234/v1

CMD ["python", "lab_launcher.py"]