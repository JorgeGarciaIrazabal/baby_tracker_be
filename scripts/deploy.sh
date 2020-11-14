#!/bin/bash
cd /home/jirazabal/code/baby_tracker_fe
npm run build
tar -czvf dist.tar.gz dist
mv dist.tar.gz  /home/jirazabal/code/baby_tracker_be/dist.tar.gz


cd /home/jirazabal/code/baby_tracker_be
git add dist.tar.gz
#git commit -m "Upgrade frontend"
#git push origin main
