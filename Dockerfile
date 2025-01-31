FROM python-3.14.0a4-slim-bookworm

WORKDIR /openroomsfinder
COPY . /openroomsfinder

RUN pip install -r requirements.txt

CMD ["python", "routes.py"]
EXPOSE 8080