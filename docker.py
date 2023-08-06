import subprocess
from decouple import config


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

def run_docker_compose():
    # docker compose --env-file prod.env up 
    command = ["docker", "compose", "--env-file", "", "up"]
    if DEBUG:
        command[3] = "dev.env"
    else:
        command[3] = "prod.env"
    try:
        subprocess.call(command)
    except subprocess.CalledProcessError as cpe:
        print(cpe)
    

run_docker_compose()