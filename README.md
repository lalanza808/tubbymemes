# SuchWowX

This service is a continuation of SuchWow for the Wownero cryptocurrency project. It has been revamped to use Interplanetary Filesystem, server federation / content sharing, and optionally Avalanche network via a smart contract with some useful features (if you're into that). It's a decentralized application (dApp); it's preferred you run it locally and bootstrap the services on your own machine.

## Setup

Tools you will need:
* https://github.com/ava-labs/avalanchego/
* https://ipfs.io/#install
* python3 (linux os will have this)

I have provided a `Makefile` with some helpful stuff...make sure to install `make` to use it.

```
# install python virtual environment and install application dependencies
make setup

# install ipfs
make install-ipfs

# optional: install avalanchego
make install-avax

# run ipfs
make run-ipfs

# optional: run avalanchego
make run-avax

# initialize sqlite database w/ schema via alembic
make init

# run development server
make dev

# access at http://127.0.0.1:5000
```
