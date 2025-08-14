#!/bin/bash

sudo python3 /home/laurens/Somtoday_Agendas/.indexlockcheck.py

sleep 5

sudo bash /home/laurens/Somtoday_Agendas/Laurens/run.sh >> /home/laurens/Somtoday_Agendas/Logs/Laurens.log 2>&1 && sudo bash /home/laurens/Somtoday_Agendas/Madelief/run.sh >> /home/laurens/Somtoday_Agendas/Logs/Madelief.log 2>&1
