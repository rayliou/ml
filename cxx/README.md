
- Use clang instead of gcc
```
VER=10 #18.04
VER=14 #Ubuntu 22.04
sudo apt install -y clang-$VER lld-$VER
export CC=/usr/bin/clang-$VER
export CPP=/usr/bin/clang-cpp-$VER
export CXX=/usr/bin/clang++-$VER
export LD=/usr/bin/ld.lld-$VER

```
