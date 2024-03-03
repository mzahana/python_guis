#!/bin/bash -e

ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source $ROOT/print_color.sh
source $ROOT/l4t_version.sh

docker build --build-arg BASE_IMAGE="nvcr.io/nvidia/l4t-base:r${L4T_VERSION}" -t mzahana/jetson-pyside:r${L4T_VERSION} . -f $ROOT/Dockerfile.jetson.pyside