ARG IMAGE_BASE=python:3.10-alpine
FROM ${IMAGE_BASE} as base
ARG APP_USER=container_user
ENV PATH="/user/home/.local/bin:${PATH}"
ENV PORT=8000
RUN mkdir -p /user && \
    addgroup --gid 1000 ${APP_USER} && \
    adduser --gecos "" --disabled-password --home /user/home/ --shell /bin/sh -u 1000 ${APP_USER} --ingroup ${APP_USER} && \
    apk --no-cache update && \
    apk --no-cache add \
        gcc \
        musl-dev \
        libffi-dev

USER ${APP_USER}
COPY --chown=${APP_USER}:${APP_USER} requirements /tmp/requirements
RUN pip install -r /tmp/requirements/base.txt --user

FROM base as release
ARG APP_USER=container_user
ARG COMMIT=""
ENV PATH="/user/home/.local/bin:${PATH}"
ENV COMMIT=${COMMIT}
ENV REDIS_URL="redis://redis:6379"
WORKDIR /user/home
USER ${APP_USER}
COPY --chown=${APP_USER}:${APP_USER} requirements /tmp/requirements
RUN pip install -r /tmp/requirements/prod.txt --user
COPY --chown=${APP_USER}:${APP_USER} . /user/home
COPY --chown=${APP_USER}:${APP_USER} ./entrypoint.sh /user/home/entrypoint.sh
EXPOSE 8000
ENTRYPOINT ["/user/home/entrypoint.sh"]

FROM release as test
ARG APP_USER=container_user
ENV PATH="/user/home/.local/bin:${PATH}"
WORKDIR /user/home
USER ${APP_USER}
COPY --chown=${APP_USER}:${APP_USER} requirements /tmp/requirements
RUN pip install -r /tmp/requirements/dev.txt --user
ENTRYPOINT ["/user/home/entrypoint.sh"]
