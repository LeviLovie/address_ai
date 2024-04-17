NO_COLOR=\033[0m
OK_COLOR=\033[32;01m
ERROR_COLOR=\033[31;01m
WARN_COLOR=\033[33;01m

help: ## Display this help
	@grep -hE '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "${OK_COLOR}%-30s${NO_COLOR} %s\n", $$1, $$2}'

everything: dataset train test ## Train the model and test it

dataset: ## Generate the dataset
	@python3 ./dataset.py

train: ## Train the model
	@python3 ./train.py

test: ## Test the model
	@python3 ./test.py
