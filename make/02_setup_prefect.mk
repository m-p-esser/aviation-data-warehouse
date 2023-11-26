##@ [Prefect: Setup]

.PHONY: setup-prefect:
	@"$(MAKE)" create-prefect-blocks

.PHONY: create-prefect-blocks
create-prefect-blocks: ## Create Prefect Blocks
	@"$(MAKE)" env-init
	@echo "Registering Prefect Blocks"
	prefect block register --file src/prefect/blocks/create_flightapi_api_key.py
	prefect block register --file src/prefect/blocks/create_flightradar24_credentials.py
	prefect block register --file src/prefect/blocks/create_gcp_credentials.py
