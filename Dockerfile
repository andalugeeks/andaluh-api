FROM python:3.12-slim

LABEL maintainer="felixonta@gmail.com"

RUN mkdir -p /project

COPY ./requirements.txt /project/requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libopenblas-dev gfortran git \
    && pip install --no-cache-dir uwsgi \
    && pip install -r /project/requirements.txt \
    && apt-get purge -y --auto-remove libopenblas-dev gfortran git \
    && apt-get install -y --no-install-recommends nginx supervisor \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --no-create-home nginx

RUN python -c "import verbecc; cg = verbecc.CompleteConjugator(verbecc.LangCodeISO639_1.es); cg.conjugate('ser')"
RUN chmod -R a+rX /usr/local/lib/python3.12/site-packages/verbecc/data

RUN chown -R nginx:nginx /project

RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

COPY nginx.conf /etc/nginx/
COPY flask-site-nginx.conf /etc/nginx/conf.d/
COPY uwsgi.ini /etc/uwsgi/
COPY supervisord.conf /etc/

COPY app /project/app

WORKDIR /project

CMD ["/usr/bin/supervisord"]
