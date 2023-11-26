##@ [Prefect: Setup]

.PHONY: setup-prefect
setup-prefect: ## Setup Prefect
	@"$(MAKE)" update-prefect-blocks


.PHONY: update-prefect-blocks
create-prefect-blocks: ## Create Prefect Blocks
	@"$(MAKE)" env-init
	@echo "Registering/Updating Prefect Blocks"
	prefect block register --file src/prefect/blocks/create_flightapi_api_key.py
	prefect block register --file src/prefect/blocks/create_flightradar24_credentials.py
	prefect block register --file src/prefect/blocks/create_gcp_credentials.py
