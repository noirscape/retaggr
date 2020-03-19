.PHONY: build test clean-build dist
.DEFAULT_GOAL := help

bold:= $(shell tput bold)
sgr0:= $(shell tput sgr0)

pyc-clean: ## Remove cython compilation files from the source directories
	@printf "$(bold)Removing __pycache__, .pyc and .pyo files$(sgr0)\n"
	find . | grep --extended-regexp '(__pycache__|\.pyc|\.pyo$$)' | xargs rm --force --recursive

build-clean: ## Remove the build directories
	@printf "$(bold)Cleaning up build directories$(sgr0)\n"
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive src/*.egg-info

build: ## Build the package for distribution
	@printf "$(bold)Building package$(sgr0)\n"
	python3 setup.py sdist bdist_wheel

clean: build-clean pyc-clean ## Run all clean steps

clean-build: clean build ## Remove the build directory and build the package

test: ## Run the tests
	@printf "$(bold)Running tests$(sgr0)\n"
	py.test --cov=src --cov-config=.coveragerc -W ignore::DeprecationWarning

clean-test: clean test ## Cleanup execution files, then run the tests

dist: clean build ## Remove build directories, build the package, and run twine
	@printf "$(bold)Uploading distribution$(sgr0)\n"
	twine upload dist/*

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
