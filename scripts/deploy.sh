#!/bin/bash
cd /home/jirazabal/code/baby_tracker_fe
npm run build
tar -czvf dist.tar.gz dist
scp dist.tar.gz root@vps65488.inmotionhosting.com:/home/jirazabal/repos/baby_tracker_fe

rm -rf dist.tar.gz

ssh root@vps65488.inmotionhosting.com "chmod 777 /home/jirazabal/repos/baby_tracker_fe/dist.tar.gz"
ssh root@vps65488.inmotionhosting.com "sudo -H -u jirazabal bash -c 'bash /home/jirazabal/scripts/deploy_script.sh'"
