##@ [Flow: Deploy]

.PHONY: deploy-flow
deploy-flow: ## Deploy flow (follow prompt instructions)
	@"$(MAKE)" env-init
	poetry export -o requirements.txt --without-hashes --without-urls --without=dev,test
	poetry run prefect deploy