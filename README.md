# Cspy
A C function call hooking generator using python.

## Project Structure
| File | Usage | Output |
| -------- | -------- |-------- |
| `api.yml`     | Define target functions you wanna hook| -
| `hook_compile.py`     | Generate API hooking function from api.yml | `hook.c`
| `hook.c`     | This file will be compiled as .so to insert into LD_PRELOAD | `hook.so`
| `main.c`     | Main program to be hooked | `main`
| `makefile`     | Compile main.c and hook.c | `hook.so, main`
| `run.sh`     | Run main with hooking functions | `log_profile`
| `log_profile`     | Function hooking logs. Format:  [return] func_name p_name=p_value | -
