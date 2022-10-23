#!/bin/bash
docker-compose build
sleep 10s
docker-compose up rabbitmq
sleep 15s
docker-compose up ascii-server
sleep 10s
docker-compose up telebot