curl https://sh.rustup.rs -sSf | sh
source "$HOME/.cargo/env"
sh book_requirements.sh
pip3 install -r cicd_requirements.txt
sudo apt install pdf2svg
sudo apt install texlive-latex-extra texlive-luatex
luaotfload-tool -v -vvv -u
sudo apt install imagemagick