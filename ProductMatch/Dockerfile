FROM python:3.8-slim

WORKDIR /workspace
COPY . ./

RUN useradd -ms /bin/bash vscode
RUN chown -R vscode /workspace
USER vscode

RUN pip install --no-cache-dir -r .devcontainer/requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
