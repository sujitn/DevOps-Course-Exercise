#!/usr/bin/env bash

sudo apt-get update

sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

git clone https://github.com/pyenv/pyenv.git /home/vagrant/.pyenv
echo 'export PYENV_ROOT="/home/vagrant/.pyenv"' >> /home/vagrant/.profile
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> /home/vagrant/.profile
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> /home/vagrant/.profile

exec "$SHELL"