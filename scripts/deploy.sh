#!/bin/bash
cd /home/jirazabal/code/baby_tracker_fe
npm run build
tar -czvf dist.tar.gz dist
scp scp dist.tar.gz root@vps65488.inmotionhosting.com:/home/jirazabal/repos/baby_tracker_fe
ssh root@vps65488.inmotionhosting.com "tar -zcvf /home/jirazabal/repos/baby_tracker_fe/dist.tar.gz /home/jirazabal/repos/baby_tracker_fe/dist/"

rm -rf dist.tar.gz


ssh root@vps65488.inmotionhosting.com "sudo -H -u jirazabal bash -c 'bash /home/jirazabal/scripts/deploy_script.sh'"
