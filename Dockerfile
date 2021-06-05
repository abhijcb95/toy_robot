FROM python:3.9
RUN pip install Flask==1.1.2
RUN pip install gunicorn==20.0.4
RUN pip install google-cloud-firestore==2.0.2
