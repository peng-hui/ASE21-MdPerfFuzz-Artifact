# MdPerfFuzz

Markdown compilers analyze input text to generate formatted text with decorated styles according to the Markdown language syntaxes. Performance bugs in Markdown compilers could cause excessive resource consumption and negatively affect user experiences. They can even be leveraged by attackers for launching denial-of-service (DoS) attacks by specially crafting inputs to server-side Markdown compilers.

MdPerfFuzz is a fuzzing framework that detects performance bugs in Markdown compilers. It uses a syntax-tree based mutation strategy to efficiently generate test cases. It then applies an execution trace similarity comparison algorithm to de-duplicate the bug reports. 

More information about MdPerfFuzz can be found in our [ASE '21 paper](mdperffuzz.pdf).


## Build

MdPerfFuzz has been tested on Debian GNU/Linux 10 (buster) and Ubuntu 18.04 LTS.

```sh
cd src/
./dep.sh # this script will install the dependencies and prepare the parser
make # build the fuzzer
cd llvm_mode & make # build llvm mode
```

## Run

### Instrumentation
When you build the testing Markdown compiler, use our customized compilers for the instrumentation. 

- `src/afl-gcc` and `src/afl-g++`.
- `src/afl-clang` and `src/afl-clang++`

For example, to instrument [cmark](https://github.com/commonmark/cmark), we have modified the Makefile of cmark to use `src/afl-clang` for the compilation. 

```sh
cd src/apps/cmark/ # enter the source code directory of cmark
make afl # the Makefile has hardcoded the path to AFL folder
```
The instrumented binary of cmark will be generated at `src/apps/cmark/build/src/cmark`.

### Start MdPerfFuzz

MdPerfFuzz works similar to AFL. To detect performance bugs, you simply add an argument `-p` when you start the fuzzer. The fuzzing results will be at the output directory you specify. You can check the [documents](src/docs/README) of AFL for more instructions.

```sh
cd src/
#./afl-fuzz -p [-i seed-directory] [-o output-directory] [-N max-input-length] binary @@
./afl-fuzz -p -i seeds -o cmark_out -N 64 ./apps/cmark/build/src/cmark @@
```

### De-duplicate bug reports

Construct edge-hit vectors for each reported bug in the output directory and use the cosine similarity algorithm to de-duplicate them.

```sh
cd src/
# use ./de-duplicate.py -h to check the usage.
./de-duplicate.py -b ./apps/cmark/build/src/cmark -i ./cmark_out -o final_out
```
The text files generated in `final_out` describe the cosine similarity of bug reports.

## License

MdPerfFuzz is under [MIT License](LICENSE.md).

## Authors

- Penghui Li (<phli@cse.cuhk.edu.hk>)

- Yinxi Liu (<yxliu@cse.cuhk.edu.hk>)

- Wei Meng (<wei@cse.cuhk.edu.hk>)
