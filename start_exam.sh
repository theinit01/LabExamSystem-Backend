#!/usr/bin/env bash
# bring up WireGuard, Pi-hole, vpn-monitor
docker compose --profile exam up -d
echo "$(date): exam services started" >> /var/log/exam-switch.log
