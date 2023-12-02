################################
# Install Prefect, Linux OS and Python

################################
ARG PYTHON_VERSION

FROM python:${PYTHON_VERSION}-slim-bookworm 

################################
# Init Work Dir
################################

ARG GCP_PROJECT_ID

WORKDIR /opt/prefect/${GCP_PROJECT_ID}

################################
# Install Project dependencies
################################

COPY requirements.txt .env ./
RUN pip install --no-cache-dir -r requirements.txt

################################
# Copy Files and Directories
################################

COPY src .
COPY .secrets .
