
## Errors
1. `depend.mk: No such file or directory`  - run `./src/sfmakedepend` or `make new`


2. `for_main.o: In function main:for_main.c:(.text+0x2a): undefined reference to MAIN__` - this is normal, we are pre-compiling tuv and thus it does not have a main body (which it is not)


3. Anything mentioning tuv or DATAXX folders; or ./params `cd TUV_5.2.1/ && git pull && cd ../ && make tuv`

