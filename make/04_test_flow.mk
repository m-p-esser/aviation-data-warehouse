##@ [Flow: Test]

.PHONY: run-unit-tests
run-unit-tests: ## Run all Unit Tests
# gh workflow run "Unit Test Prefect Flows" // Currently not working altough dispatcher has been added
	@"$(MAKE)" env-init
	pytest -v