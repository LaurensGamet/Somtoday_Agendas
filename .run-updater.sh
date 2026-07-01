#!/bin/bash

sudo python3 /mnt/c/Users/laure/OneDrive/Documenten/Somtoday_Agendas/.indexlockcheck.py

sleep 5

sudo bash /mnt/c/Users/laure/OneDrive/Documenten/Somtoday_Agendas/Laurens/run.sh >> /mnt/c/Users/laure/OneDrive/Documenten/Somtoday_Agendas/Logs/Laurens.log 2>&1

sleep 10

sudo bash /mnt/c/Users/laure/OneDrive/Documenten/Somtoday_Agendas/Madelief/run.sh >> /mnt/c/Users/laure/OneDrive/Documenten/Somtoday_Agendas/Logs/Madelief.log 2>&1

sleep 10

sudo bash /mnt/c/Users/laure/OneDrive/Documenten/Somtoday_Agendas/Loukas/run.sh >> /mnt/c/Users/laure/OneDrive/Documenten/Somtoday_Agendas/Logs/Loukas.log 2>&1
