#!/usr/bin/env bash
# tear down only the exam services
docker compose --profile exam down
echo "$(date): exam services stopped" >> /var/log/exam-switch.log
