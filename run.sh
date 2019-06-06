#!/bin/bash

if ! test -f "./log_profile"; then
    touch log_profile
fi

LD_PRELOAD=./hook.so ./main test
