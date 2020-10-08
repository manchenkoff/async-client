# AsyncChat client application

Simple CLI-application to connect with AsyncChat application (like Telnet)

## How to build

Just download and run `make build` then use executable file from `dist` directory

Available `make` commands

```bash
build                          Build application
clean                          Clean up distributable files
help                           Show this message
run                            Run application
sync                           Install dependencies
```

## How to use

To start a connection run the following command in the terminal / command line:

```bash
async-async_client --host=127.0.0.1 --port=8888
```
