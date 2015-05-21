FROM checkio/code-empire-dev-base
MAINTAINER Igor Lubimov <igor@checkio.org>

ENV DB_NAME code_empire

COPY root/.ssh /root/.ssh
RUN chmod 400 /root/.ssh/*

COPY requirements /opt/project/
RUN pip-accel install -r /opt/project/back/development.txt

# TODO: move to env
RUN pip-accel install -r /opt/project/async/requirements.txt

RUN mkdir /opt/db && \
    chown -R postgres /opt/db
COPY dump.sql /opt/db/dump.sql
USER postgres
RUN /etc/init.d/postgresql start && \
    psql $DB_NAME < /opt/db/dump.sql

USER root
RUN rm -rf /opt/db/*

RUN rm -rf /etc/nginx/conf.d/*
COPY etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf
COPY etc/nginx/conf.d/queue-monitor.conf /etc/nginx/conf.d/queue-monitor.conf
COPY etc/nginx/conf.d/code-empire.conf /etc/nginx/conf.d/code-empire.conf

COPY etc/apache2/ports.conf /etc/apache2/ports.conf
COPY etc/apache2/sites-available/code-empire.conf /etc/apache2/sites-available/code-empire.conf
RUN mkdir -p /etc/apache2/sites-enabled
RUN ln -s /etc/apache2/sites-available/code-empire.conf /etc/apache2/sites-enabled/code-empire.conf

COPY scripts/init.sh /opt/init.sh
COPY scripts/init-django.sh /opt/init-django.sh
COPY scripts/build-static.sh /opt/build-static.sh
COPY scripts/backup-db.sh /opt/backup-db.sh
RUN chmod 755 /opt/init.sh && \
    chmod 755 /opt/init-django.sh && \
    chmod 755 /opt/build-static.sh && \
    chmod 755 /opt/backup-db.sh && \
    useradd -G www-data -ms /bin/bash checkio

VOLUME /var/lib/postgresql/9.4/main

EXPOSE 80 81 8888 5672 5432

CMD ["/bin/bash", "/opt/init.sh"]
