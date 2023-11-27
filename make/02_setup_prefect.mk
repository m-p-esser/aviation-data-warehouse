##@ [Prefect: Setup]

.PHONY: setup-prefect
setup-prefect: ## Setup Prefect
	@"$(MAKE)" update-prefect-blocks


.PHONY: create-prefect-blocks
create-prefect-blocks: ## Create/Update Prefect Blocks
	@"$(MAKE)" env-init
	@echo "Registering/Updating Prefect Blocks"
	prefect block register --file src/prefect/blocks/create_flightapi_api_key.py
	prefect block register --file src/prefect/blocks/create_flightradar24_credentials.py
	prefect block register --file src/prefect/blocks/create_gcp_credentials.py
	prefect block register --file src/prefect/blocks/create_env_var_strings.py


.PHONY: create-gcr-push-work-pool
create-gcr-push-work-pool: ## Create Google Cloud Run (Push) Work Pool
	@"$(MAKE)" env-init
	@echo "Creating/Updating Google Cloud Run Push Work Pool"
	poetry run prefect work-pool create $(GCP_PROJECT_ID)-gcr-push-work-pool-$(ENV) \
		--base-job-template src/prefect/work_pool/gcr_push_template.json \
		--type cloud-run:push
