#!/bin/bash
#!/bin/sh
while [ 1 ]
do
	rm -f /var/lib/virtdc/logs/monitor_logs/domain/*
	rm -f /var/lib/virtdc/logs/monitor_logs/host/*
	sleep 86400
	
done
exit 0

