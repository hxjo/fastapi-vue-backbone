FROM node:18


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

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY ./fastapi .

COPY start.sh /srv
RUN chmod +x /srv/start.sh

EXPOSE 8000
EXPOSE 5173
ENTRYPOINT ["/srv/start.sh"]

