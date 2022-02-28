echo "  sleep for 10 sec"
sleep 10
echo "  ifconfig lo:0 172.16.123.1"
sudo ifconfig lo:0 172.16.123.1
echo "  start workload"
docker-compose up -d