import os
import sys
import shutil
import docker
import github3
import git
import dspfront_build
import dspback_build
#from python_on_whales import docker
#from python_on_whales import DockerClient
""""
vars i need:
    HOSTNICK:dev,test,beta,prod,...
    DSP_BRANCH_OR_TAG
    DSPFRONT_BRANCH_OR_TAG
    DSPBACK_BRANCH_OR_TAG

"""

print("Deployment begun") # get a date time 
DEPLOYMENT_TARGET = "./opt/cznethub"
print("DEPLOYMENT_TARGET = './opt/cznethub'")
DEPLOYMENT_SOURCE = "./projects/cznethub/dsp/targets"
print("DEPLOYMENT_SOURCE = './projects/cznethub/dsp/targets'")
HOSTNICK = sys.argv[1]
print("HOSTNICK = {}".format(HOSTNICK))

GITHUB_ORG_URL="https://github.com/cznethub"
print("GITHUB_ORG_URL={}".format(GITHUB_ORG_URL))
DSP_BRANCH_OR_TAG= sys.argv[2]
print("DSP_BRANCH_OR_TAG={}".format(DSP_BRANCH_OR_TAG))
DSPFRONT_BRANCH_OR_TAG=sys.argv[3]
print("DSPFRONT_BRANCH_OR_TAG={}".format(DSPFRONT_BRANCH_OR_TAG))
DSPBACK_BRANCH_OR_TAG=sys.argv[4]
print("DSPBACK_BRANCH_OR_TAG={}".format(DSPBACK_BRANCH_OR_TAG))


print("If previous deployment at {}/dsp exists, remove".format(DEPLOYMENT_TARGET))
if (os.path.exists(DEPLOYMENT_TARGET + "/dsp")):
    print("Change to deployment directory.")
    print("os.chdir({}).format(DEPLOYMENT_TARGET")
    os.chdir(DEPLOYMENT_TARGET)
    print("Stop previous deployment.")
    # here comes the docker stuff
    client = docker.from_env() # used in rest of program to get env for docker
    dspback_build.stop(client)
    dspfront_build.stop(client)
    
    print("cd {}".format(DEPLOYMENT_TARGET))
    os.chdir(DEPLOYMENT_TARGET)

    print("Removing previous deployment.")
    print("shutil.rmtree(path) # essentially deletes a directory and it's contents")
    shutil.rmtree("{}/dsp",DEPLOYMENT_TARGET)
    print("Previous deployment removed.")
else:
    print("no previous deployment.")

print("Remove previous images.")
print("Remove dspfront image.")
# this code checks if there any images to remove
client = docker.from_env()
if (len(client.images.list("dspfront")) == 0):
    print("Dspfront image not found.")
else:
    print("Remove dspfront")
    # not sure what the {{.Tag}} references to in the bash script but we will see
    #docker rmi dspfront: (that tag part goes here)
    client.images.remove("dspfront", True, True) #name, force, no prune

print("Remove dspback image.")
if (len(client.images.list("dspback")) == 0):
    print("Dspback image not found.")
else:
    print("Remove dspback")
    # not sure what the {{.Tag}} references to in the bash script but we will see
    #docker rmi dspfront: (that tag part goes here)
    client.images.remove("dspback", True, True) #name, force, no prune
    
print("Remove node image.")
if (len(client.images.list("node")) == 0):
    print("Node image not found.")
else:
    print("Remove node")
    # not sure what the {{.Tag}} references to in the bash script but we will see
    #docker rmi dspfront: (that tag part goes here)
    client.images.remove("node", True, True) #name, force, no prune


print("Remove python image.")
if (len(client.images.list("python")) == 0):
    print("Python image not found.")
else:
    print("Remove python")
    # not sure what the {{.Tag}} references to in the bash script but we will see
    #docker rmi dspfront: (that tag part goes here)
    client.images.remove("python", True, True) #name, force, no prune

print("Remove nginx image.")
if (len(client.images.list("nginx")) == 0):
    print("Nginx image not found.")
else:
    print("Remove nginx")
    # not sure what the {{.Tag}} references to in the bash script but we will see
    #docker rmi dspfront: (that tag part goes here)
    client.images.remove("nginx", True, True) #name, force, no prune

print("Remove dangling images.")
if (len(client.images.list(filters={"dangling":True})) == 0):
    print("No dangling images.")
else:
    print("Removing dangling images")
    # not sure what the {{.Tag}} references to in the bash script but we will see
    #docker rmi dspfront: (that tag part goes here)
    for image in client.images.list(filters={"dangling":True}):
        #short_id = 'sha256:1f6ddc1b2547'
        #short_id[7:] = '1f6ddc1b2547'
        id = image.short_id[7:]        
        client.images.remove(id, True, True)

print("Previous images removed.")

print("Pull everything from github and checkout to correct branches")


gh = github3.GitHub()
# this the format of how it should be done, I will continue mimicking deploy-contribute.sh
# repo = gh.repository("cznethub", "dspback")
# clone = git.Repo.clone_from(repo.clone_url, "dspback")
# clone.git.checkout("tags/v1.2.6")
print("Change to deployment target directory.")
print("os.chdir({})".format(DEPLOYMENT_TARGET))
os.chdir(DEPLOYMENT_TARGET)
repo = gh.repository("cznethub", "dsp")
print("Clone dsp from {}/dsp.git.".format(DSP_BRANCH_OR_TAG))
clone = git.Repo.clone_from(repo.clone_url, "dsp")
print("Dsp cloned")
print("Checkout to {}", DSP_BRANCH_OR_TAG)
clone.git.checkout(DSP_BRANCH_OR_TAG)

print("Change to dsp directory.")
print("os.chdir(./dsp)")
os.chdir("./dsp")
repo = gh.repository("cznethub", "dspfront")
print("Clone dspfront from {}/dspfront.git.".format(DSPFRONT_BRANCH_OR_TAG))
clone = git.Repo.clone_from(repo.clone_url, "dspfront")
print("Dspfront cloned")
print("os.chdir(./dspfront)")
os.chdir("./dspfront")
print("Checkout to {}", DSPFRONT_BRANCH_OR_TAG)
clone.git.checkout(DSPFRONT_BRANCH_OR_TAG)
print("os.chdir(..)")
os.chdir("..")

repo = gh.repository("cznethub", "dspback")
print("Clone dspback from {}/dspback.git.".format(DSPBACK_BRANCH_OR_TAG))
clone = git.Repo.clone_from(repo.clone_url, "dspback")
print("Dspback cloned")
print("os.chdir(./dspback)")
os.chdir("./dspback")
print("Checkout to {}", DSPBACK_BRANCH_OR_TAG)
clone.git.checkout(DSPBACK_BRANCH_OR_TAG)
print("os.chdir(..)")
os.chdir("..")

# Copy environment part, can't really do cause it's supposed to be the first go around
# but I'll at least make an effort to try an make it work.
"""
print("Copy environment.")
print("shutil.copyfile(\"{}/{}/.env\",format(DEPLOYMENT_SOURCE, HOSTNICK),\"{}/dsp\".format(DEPLOYMENT_TARGET))")
shutil.copyfile("{}/{}/.env",format(DEPLOYMENT_SOURCE, HOSTNICK),"{}/dsp".format(DEPLOYMENT_TARGET))
print("shutil.copyfile(\"{}/dsp/.env\".format(DEPLOYMENT_TARGET), \"{}/dsp/dspfront\".format(DEPLOYMENT_TARGET))")
shutil.copyfile("{}/dsp/.env".format(DEPLOYMENT_TARGET), "{}/dsp/dspfront".format(DEPLOYMENT_TARGET))
print("shutil.copyfile(\"{}/dsp/.env\".format(DEPLOYMENT_TARGET), \"{}/dsp/dspback\".format(DEPLOYMENT_TARGET))")
shutil.copyfile("{}/dsp/.env".format(DEPLOYMENT_TARGET), "{}/dsp/dspback".format(DEPLOYMENT_TARGET))
print("Environment copied.")
"""

# end of environment part

# start building an running the deployment
# can't really do without the compose command.
dspback_build.build(client, DEPLOYMENT_TARGET)
dspfront_build.build(client, DEPLOYMENT_TARGET)