Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"

  config.vm.provision "shell", privileged: false, inline: <<-SHELL
    sudo apt-get update
	sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
	curl https://pyenv.run | bash
	echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.profile
	echo 'eval "$(pyenv init -)"' >> ~/.profile
	echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.profile
	source ~/.profile
	export PATH="/home/vagrant/.pyenv/bin:$PATH"
	eval "$(pyenv init -)"
	eval "$(pyenv virtualenv-init -)"
	pyenv install 3.8.5
	pyenv global 3.8.5
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
  SHELL
  
  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the TODO app setup script"
    trigger.run_remote = {privileged: false, inline: "
      cd /vagrant
      poetry install
      poetry run flask run --host 0.0.0.0
	  "}
  end
  
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  
end
