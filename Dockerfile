FROM python:3.11

ARG APP_DIR
ARG APP_PORT
ARG DEBIAN_FRONTEND=noninteractive

ENV UVICORN_PORT=$APP_PORT
ENV TZ=Asia/Seoul

# Expose the application port
EXPOSE ${UVICORN_PORT}

# Set the working directory
WORKDIR ${APP_DIR}

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx

# Copy application files
ADD ./requirements.txt ${APP_DIR}/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Set the command to run the application
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${UVICORN_PORT}"]
