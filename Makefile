# -*- coding: utf-8 -*-

TIMESTAMP := $(shell date +%Y%m%d%H%M%S)
MAKEFILE_DIR := $(dir $(realpath $(firstword $(MAKEFILE_LIST))))
OS_NAME := $(shell uname -s)

CMD_DOCKER := docker
CMD_DOCKER_COMPOSE := docker compose

MAIN_CONTAINER_APP := app
MAIN_CONTAINER_SHELL := bash
OPEN_TARGET := http://0.0.0.0:8080/

OPTS :=
.DEFAULT_GOAL := default
.PHONY: default setup hide reveal open build start check test doc clean prune help

default: start ## 常用

setup: ## 初期
ifeq ($(OS_NAME),Darwin)
	brew install git-cliff
	brew install git-secret
	brew install direnv
	brew install pre-commit
	brew install ruff
endif
	direnv allow
	pre-commit install
	@if [ $(OS_NAME) = "Darwin" ]; then say "The initialization process is complete." ; fi

hide: ## 秘匿
	git secret hide -vm

reveal: ## 暴露
	git secret reveal -vf

open: ## 閲覧
	@if [ $(OS_NAME) = "Darwin" ]; then open ${OPEN_TARGET} ; fi

build: check ## 構築
	./mwaa-local-env build-image
	@if [ $(OS_NAME) = "Darwin" ]; then say "The building process is complete." ; fi

start: build ## 開始
	./mwaa-local-env start

check: ## 検証
	pre-commit run --all-files
	@if [ $(OS_NAME) = "Darwin" ]; then say "The check process is complete." ; fi

test: ## 試験
	echo "Not implemented yet."
	@if [ $(OS_NAME) = "Darwin" ]; then say "The test process is complete." ; fi

doc: ## 文書
	echo "Not implemented yet."
	@if [ $(OS_NAME) = "Darwin" ]; then say "The documentation process is complete." ; fi

clean: ## 掃除
	rm -rfv logs/*
	find . -type f -name "*.log" -prune -exec rm -rf {} +
	rm -rfv .mypy_cache
	rm -rfv .pytest_cache
	rm -rfv .coverage.*
	@if [ $(OS_NAME) = "Darwin" ]; then say "The cleanup process is complete." ; fi

prune: ## 破滅
	$(CMD_DOCKER) system prune --all --force --volumes
	@if [ $(OS_NAME) = "Darwin" ]; then say "The pruning process is complete." ; fi

help: ## 助言
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
