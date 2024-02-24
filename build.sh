mkdir -p build
mkdir -p src/build
mkdir -p testcpplink/build

python glueGenForRusty/initglue.py src/build/__gluefile.st
docker run --rm -v /home/pi/ExamplePrjForRustyIntegration/:/build -v /home/pi/rusty/target/release/:/tool ghcr.io/plc-lang/rust-llvm:latest -c '/tool/plc build plc.json --hardware-conf build/conf.json --check'
python glueGenForRusty/gluegeneratorfromconf.py build/conf.json src/build/__gluefile.st  testcpplink/build/plc.hpp
docker run --rm -v /home/pi/ExamplePrjForRustyIntegration/:/build -v /home/pi/rusty/target/release/:/tool ghcr.io/plc-lang/rust-llvm:latest -c '/tool/plc -g -Onone build plc.json'

g++ -g -c testcpplink/main.cpp -I testcpplink/build/ -o testcpplink/build/main.o && cc -o testcpplink/build/main testcpplink/build/main.o build/ExamplePlcObject.o
