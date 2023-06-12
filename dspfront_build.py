import docker 
import os
def build(client, DEPLOYMENT_TARGET):
    print(os.getcwd())
    print("Building dspfront")
    print(client.images.build(
        path="./dspfront",
        tag={"dspfront"}
    ))
    client.containers.run(
        name={"dspfront"}, 
        detach=True,
        ports={"5001/tcp":5001} #couldn't find a 'restart_policy' or 'depends_on'
    )

    print("Built dspfront")
def stop(client):
    print("Stopping dspfront")
    container = client.containers.get("dspfront")
    container.stop()
    print("Stopped dspfront")