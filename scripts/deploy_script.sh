source /home/jirazabal/.my_bashrc
cd /home/jirazabal/repos/baby_tracker_fe
git fetch origin
git reset --hard origin/main
cd /home/jirazabal/repos/baby_tracker_be
git fetch origin
git reset --hard origin/main

sudo kill -9 `pgrep python`
/home/jirazabal/scripts/startup_script.sh &

sudo kill -9 `pgrep node`

cd /home/jirazabal/repos/baby_tracker_fe
npm run start &
