FROM node:18

ENV POETRY_VENV=/srv/fastapi/.venv


RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip gcc build-essential libssl-dev libffi-dev git openssh-client \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory
WORKDIR /srv/vue

# Copy package.json and package-lock.json (if available)
COPY vue/package*.json .


# Install Node.js dependencies
RUN npm install

# Copy the rest of the application code
COPY ./vue .

WORKDIR /srv/fastapi

COPY fastapi/pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.in-project true
RUN poetry install --no-interaction

ENV PATH="$POETRY_VENV/bin:$PATH"

COPY ./fastapi .

COPY start /srv
RUN chmod +x /srv/start


EXPOSE 8000
EXPOSE 5173

ENTRYPOINT ["/bin/bash", "-c", "source $POETRY_VENV/bin/activate && exec /srv/start"]

