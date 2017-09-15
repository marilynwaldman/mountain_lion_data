

# Training an object detector using Cloud Machine Learning Engine from Google Cloud

The object detector  [tutorial](https://cloud.google.com/blog/big-data/2017/06/training-an-object-detector-using-cloud-machine-learning-engine) is written for a Ubuntu platform.  This repo creates a docker image and container image on GCP to run the 
tutorial on.  All dependencies are loaded into the docker image.  You will not need to issue apt-get or pip commands from the docker image.


Here's an overview of what you'll do:

- Create a free account on Google Cloud or use an exiting account.
- Create a new project on Google Cloud.
- Upload and build a docker image to Google Cloud.
- Create a "container-optimized" VM and ssh to it.
- Start a docker container running on the VM. 
- Then, in the running docker container, run the [tutorial](https://cloud.google.com/blog/big-data/2017/06/training-an-object-detector-using-cloud-machine-learning-engine)

## Prerequsites:

- A credit card (you will not be charged), to create a Google Cloud Platform account; or, an existing account.
- Chrome, or another browser and an ssh client.


## Initial setup


### 1. Set Up Your GCP Project

#### 1.1 Create a Cloud Platform project

Create a Google Cloud Platform (GCP) account by [signing up for the free trial](https://cloud.google.com/free-trial/).
You will be asked to enter a credit card number, but you will get $300 of credits, and won't be billed.

If you already have an account, and have run through your trial credits, see one of the workshop instructors. We will give you additional credits to apply to your account.

#### 1.2 Enable the necessary APIs

1. Click on the “hamburger” menu at upper-left, and then “API Manager”.
1. On the left nav, choose "Dashboard" if not already selected, then choose "+Enable API" in the top-middle of page.
1. Enter "Google Compute Engine API" in the search box and click it when it appears in the list of results.
1. Click on “Enable” (top-middle of page).
1. Repeat steps 2 through 4 for: "Google Cloud Container Builder API" and "Google Cloud Machine Learning".

![Hamburger menu](./assets/hamburger.png)  

![API Manager](./assets/api_manager.png)


### 2. Connect to your project's Cloud Shell

Click on the Cloud Shell icon (leftmost icon in the set of icons at top-right of the page).

![Cloud Shell](./assets/cloudshell.png)


Run commands 3-6 below in the Cloud Shell.

### 3. Initialize Cloud ML for your project

```shell
gcloud  ml vision
```

Respond "Y" when asked.

### 4. Set up your Cloud Storage Bucket and upload the Dockerfile

```shell
PROJECT_ID=$(gcloud config list project --format "value(core.project)")
BUCKET_NAME=${PROJECT_ID}-ml
gsutil mb -l us-central1 gs://$BUCKET_NAME
```
##### Build and upload the Dockerfile

# Use a Docker File on Google Cloud Platform Container Image
 
#### Build the Dockerfile and upload it to GCP.  Instruction found [here](https://cloud.google.com/container-builder/docs/quickstarts/dockerfile)

git clone this repo:

    git clone https://github.com/marilynwaldman/GCPObjectDetection.git
    cd GCPObjectDetection  

#### Log in to Google Cloud

Authorize gcloud to access your project:
    
    gcloud auth login
    
Configure your project for gcloud, where [PROJECT-ID] is your Cloud Platform project ID:
  
    gcloud config set project $PROJECT_ID
   
If you don't know your project ID, run the following command:
  
    gcloud projects list
  

#### Build and push your Dockerfile to GCP


To submit a build request using your Dockerfile, run the following command from the directory containing your application code, Dockerfile, and any other assets:


    gcloud container builds submit --tag gcr.io/$PROJECT_ID/object-detect .

where

[PROJECT-ID] is your Cloud Platform project ID


Check that your image is built on GCP. Run the following command:

    gcloud container images list


### Make the docker image available to container instances.  

Per instructions [here](https://cloud.google.com/container-registry/docs/access-control)

Display your project's Cloud Storage buckets:

    gsutil ls

Mark all current objects, including the image you just pushed, in your registry public by running the following command in your shell or terminal window:

    gsutil acl ch -r -u AllUsers:READ gs://artifacts.$PROJECT_ID.appspot.com


Make your registry's bucket publicly accessible:

    gsutil acl ch -u AllUsers:READ gs://artifacts.$PROJECT_ID.appspot.com

### 5. Create a container-optimized image in GCE

```shell
gcloud compute instances create object-detect \
    --image-family gci-stable \
    --image-project google-containers \
    --zone us-central1-b --boot-disk-size=100GB \
    --machine-type n1-standard-4
```

You can ignore the "I/O performance warning for disks < 200GB" for this example; it is not important in this context.

### 6. Set up a firewall rule for your project that will allow access to the web services we will run

```shell
gcloud compute firewall-rules create object-detect --allow tcp:8888,tcp:6006,tcp:5000
```

### 7. SSH into the new GCE instance, in a new browser window

- Click on the “hamburger” menu at upper-left, and then “Compute Engine”
- Find your instance in the list (mid-page) and click on the “SSH” pulldown menu on the right. Select “Open in browser window”.
- A new browser window will open, with a command line into your GCE instance.

### 8. Build the docker image and upload to GCP, then start the Docker container in the GCE image (in the newly opened SSH browser window):

```shell
sudo docker pull gcr.io/[Project-id]/object-detect
mkdir notebooks
sudo docker run -v `pwd`/notebooks:/root/notebooks -it -p 6006:6006 -p 8888:8888 -p 5000:5000 gcr.io/[Project_id]/object-detect
```

You should be issued a prompt from the docker shell.

Run the following in the Docker container - at the root***# prompt.

### 9. Configure the Docker container. You’ll need your project ID for this step.

(If you have forgotten your project ID, you can find it in the console by selecting the Home Dashboard.  It will be listed near the upper left of the main panel.)

In the following, replace `<your-project-ID>` with your actual project ID.

```shell

gcloud config set project <your-project-ID>
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-b

PROJECT=$(gcloud config list project --format "value(core.project)")
YOUR_GCS_BUCKET="gs://${PROJECT}-ml"

```

```shell
gcloud auth login
```
(and follow the subsequent instructions)

```shell
gcloud beta auth application-default login
```
(and follow the subsequent instructions)


## If you need to restart the container later

If you later exit your container and then want to restart it again, you can find the container ID by running the following in your VM:

```shell
docker ps -a
docker start <container_id>
```
Once the workshop container is running again, you can exec back into it like this:

```shell
docker exec -it <container_id> bash
```

Note that you may need to define environment variables from step 9 when you reconnect.
Note also that if you later start a separate new container 'from scratch', you will need to repeat the auth setup.

## What next?

You should now be set to run all of the workshop exercises from your docker container!

From this docker container do not try to re-import dependencies with apt-get or pip. 
## Cleanup

Once you’re done with your VM, you can stop or delete it. If you think you might return to it later, you might prefer to just stop it. (A stopped instance does not incur charges, but all of the resources that are attached to the instance will still be charged).  You can do this from the [cloud console](https://console.cloud.google.com), or via command line from the Cloud Shell as follows:



1. gcloud compute instances create object-detection \
   --image-family gci-stable \
   --image-project google-containers \
   --zone us-central1-b --boot-disk-size=100GB \
   --machine-type n1-standard-4

2. gcloud compute firewall-rules create object-detection --allow tcp:8888,tcp:6006,tcp:5000

3.  git clone git@github.com:marilynwaldman/GCPObjectDetection.git
    cd GCP*
    cd GCP*
    docker build ObjectDetect .
    docker images
    docker run -p 6006:6006 -p 8888:8888 -p 5000:5000 object-detection

imperial-octane-178819


sudo docker run -p 6006:6006 -p 8888:8888 -p 5000:5000 gcr.io/tensorflow/tensorflow

open new terminal ssh
