FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ARG user=django-user
RUN adduser --disabled-password $user

RUN mkdir -p /app && \
    chown -R $user /app

COPY requirements.txt /app/requirements.txt

USER $user
ENV PATH="/home/$user/.local/bin:/usr/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]