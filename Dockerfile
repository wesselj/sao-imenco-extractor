## 1. Selecting the base image with the appropriate Python version

FROM python:3.10-slim
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
build-essential gcc


## 2. Adding a group and a python user to that group

RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python


## 3. Creating a working directory owned by the python user

RUN mkdir /usr/src/app && chown python:python /usr/src/app
WORKDIR /usr/src/app

## 4. Copying requirements

COPY --chown=python:python pyproject.toml .


## 5. Poetry install

RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install


## 6. Copying the app code

COPY --chown=python:python imenco_extractor ./imenco_extractor


## 7. Actually selecting our python user to run the extractor

USER 999

ENTRYPOINT ["poetry", "run", "imenco_extractor"]