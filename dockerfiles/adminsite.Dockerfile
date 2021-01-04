FROM python

ARG CMPDBOT_DIR

WORKDIR $CMPDBOT_DIR

COPY requirements requirements

RUN pip install --upgrade pip && \
    pip install -r requirements/requirements-adminsite.txt

COPY code/adminsite code/adminsite

ENV PYTHONPATH $CMPDBOT_DIR/code

CMD ["python", "-m", "adminsite"]
