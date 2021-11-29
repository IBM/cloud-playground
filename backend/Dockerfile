FROM python:3

COPY backend /backend
COPY common /backend/common
WORKDIR /backend
RUN mkdir -p /backend/work  \
    && python3 -m pip install -r ./requirements.txt
ENV PYTHONPATH=/backend
EXPOSE 5000

ENTRYPOINT [ "python3", "app/start.py" ]
