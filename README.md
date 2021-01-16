# auvsi_system
Ground control application that will be used to compete in the AUVSI autonomous drone competition.

![Docker Image CI](https://github.com/anselm94/googlekeepclone/workflows/Docker%20Image%20CI/badge.svg)


<div align="center">

![Home page demo](docs/img/app.png)
</div>



## Table of contents
* [Prerequisites](#prerequisites)
* [Getting Started](#getting-started)
    + [First time set-up](#first-time-set-up)
    + [Running the Interop Server](#running-the-interop-server)
    + [Running the Interop Client](#running-the-interop-client)
* [Features](#features)
* [Documentation](#documentation)


### Prerequisites
* [Ubuntu](http://www.ubuntu.com/download/desktop/install-ubuntu-desktop)
* [Ubuntu Terminal](https://help.ubuntu.com/community/UsingTheTerminal)
* [Linux Shell](http://linuxcommand.org/learning_the_shell.php)
* [Git](https://git-scm.com/doc)
* [Github](https://guides.github.com/activities/hello-world)
* [Docker](https://docs.docker.com/engine/getstarted)
* [Python](https://docs.python.org/2/tutorial)
* [Virtualenv](https://virtualenv.pypa.io/en/stable)
* [Pip](https://pip.pypa.io/en/stable/user_guide)
* [Django](https://docs.djangoproject.com/en/1.8/intro)
* [Protobuf](https://developers.google.com/protocol-buffers/docs/pythontutorial)
* [Postgres](https://www.postgresql.org/docs/9.3/static/index.html)
* [Nginx](https://www.nginx.com)

## Getting Started

### First time set up
1) Clone the Git repository
```sh
git clone https://github.com/munikeraragon/AUVSI --recursive
```

2) cd interop/server
```sh
cd AUVSI/interop/server
```

3) Create the interop server's database.

```sh
sudo ./interop-server.sh create_db
```

4) Load initial test data into the server. This provides access to a default admin
account (u: `testadmin`, p: `testpass`) and a default team account (u:
`testuser`, p: `testpass`). This will also load a sample mission into the server.

```sh
sudo ./interop-server.sh load_test_data
```

### Running the Interop Server
#### Start shell
1) Change into the client subdirectory of the Git repo.
```sh
cd AUVSI/interop/server
```
2) Run the interop server on port 8000. The server will run until stopped using `Ctrl-C`.
```sh
sudo ./interop-server.sh up
```

### Running the Interop Client
#### Start shell
1) Change into the client subdirectory of the Git repo.
```sh
cd AUVSI/interop/client
```
2) Run the Docker container.
```sh
sudo docker run --net=host --interactive -v $(cd ../.. && pwd)/auvsi_system:/interop/auvsi_system --tty auvsisuas/interop-client

```
3) Change into the auvsi_system subdirectory of the Git repo.
```sh
cd /interop/auvsi_system
```
4) Install system requirements
```sh
sudo bash install.sh
```

3) Run the AUVSI interface system on port 5000. The app will run until stopped using `Ctrl-C`. 
```sh
python manage.py runserver 0.0.0.0:5000
```


## Features


## Documentation


