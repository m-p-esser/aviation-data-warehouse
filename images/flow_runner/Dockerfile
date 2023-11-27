ARG PYTHON_VERSION

################################
# Install Prefect, Linux OS and Python
################################

FROM prefecthq/prefect:2.13-python3.10

# ################################
# # Install Poetry
# ################################

# ARG POETRY_VERSION

# RUN pip install poetry==1.5.1

################################
# Copy Files and Directories
################################

WORKDIR /opt/prefect/aviation-data-warehouse
# COPY .env pyproject.toml poetry.lock ./
COPY requirements.txt .env ./
ADD src src
ADD .secrets .secrets
# #  Poetry will complain if a README.md is not found
# RUN touch README.md

# ################################
# # Install Project dependencies
# ################################

# ENV POETRY_NO_INTERACTION=1 \
#     POETRY_VIRTUALENVS_IN_PROJECT=1 \
#     POETRY_VIRTUALENVS_CREATE=1 \
#     POETRY_CACHE_DIR=/tmp/poetry_cache

# RUN poetry install --without dev && rm -rf $POETRY_CACHE_DIR
RUN pip install --no-cache-dir -r requirements.txt

# ENTRYPOINT ["poetry", "run", "prefect", "worker", "start", "--pool", "dev-docker-work-pool" "--type", "docker"]