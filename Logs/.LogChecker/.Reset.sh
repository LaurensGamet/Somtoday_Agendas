sudo rm /home/laurens/logs/Somtoday_Laurens.log /home/laurens/logs/Somtoday_Madelief.log

sudo touch /home/laurens/logs/Somtoday_Laurens.log
sudo touch /home/laurens/logs/Somtoday_Madelief.log

sudo bash /home/laurens/logs/.LogChecker/Restart.sh

sudo bash /home/laurens/Somtoday_Laurens/run.sh >> /home/laurens/logs/Somtoday_Laurens.log 2>&1
sudo bash /home/laurens/Somtoday_Madelief/run.sh >> /home/laurens/logs/Somtoday_Madelief.log 2>&1
