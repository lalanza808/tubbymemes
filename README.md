# tubbymemes

Meme site dedicated to the best project on the Etherium network ;)

https://tubbycats.xyz/about

Memes are backed by Interplanetary Filesystem, server federation / content sharing, and optionally Avalanche network via a smart contract with some useful features (if you're into that). It's a decentralized application (dApp); it's preferred you run it locally and bootstrap the services on your own machine.

## Setup

Tools you will need:
* https://ipfs.io/#install
* python3 (linux os will have this)
* python3-venv
* https://github.com/ava-labs/avalanchego/ (optional)

### Development

I have provided a `Makefile` with some helpful stuff...make sure to install `make` to use it.

```
# install python virtual environment and install application dependencies
make setup

# setup secrets
cp env-example .env && vim .env

# install ipfs
sudo make install-ipfs

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

### Production

You need a few more things:
* A VPS with a decent provider
* Nginx
* Certbot / Letsencrypt

Below is a set of commands you can follow to get setup. I used Ubuntu 20.04 on Digital Ocean. Run the below commands as root or prepend `sudo`.

```
# install nginx
apt-get install nginx -y

# install certbot
apt-get install certbot -y

# point DNS records at your VPS w/ a domain you control

# generate diffie hellman keys
openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048

# setup nginx ssl config from this repo
cp conf/nginx-ssl.conf /etc/nginx/conf.d/ssl.conf

# setup nginx site config from this repo
cp conf/nginx-site.conf /etc/nginx/sites-enabled/tubbymemes.conf

# generate TLS certificates
service nginx stop
certbot certonly --standalone -d <your dns record> --agree-tos -m <your email> -n
service nginx start

# setup ipfs service account and storage location
useradd -m ipfs
mkdir -p /opt/ipfs
chown ipfs:ipfs /opt/ipfs

# setup ipfs service daemon
cp conf/ipfs.service /etc/systemd/system/ipfs.service
systemctl daemon-reload
systemctl enable ipfs
systemctl start ipfs

# setup tubbymemes service account and storage location
useradd -m tubbymemes
mkdir -p /opt/tubbymemes

# setup tubbymemes application
git clone https://github.com/lalanza808/tubbymemes /opt/tubbymemes
cp /opt/tubbymemes/env-example /opt/tubbymemes/.env
vim /opt/tubbymemes/.env
chown -R tubbymemes:tubbymemes /opt/tubbymemes

# setup tubbymemes service daemon
cp conf/tubbymemes.service /etc/systemd/system/tubbymemes.service
systemctl daemon-reload
systemctl enable tubbymemes
systemctl start tubbymemes

# setup ongoing syncing with remote servers and Avalanche network
crontab -u tubbymemes conf/crontab
```

At this point you should have Nginx web server running with TLS certificates generated with Letsencrypt/Certbot, Systemd services for IPFS daemon for serving files and Gunicorn for serving the Flask application.

You'll obviously need to update some of your configuration files to match your domain/DNS, but it's fairly trivial.

Reach out on Twitter or Discord if you need support.
