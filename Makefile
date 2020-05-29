stg:
	php artisan config:clear
	npm run dev
	sls deploy --force
prod:
	php artisan config:clear
	npm run prod
	sls deploy --force --stage prod
ssm:
	# EXAMPLE: make key=SLACK_TOKEN value=xoxp-00000000000000-abcdef ssm
	aws ssm put-parameter --name ${key} --type "String" --region ap-northeast-1 --overwrite --value ${value} --profile umihico
