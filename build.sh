mkdir build

docker run --rm -v /home/pi/ExamplePrjForRustyIntegration/:/build -v /home/pi/rusty/target/release/:/tool ghcr.io/plc-lang/rust-llvm:latest -c '/tool/plc build --hardware-conf build/conf.json -g -Onone'

g++ -g -c testcpplink/main.cpp && cc -o testcpplink/main testcpplink/main.o build/ExamplePlcObject.o
