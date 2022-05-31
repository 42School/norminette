FROM python:3.9-alpine

LABEL name="norminette"
LABEL description="42 Norme C linter."
LABEL license="MIT"
LABEL authors="42 <pedago@42.fr>"
LABEL homepage="https://pypi.org/project/norminette/"
LABEL repository="https://github.com/42School/norminette"

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
