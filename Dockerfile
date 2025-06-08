FROM python:3.11-slim
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install uv

WORKDIR /app
COPY requirements.txt .
RUN uv pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
