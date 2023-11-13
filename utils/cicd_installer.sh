curl https://sh.rustup.rs -sSf | sh
source "$HOME/.cargo/env"
sh book_requirements.sh
pip3 install -r cicd_requirements.txt