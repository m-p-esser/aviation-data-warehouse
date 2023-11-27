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

RUN pip install --no-cache-dir -r requirements.txt

# ENTRYPOINT ["poetry", "run", "prefect", "worker", "start", "--pool", "dev-docker-work-pool" "--type", "docker"]