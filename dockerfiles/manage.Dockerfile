FROM python

ARG CMPDBOT_DIR

WORKDIR $CMPDBOT_DIR

COPY requirements requirements

RUN pip install --upgrade pip && \
    pip install -r requirements/requirements-botcommon.txt && \
    pip install -r requirements/requirements-manage.txt

COPY botvars botvars
COPY code/botcommon code/botcommon
COPY code/manage code/manage
COPY code/setup-manage.py code/setup-manage.py

WORKDIR $CMPDBOT_DIR/code

RUN python setup-manage.py install

ENV PYTHONPATH $CMPDBOT_DIR/code
