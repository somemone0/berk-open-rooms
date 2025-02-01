FROM amancevice/pandas:slim-2.2.2

WORKDIR /openroomsfinder
COPY . /openroomsfinder

RUN pip install -r requirements.txt
EXPOSE 8080
RUN python

CMD ["python", "routes.py"]
