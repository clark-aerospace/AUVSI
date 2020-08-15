# auvsi_system
Ground control application that will be used to compete in the AUVSI autonoums dron competition.

![Docker Image CI](https://github.com/anselm94/googlekeepclone/workflows/Docker%20Image%20CI/badge.svg)


<div align="center">
![Home page demo](./docs/img/home_page.png)

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
cd interop/server
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
cd interop/server
```
2) Run the interop server on port 8000. The server will run until stopped using `Ctrl-C`.
```sh
sudo ./interop-server.sh up
```

### Running the Interop Client
#### Start shell
1) Change into the client subdirectory of the Git repo.
```sh
cd /interop/client
```
2) Run the Docker container.
```sh
sudo ./interop-client.sh run
```
3) Change into the auvsi_system subdirectory of the Git repo.
```sh
cd /interop/auvsi_system
```
3) Run the AUVSI interface system.
```sh
python manage.py runserver
```


## Features


## Documentation


