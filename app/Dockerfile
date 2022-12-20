FROM python:3.9

# Configure python
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

ARG REQUIREMENT='requirements.txt'

# get packages
COPY $REQUIREMENT /tmp/
RUN pip install --no-cache-dir -r /tmp/$REQUIREMENT

# Make Volume dir . /app/
RUN mkdir -p /app/src/app
WORKDIR /app/src
EXPOSE 8080

CMD ["python", "app/main.py"]
