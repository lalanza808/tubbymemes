setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	mkdir -p data/uploads

shell:
	bash manage.sh shell

init:
	.venv/bin/alembic upgrade head

dev:
	bash manage.sh run

prod:
	bash manage.sh prod

install-ipfs:
	wget https://dist.ipfs.io/go-ipfs/v0.10.0/go-ipfs_v0.10.0_linux-amd64.tar.gz
	tar -xvzf go-ipfs_v0.10.0_linux-amd64.tar.gz
	cd go-ipfs && bash install.sh

install-avax:
	wget https://github.com/ava-labs/avalanchego/releases/download/v1.7.3/avalanchego-linux-amd64-v1.7.3.tar.gz
	tar -xzvf avalanchego-linux-amd64-v1.7.3.tar.gz

run-ipfs:
	ipfs daemon

run-avax:
	./avalanchego-v1.7.3/avalanchego

run-avax-test:
	./avalanchego-v1.7.3/avalanchego --network-id fuji

kill:
	pkill -e -f suchwowx
