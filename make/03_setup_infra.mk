##@ [Infrastructure: Setup]

.PHONY: setup-infra ## Setup infrastructure
	@"$(MAKE)" create-prefect-artifact-repository


.PHONY: create-prefect-artifact-repository
create-prefect-artifact-repository: ## Create GCP Artificat Repository for Prefect Flows
	@"$(MAKE)" make env-init
	gcloud artifacts repositories create prefect-$(ENV) --repository-format DOCKER --location $(GCP_DEFAULT_REGION)
	gcloud auth configure-docker \
		$(GCP_DEFAULT_REGION)-docker.pkg.dev
