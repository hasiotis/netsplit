.PHONY: help ## Print this help
help:
	@grep -E '^\.PHONY: [a-zA-Z_-]+ .*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'


.PHONY: init ## Initialize for development
init:
	@uv sync
	@uv run prek install


.PHONY: test ## Run tests
test:
	@uv run pytest


.PHONY: clean ## Cleanup generated files
clean:
	@rm -rf *.egg-info build dist docs/_build .coverage results.xml
	@find . -type d -name __pycache__ -exec rm -r {} \+


.PHONY: release  ## Make release
release:
	uv run cz bump;
	VERSION=`uv version --short`;                       \
	git push;                                             \
	git tag -a v$$VERSION -m "Tagged version $$VERSION";  \
	git push --tags;                                      \
	uv build --clear && uv publish --token ${UV_PUBLISH_TOKEN}
