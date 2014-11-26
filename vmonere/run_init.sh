## This init script is run on guest

while [ ! -e /var/lib/virtdc/vmonere/guest/host_config.txt ]
do
	sleep 5
done

/usr/bin/python /var/lib/virtdc/vmonere/guest/vmonere_agent.py &
