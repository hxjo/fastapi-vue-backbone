FROM node:18

ENV UV_VENV=/srv/fastapi/.venv
SHELL ["/bin/bash", "-c"]


RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip gcc build-essential libssl-dev libffi-dev git openssh-client \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Source the cargo env
ENV PATH="/root/.cargo/bin:$PATH"

# Set the working directory
WORKDIR /srv/vue

# Copy package.json and package-lock.json (if available)
COPY vue/package*.json .


# Install Node.js dependencies
RUN npm install

# Copy the rest of the application code
COPY ./vue .

WORKDIR /srv/fastapi

COPY fastapi/pyproject.toml ./
COPY fastapi/requirements* ./

RUN uv venv
ENV PATH="$UV_VENV/bin:$PATH"
RUN uv pip install -r requirements.dev.in


COPY ./fastapi .

COPY start /srv
RUN chmod +x /srv/start


EXPOSE 8000
EXPOSE 5173

ENTRYPOINT ["/bin/bash", "-c", "source $UV_VENV/bin/activate && exec /srv/start"]

