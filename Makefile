stg:
	php artisan config:clear
	npm run dev
	gzip -k --best -f public/js/app.js
	aws s3 cp public/js/app.js.gz s3://stg-storage.umihi.co/portfoliohub/asset/js/app.js --content-encoding "gzip" --content-type "text/javascript"
	aws s3 cp public/css/app.css s3://stg-storage.umihi.co/portfoliohub/asset/css/
	sls deploy --force
prod:
	php artisan config:clear
	npm run prod
	gzip -k --best -f public/js/app.js
	aws s3 cp public/js/app.js.gz s3://storage.umihi.co/portfoliohub/asset/js/app.js --content-encoding "gzip" --content-type "text/javascript"
	aws s3 cp public/css/app.css s3://storage.umihi.co/portfoliohub/asset/css/
	sls deploy --force --stage prod
ssm:
	# EXAMPLE: make key=SLACK_TOKEN value=xoxp-00000000000000-abcdef ssm
	aws ssm put-parameter --name ${key} --type "String" --region ap-northeast-1 --overwrite --value ${value} --profile umihico
update:
	composer update
	git add composer*
	git commit -m "composer update"
	git push
	make prod
