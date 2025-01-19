sudo rm /home/laurens/Somtoday_Agendas/Logs/Laurens.log /home/laurens/Somtoday_Agendas/Logs/Madelief.log

sudo touch /home/laurens/Somtoday_Agendas/Logs/Laurens.log
sudo touch /home/laurens/Somtoday_Agendas/Logs/Madelief.log

sudo bash /home/laurens/Somtoday_Agendas/Logs/.LogChecker/Restart.sh

sudo bash /home/laurens/Somtoday_Agendas/Laurens/run.sh >> /home/laurens/Somtoday_Agendas/Logs/Laurens.log 2>&1
sudo bash /home/laurens/Somtoday_Agendas/Madelief/run.sh >> /home/laurens/Somtoday_Agendas/Logs/Madelief.log 2>&1
