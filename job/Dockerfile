FROM python:3

COPY job /job
COPY common /job/common
WORKDIR /job
RUN mkdir -p /job/work  \
    &&  python3 -m pip install -r ./requirements.txt    \
    &&  python3 -m pip install --upgrade "ibm-vpc>=0.8.0" \
    &&  python3 -m pip install --upgrade "ibm-cos-sdk"
ENV PYTHONPATH=/job

ENTRYPOINT [ "python3", "main.py" ]
