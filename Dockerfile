FROM python:3.9-alpine

ARG USR=norme
RUN adduser -S $USR
USER $USR

ARG LOCDIR=/home/$USR/.local/bin
ENV PATH="${LOCDIR}:${PATH}"

WORKDIR /usr/local/bin/norminette

COPY pyproject.toml LICENSE README.md ./
COPY norminette/ ./norminette

RUN pip3 --disable-pip-version-check install --user .

WORKDIR /code

ENTRYPOINT ["norminette"]
