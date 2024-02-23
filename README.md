# ExamplePrjForRustyIntegration
example st project with intent to integrate into OpenPLC


# building with command

docker run --rm -v /home/pi/ExamplePrjForRustyIntegration/:/build -v /home/pi/rusty/target/release/:/tool ghcr.io/plc-lang/rust-llvm:latest -c '/tool/plc build --hardware-conf build/conf.json'


# installing docker

sudo apt update
sudo apt upgrade
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# get rusty

clone https://github.com/PLC-lang/rusty.git
cd rusty
docker run --rm -v $PWD:/build ghcr.io/plc-lang/rust-llvm:latest -c 'cargo build --release'

