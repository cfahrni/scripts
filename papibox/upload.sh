#!/bin/bash
/usr/bin/sshpass -p '***********' scp /tmp/image.jpg user@hostname:prefix-$(date +"%Y%m%d-%H%M").jpg
