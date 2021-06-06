FROM python:3.8
RUN pip3 install Flask==1.1.2
RUN pip3 install gunicorn==20.0.4
RUN pip3 install google-cloud-firestore==2.0.2
COPY helpers.py /app
COPY main.py /app