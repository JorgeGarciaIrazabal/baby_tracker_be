source /home/jirazabal/.my_bashrc
cd /home/jirazabal/repos/baby_tracker_fe
git fetch origin
git reset --hard origin/main
cd /home/jirazabal/repos/baby_tracker_be
git fetch origin
git reset --hard origin/main

echo "killing python"
pkill python

/home/jirazabal/scripts/startup_script.sh &
echo "extracting dist"
rm -rf /home/jirazabal/repos/baby_tracker_fe/dist
mkdir /home/jirazabal/repos/baby_tracker_fe/dist
tar -xzvf /home/jirazabal/repos/baby_tracker_fe/dist.tar.gz -C /home/jirazabal/repos/baby_tracker_fe
# rm -rf /home/jirazabal/repos/baby_tracker_fe/dist.tar.gz
echo "killing node"
pkill node

cd /home/jirazabal/repos/baby_tracker_fe
npm run start &
