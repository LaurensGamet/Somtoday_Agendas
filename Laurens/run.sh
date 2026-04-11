#!/bin/bash
current_datetime=$(date +"%H%M%d%m%Y")

echo $(date +"%H"":""%M"" ""%d""-""%m""-""%Y")
echo
echo "# Get in right directory"
cd /mnt/c/Users/laure/OneDrive/Documenten/Somtoday_Agendas

if [ -f "/mnt/c/Users/laure/OneDrive/Documenten/Somtoday_Agendas/.git/index.lock" ]; then
    sudo rm -f /mnt/c/Users/laure/OneDrive/Documenten/Somtoday_Agendas/.git/index.lock
fi

echo

echo "# Get up to date"
#git add -A --ignore-errors
#git commit -q --allow-empty -m "$current_datetime"
sudo git pull 

echo

echo "# Run main file"
sudo python3 /mnt/c/Users/laure/OneDrive/Documenten/Somtoday_Agendas/Laurens/main.py
echo "Done"

echo  
echo
