FROM python

ARG CMPDBOT_DIR

WORKDIR $CMPDBOT_DIR

COPY requirements requirements

RUN pip install --upgrade pip && \
    pip install -r requirements/requirements-bot.txt && \
    pip install -r requirements/requirements-botcommon.txt

COPY botvars botvars
COPY code/bot code/bot
COPY code/botcommon code/botcommon
COPY extlibs/vishnubob-wait-for-it extlibs/vishnubob-wait-for-it

ENV PYTHONPATH $CMPDBOT_DIR/code

CMD ["python", "-m", "bot"]
