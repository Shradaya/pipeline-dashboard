FROM python:3.8-slim

COPY requirements.txt /
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY wsgi.py gunicorn-cfg.py config.py .env entrypoint.sh /
COPY app app 

ENV APP wsgi.py
EXPOSE 8000

CMD ["/bin/bash", "/entrypoint.sh"]