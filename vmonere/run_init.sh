while [ ! -e /var/lib/virtdc/vmonere/guest ]
do
	sleep 10
done

/var/lib/virtdc/vmonere/guest/vmonere_agent.py &
