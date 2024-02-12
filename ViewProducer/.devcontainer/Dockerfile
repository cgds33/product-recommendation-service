FROM python:3.8-slim

WORKDIR /workspace
COPY . ./

RUN useradd -ms /bin/bash vscode
RUN chown -R vscode /workspace
USER vscode

RUN pip install --no-cache-dir -r .devcontainer/requirements.txt
