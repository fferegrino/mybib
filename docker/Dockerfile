FROM python:3.6-alpine
ENV PATH ${PATH}:/root/.local/bin
WORKDIR /code
COPY Pipfile Pipfile.lock ./
COPY mybib ./mybib
RUN pip install --user pipenv && \
    pipenv install --system --deploy
CMD ["gunicorn", "--chdir", "mybib/web", "--reload", "app:app", "-b :8000"]

