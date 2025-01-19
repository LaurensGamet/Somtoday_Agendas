#!/bin/bash
current_datetime=$(date +"%H%M%d%m%Y")

echo $(date +"%H"":""%M"" ""%d""-""%m""-""%Y")
echo
echo "# Get in right directory"
cd /home/laurens/Somtoday_Agendas/Laurens

echo

echo "# Get up to date"
sudo git pull 

echo

echo "# Run main file"
sudo python3 /home/laurens/Somtoday_Agendas/Laurens/main.py
echo "# Done"

echo  
echo  

