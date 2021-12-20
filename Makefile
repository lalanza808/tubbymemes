setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	mkdir -p data/uploads

shell:
	bash manage.sh shell

init:
	bash manage.sh init

dev:
	bash manage.sh run

prod:
	bash manage.sh prod

install-ipfs:
	wget https://dist.ipfs.io/go-ipfs/v0.10.0/go-ipfs_v0.10.0_linux-amd64.tar.gz
	tar -xvzf go-ipfs_v0.10.0_linux-amd64.tar.gz
	cd go-ipfs && bash install.sh

kill:
	pkill -e -f suchwowx
