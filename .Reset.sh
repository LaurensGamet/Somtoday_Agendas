#!/bin/bash

sudo rm /home/laurens/Somtoday_Agendas/Logs/Laurens.log /home/laurens/Somtoday_Agendas/Logs/Madelief.log

sudo touch /home/laurens/Somtoday_Agendas/Logs/Laurens.log
sudo touch /home/laurens/Somtoday_Agendas/Logs/Madelief.log

sudo bash /home/laurens/Somtoday_Agendas/.Restart.sh
