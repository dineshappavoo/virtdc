while [ ! -e /var/lib/virtdc/vmonere/guest ]
do
	sleep 10
done

/usr/bin/python /var/lib/virtdc/vmonere/guest/vmonere_agent.py &
