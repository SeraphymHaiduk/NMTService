-include .env.local
export

SYSTEM_PYTHON = $(shell which python)
PYTHON = venv/bin/python

# Plese add this to ~/.bashrc
# export CUDA_HOME=/usr/local/cuda
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64
# export PATH=$PATH:$CUDA_HOME/bin

# copy environment variables config template if .env.local does not exist yet
copy-env:
	cp -n .env.template .env.local

install-nvidia-drivers:
	# wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
	# sudo dpkg -i cuda-keyring_1.1-1_all.deb
	# sudo apt update
	# sudo apt -y install cuda-toolkit-12-6
	# rm cuda-keyring_1.1-1_all.deb*
	# sudo apt install -y cuda-drivers
	sudo apt install -y nvidia-driver-560

remove-all-nvidia-packages:
	sudo apt-get purge 'nvidia*'
	sudo apt-get autoremove
	sudo apt-get autoclean

dep: copy-env
	sudo apt update
	sudo apt install -y mecab libmecab-dev mecab-ipadic-utf8 unidic-mecab
	sudo apt install -y python3.10 python3.10-venv #python3.10-dev
	python3.10 -m venv venv
	$(PYTHON) -m pip install -r ./app/requirements.txt

run:
	$(PYTHON) -m uvicorn --app-dir 'app' src.main:app --port 5332 --host 0.0.0.0

# sudo apt install docker-compose   before first running
# systemctl start docker.service    if no docker deamon is running
database-up:
	docker compose up -d

database-check-containers:
	docker compose ps

## install docker:
# sudo apt update
# sudo apt install docker.io -y
# sudo systemctl start docker
# sudo systemctl enable docker

## install docker compose plugin
# sudo mkdir -p /usr/lib/docker/cli-plugins
# sudo curl -SL https://github.com/docker/compose/releases/download/v2.22.0/docker-compose-linux-x86_64 -o /usr/lib/docker/cli-plugins/docker-compose
# sudo chmod +x /usr/lib/docker/cli-plugins/docker-compose
# docker compose version
# 
## for using without sudo:
# sudo usermod -aG docker $USER
# newgrp docker
