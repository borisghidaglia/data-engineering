# Not Tripadvisor

This project has been developped during the course DSIA-4203C. The goal was to crawl
and scrape data from a chosen website. We decided to retrieve users and reviews from
Tripadvisor.

## Table of content
1. [Getting Started](#getting-started)  
    1.1 [Prerequisites](#prerequisites)  
    1.2 [Installing and Running](#installing-and-running)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

Thanks to docker's magic, it's really the only thing you need to setup *- ok, along with docker-compose*. You can install docker [here](https://docs.docker.com/install/). If you don't
fit the system requirements, don't forget to check [Docker Toolbox](https://docs.docker.com/toolbox/overview/). As for Docker Compose : [it's over here](https://docs.docker.com/compose/install/).

### Installing and Running

Clone this repository with :
```bash
$ git clone https://github.com/borisghidaglia/data-engineering.git
```

Go into the repository :
```bash
$ cd data-engineering/
```

Then, you need to download the dumped data we prepared for you, so that it can be restored
in the *mongo* container you will start. * - Make sure you have curl and unzip installed*
```bash
$ mkdir data && \
mkdir data/dump && \
cd data/dump && \
curl -o tripadvisor_dump.zip https://perso.esiee.fr/~prolonga/data/tripadvisor_dump.zip && \
unzip tripadvisor_dump.zip && \
rm tripadvisor_dump.zip && \
cd ../..
```

**If you downloaded Docker Desktop**, make sure the app is running. **You've got Docker Toolbox ?**
If the *docker-machine* isn't started yet, run :
```bash
$ docker-machine start default
```

Finally :
```bash
$ docker-compose up -d
```

Once *app, mongo, mongo_seed* and *elastic* are built and up, and after waiting for a little while, you will be able to use the app in your browser.
