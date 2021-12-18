setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

shell:
	bash manage.sh shell

dev:
	bash manage.sh run

prod:
	bash manage.sh prod

install-ipfs:
	wget https://dist.ipfs.io/go-ipfs/v0.10.0/go-ipfs_v0.10.0_linux-amd64.tar.gz
	tar -xvzf go-ipfs_v0.10.0_linux-amd64.tar.gz
	cd go-ipfs && bash install.sh

huey:
	mkdir -p data/
	.venv/bin/huey_consumer suchwowx.tasks.huey -w 1 -v | tee -a data/huey.log

kill:
	pkill -e -f huey
	pkill -e -f suchwowx
