#!/bin/bash
current_datetime=$(date +"%H%M%d%m%Y")

echo $(date +"%H"":""%M"" ""%d""-""%m""-%Y")
echo
echo "# Get in right directory"
cd /home/laurens/Somtoday_Agendas/Laurens

echo

echo "# Commit local changes"
git add Logs/Laurens.log Logs/Madelief.log
git commit -m "$current_datetime" || echo "No changes to commit"

echo

echo "# Get up to date"
git pull --rebase || (echo "Error: Resolving conflicts"; git rebase --abort)

echo

echo "# Run main file"
sudo python3 /home/laurens/Somtoday_Agendas/Laurens/main.py
echo "Done"

echo  
echo
