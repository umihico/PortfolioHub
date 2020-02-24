import os
import boto3
import yaml

if os.getenv("ENV", "local") == "local":
    session = boto3.Session(profile_name='umihico')
    ssm = session.client('ssm')
    with open('local.yml') as file:
        for key, value in yaml.safe_load(file).items():
            os.environ[key] = str(value) if isinstance(value, int) or not value.startswith(
                "${ssm:") else ssm.get_parameter(Name=value[6:-1])['Parameter']['Value']


def test_get():
    keys = [
        "GITHUB_TOKEN",
        "CHROMELESS_URL",
        "CHROMELESS_APIKEY",
        "MYSQL_HOST",
        "MYSQL_USER",
        "MYSQL_ROOT_PASSWORD",
        "MYSQL_PORT",
    ]
    for key in keys:
        print(os.environ[key])


if __name__ == '__main__':
    test_get()
