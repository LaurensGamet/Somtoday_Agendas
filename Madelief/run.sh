#!/bin/bash
current_datetime=$(date +"%H%M%d%m%Y")

echo $(date +"%H"":""%M"" ""%d""-""%m""-%Y")
echo
echo "# Get in right directory"
cd /home/laurens/Somtoday_Agendas/

echo

echo "# Commit local changes"
git add . || echo "Nothing to stage"
git commit -m "$current_datetime" || echo "No changes to commit"

echo

echo "# Ensure clean working directory"
git status --porcelain | grep '^ M' && echo "Unstaged changes detected. Staging them now..." && git add .
git status --porcelain | grep '^ M' && echo "Committing unstaged changes..." && git commit -m "$current_datetime" || echo "Working directory clean"

echo

echo "# Get up to date"
git pull --rebase || (echo "Error during pull, resetting changes"; git reset --hard HEAD)

echo

echo "# Run main file"
sudo python3 /home/laurens/Somtoday_Agendas/Madelief/main.py
echo "# Done"

echo  
echo
