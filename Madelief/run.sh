#!/bin/bash
current_datetime=$(date +"%H%M%d%m%Y")

echo $(date +"%H"":""%M"" ""%d""-""%m""-""%Y")
echo
echo "# Get in right directory"
cd /home/laurens/Somtoday_Agendas

sudo python3 /home/laurens/Somtoday_Agendas/.indexlockcheck.py

sleep 5

echo

echo "# Get up to date"
#sudo git add -A --ignore-errors
#sudo git commit -q --allow-empty -m "$current_datetime"
#sudo git push
sudo git pull 

echo

echo "# Run main file"
sudo python3 /home/laurens/Somtoday_Agendas/Madelief/main.py
echo "Done"

echo  
echo
