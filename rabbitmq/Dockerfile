FROM rabbitmq:3.8.3

ENV RABBITMQ_VERSION=3.8.3

RUN rabbitmq-plugins enable --offline rabbitmq_management
RUN rabbitmq-plugins enable --offline rabbitmq_mqtt
RUN rabbitmq-plugins enable --offline rabbitmq_web_mqtt
RUN rabbitmq-plugins enable --offline  rabbitmq_prometheus
# Fix nodename
RUN echo 'NODENAME=rabbit@localhost' > /etc/rabbitmq/rabbitmq-env.conf

# #todo: What are the different port names for?
# #Also do we need to EXPOSE or forward the port
# # This port Use by rabbitmq websocket
# EXPOSE 15675
# # This port use by mqtt
# EXPOSE 1883
# EXPOSE 8883