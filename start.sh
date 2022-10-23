#!/bin/bash
sudo docker-compose build
sleep 10s
chown rabbitmq:rabbitmq /var/lib/rabbitmq/mnesia
sudo docker-compose up rabbitmq &
sleep 50s
sudo docker-compose up ascii-server &
sleep 10s
sudo docker-compose up telegram-bot &
