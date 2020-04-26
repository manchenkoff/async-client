COLOR_HEADER=\e[92m
COLOR=\e[93m
END=\033[0m
PROJECT_NAME := AsyncClient

.SILENT: help clean build

help:
	printf "$(COLOR_HEADER)$(PROJECT_NAME) management\n\n" && \
	printf "$(COLOR)make help$(END)\t Show this message\n" && \
	printf "$(COLOR)make build$(END)\t Build application distributive directory\n" && \

clean:
	@rm -Rf ./build ./dist

build: clean
	@pyinstaller main.spec