FROM python:3
COPY http_api.py /
COPY settings.py /
EXPOSE 5000
ENTRYPOINT ["python3", "http_api.py"]
