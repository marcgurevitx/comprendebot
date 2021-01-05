FROM python

ARG CMPDBOT_DIR

WORKDIR $CMPDBOT_DIR

COPY requirements requirements

RUN pip install --upgrade pip && \
    pip install -r requirements/requirements-adminsite.txt

COPY code/adminsite code/adminsite
COPY extlibs/vishnubob-wait-for-it extlibs/vishnubob-wait-for-it

ENV PYTHONPATH $CMPDBOT_DIR/code

CMD ["python", "-m", "adminsite"]
