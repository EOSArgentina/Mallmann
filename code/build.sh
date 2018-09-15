#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

WASM_ROOT=${WASM_ROOT:-"/opt/wasm"}
EOS_INSTALL=${EOS_INSTALL:-"/opt/eos"}
CODE=$DIR

if [ ! -f $WASM_ROOT/bin/clang ]; then echo "$WASM_ROOT/bin/clang not found, please set WASM_ROOT env variable"; exit; fi
if [ ! -f $WASM_ROOT/bin/llc ]; then echo "$WASM_ROOT/bin/llc not found, please set WASM_ROOT env variable"; exit; fi
if [ ! -f $EOS_INSTALL/bin/eosio-s2wasm ]; then echo "$EOS_INSTALL/bin/eosio-s2wasm not found, please set EOS_INSTALL env variable"; exit; fi
if [ ! -f $EOS_INSTALL/bin/eosio-wast2wasm ]; then echo "$EOS_INSTALL/bin/eosio-wast2wasm not found, please set EOS_INSTALL env variable"; exit; fi

for i in "forward" "set_resource_limits" "update_row" "void"; do
	$WASM_ROOT/bin/clang -emit-llvm -O3 --target=wasm32 -nostdinc \
	     -nostdlib -ffreestanding -nostdlib \
	     -fno-threadsafe-statics -fno-rtti -fno-exceptions \
	     -I$EOS_INSTALL/include/musl/upstream/include \
	     -o $CODE/$i/$i.bc -c $CODE/$i/$i.c

	$WASM_ROOT/bin/llc -thread-model=single \
	     --asm-verbose=false \
	     -o $CODE/$i/$i.s $CODE/$i/$i.bc

	$EOS_INSTALL/bin/eosio-s2wasm -o $CODE/$i/$i.wast \
	     -s 16384 $CODE/$i/$i.s

	$EOS_INSTALL/bin/eosio-wast2wasm $CODE/$i/$i.wast $CODE/$i/$i.wasm -n
done