FROM node:18


RUN apt-get update \
    && apt-get install -y --no-install-recommends curl python3 python3-pip gcc build-essential libssl-dev libffi-dev git openssh-client \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Set the working directory
WORKDIR /srv/vue

# Copy package.json and package-lock.json (if available)
COPY vue/package*.json .


# Install Node.js dependencies
RUN npm install

# Copy the rest of the application code
COPY ./vue .

WORKDIR /srv/fastapi

COPY fastapi/requirements.txt ./

RUN exec bash

RUN $HOME/.cargo/bin/uv venv

ENV VIRTUAL_ENV=/srv/fastapi/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN $HOME/.cargo/bin/uv pip install -r requirements.txt

COPY ./fastapi .

COPY start /srv
RUN chmod +x /srv/start

EXPOSE 8000
EXPOSE 5173

