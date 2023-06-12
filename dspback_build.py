import os
import docker
def build(client, DEPLOYMENT_TARGET):
    print(os.getcwd())
    print("Building dspback")
    print(client.images.build(
        path="./dspback",
        tag={"dspback"}
    ))
    client.containers.run(
        name={"dspback"}, 
        detach=True,
        ports={"5002/tcp":5002} #couldn't find a 'restart_policy' or 'depends_on'
    )
def stop(client):
    print("Stopping dspback")
    container = client.containers.get("dspback")
    container.stop()
    print("Stopped dspback")