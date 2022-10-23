#!/bin/bash
sudo docker-compose build
sleep 10s
sudo docker-compose up rabbitmq
sleep 15s
sudo docker-compose up ascii-server
sleep 10s
sudo docker-compose up telebot