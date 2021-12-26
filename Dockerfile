FROM python:3


USER root
# ENV PYTHONBUFFERED 1
# ENV PYTHONWRITEBYTECODE 1

# Netcat is a computer networking utility for reading from and writing to network 
# connections using TCP or UDP. Netcat is designed to be a dependable back-end that 
# can be used directly or easily driven by other programs and scripts.
RUN apt-get update && apt-get install -y netcat

# create an app user in the appgroup
# RUN useradd --user-group --create-home --no-log-init --shell /bin/bash app
RUN adduser app
RUN usermod -aG sudo app
RUN echo '%app  ALL=(ALL:ALL) ALL' >> /etc/sudoers
RUN mkdir -p /home/app/web
RUN chown -R app:app /home/app/web
RUN chmod -R 775 /home/app/

USER app
# set environment variable
ENV APP_HOME=/home/app/web
# set the following dir as working dir
WORKDIR $APP_HOME
RUN pip install --upgrade pip
# COPY ./requirements.txt $APP_HOME
# RUN pip install -r requirements.txt
# COPY . $APP_HOME

# USER root
# RUN chown -R app:app $APP_HOME
# WORKDIR $APP_HOME

# USER app -s /usr/bin/bash
# USER app
ENV VIRTUAL_ENV=/home/app/first_try_env
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# RUN pip install --upgrade pip
COPY requirements.txt $APP_HOME
RUN pip install -r requirements.txt
COPY . $APP_HOME


USER root
RUN mkdir -p $APP_HOME/static
RUN mkdir -p $APP_HOME/postgres_docker_data

RUN chown -R app:app $APP_HOME/static
RUN chown -R app:app $APP_HOME/postgres_docker_data

RUN chmod 775 $APP_HOME/static
RUN chmod 775 $APP_HOME/postgres_docker_data
# setting permissions
# RUN chown -R app:app $APP_HOME

USER app:app

# run this script after the creating of the container
ENTRYPOINT [ "/home/app/web/entrypoint.sh" ]









# FROM python:3

# ENV PYTHONBUFFERED 1
# ENV PYTHONWRITEBYTECODE 1

# # Netcat is a computer networking utility for reading from and writing to network 
# # connections using TCP or UDP. Netcat is designed to be a dependable back-end that 
# # can be used directly or easily driven by other programs and scripts.
# RUN apt-get update && apt-get install -y netcat

# # create an app user in the appgroup
# RUN useradd --user-group --create-home --no-log-init --shell /bin/bash app

# # set environment variable
# ENV APP_HOME=/home/app/web

# RUN mkdir -p $APP_HOME/static

# # set the following dir as working dir
# WORKDIR $APP_HOME

# # RUN mkdir /code
# COPY requirements.txt $APP_HOME
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
# COPY . $APP_HOME

# # setting permissions
# RUN chown -R app:app $APP_HOME

# USER app:app

# # run this script after the creating of the container
# ENTRYPOINT [ "/home/app/web/entrypoint.sh" ]