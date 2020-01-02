build:
	ssh lightsail "sudo chown -R ec2-user:ec2-user ~/dockers;"
	rsync -achrvzP --delete . lightsail:dockers/portfoliohub.umihi.co/laravel
	ssh lightsail "chmod -R 777 ~/dockers;cd ~/dockers/lemp;docker-compose restart portfoliohub"
