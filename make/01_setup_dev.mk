##@ [Development Enviroment: Setup]
# needs to run everytime you start to develop on your local machine

.PHONY: dev-init
dev-init:
	@"$(MAKE)" env-init
	@"$(MAKE)" gcp-init
	@"$(MAKE)" prefect-init


.PHONY: env-init
env-init: # Init environment based on currently active Git branch
	@$(eval current_branch=`git branch --show-current`)
	@echo "The current branch is: $(current_branch)"
	poetry run python -c "from src.utils import update_env_based_on_git_branch; update_env_based_on_git_branch('$(current_branch)', '.env')"
	@echo "Updated .env file"


.PHONY: prefect-init
prefect-init:
	@echo "Logging into Prefect Cloud"
	poetry run prefect cloud login


.PHONY: gcp-init
gcp-init: ## Set GCP Service account as standard service account
	gcloud auth login
	@"$(MAKE)" set-default-gcp-project
	@echo "Configure Service Account to be active account. Required to work with GCP commands"
	@"$(MAKE)" set-deployment-service-account-as-default
	gcloud config configurations list



