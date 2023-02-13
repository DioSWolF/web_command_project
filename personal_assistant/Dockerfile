FROM python:3.10.8

WORKDIR F:\web_command_project\personal_assistant

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD [ "python", "manage.py", "runserver" ] 