FROM python:3.7-alpine

# Install dependencies:
RUN pip install pipenv
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile

# Run the application:
COPY *.py ./
# Don't add secrets )
# COPY *.json ./
COPY *.tsv ./
CMD ["python", "run.py"]