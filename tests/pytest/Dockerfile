FROM python:3.12-slim AS req
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install uv
COPY requirements.txt .
RUN uv pip install -r requirements.txt

FROM python:3.12-slim AS run-tests
COPY --from=req /opt/venv /opt/venv
RUN useradd --create-home nonroot
RUN chown -R nonroot:nonroot /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
USER nonroot
WORKDIR tests
COPY . .
CMD pytest
