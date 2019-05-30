FROM python:3.7-alpine
# RUN apt-get update && apt-get install \
#   -y --no-install-recommends python3 python3-virtualenv

# ENV VIRTUAL_ENV=/opt/venv
# RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the application:
COPY *.py ./
COPY *.json ./
COPY *.tsv ./
CMD ["python", "run.py"]