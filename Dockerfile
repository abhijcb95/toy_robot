FROM python:3.8
RUN pip3 install Flask==1.1.2
RUN pip3 install gunicorn==20.0.4
COPY main.py /
COPY helpers.py /