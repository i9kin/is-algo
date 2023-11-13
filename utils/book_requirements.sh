curl -L --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/cargo-bins/cargo-binstall/main/install-from-binstall-release.sh | bash
cargo binstall -y mdbook-katex@0.5.8 mdbook-quiz@0.3.3 mdbook-last-changed@0.1.3 mdbook@0.4.25 mdbook-admonish@1.13.1
cd -
mdbook-admonish install
sudo apt install texlive-latex-extra texlive-luatex
sudo apt install pdf2svg
luaotfload-tool -v -vvv -u
sudo apt install imagemagick