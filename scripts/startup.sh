#!/bin/bash

ssh root@vps65488.inmotionhosting.com "sudo -H -u jirazabal bash -c 'bash /home/jirazabal/scripts/deploy_script.sh'"

ssh root@vps65488.inmotionhosting.com "systemctl restart baby_tracker"

