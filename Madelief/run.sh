#!/bin/bash
current_datetime=$(date +"%H%M%d%m%Y")

echo $(date +"%H"":""%M"" ""%d""-""%m""-""%Y")
echo
echo "# Get in right directory"
cd /home/laurens/Somtoday_Agendas

echo

echo "# Get up to date"
git add -A
git commit -q -m "$current_datetime"
sudo git pull 

echo

echo "# Run main file"
sudo python3 /home/laurens/Somtoday_Agendas/Madelief/main.py
echo "# Done"

echo  
echo
