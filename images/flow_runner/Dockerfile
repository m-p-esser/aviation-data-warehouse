################################
# Install Prefect, Linux OS and Python

################################
ARG PYTHON_VERSION
ARG PREFECT_VERSION

FROM prefecthq/prefect:${PREFECT_VERSION}-python${PYTHON_VERSION}

################################
# Copy Files and Directories
################################

ARG GCP_PROJECT_ID

WORKDIR /opt/prefect/${GCP_PROJECT_ID}

COPY requirements.txt .env ./
ADD src src
ADD .secrets .secrets

# ################################
# # Install Project dependencies
# ################################

RUN python -m venv /venv
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["source", "venv/bin/activate"]