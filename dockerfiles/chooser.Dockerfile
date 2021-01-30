FROM python

ARG CMPDBOT_DIR

WORKDIR $CMPDBOT_DIR

COPY requirements requirements

RUN pip install --upgrade pip && \
    pip install -r requirements/requirements-botcommon.txt && \
    pip install -r requirements/requirements-chooser.txt

COPY botvars botvars
COPY code/botcommon code/botcommon
COPY code/chooser code/chooser

ENV PYTHONPATH $CMPDBOT_DIR/code

CMD ["python", "-m", "chooser"]
