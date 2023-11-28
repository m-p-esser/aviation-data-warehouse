""" Misc utility functions """

from dotenv import dotenv_values, find_dotenv


def load_env_vars(env_file_name: str = ".env") -> dict:
    """Load environment variables from .env file and store as dict"""
    env_file = find_dotenv(
        filename=env_file_name, raise_error_if_not_found=True, usecwd=True
    )
    env_vars = dotenv_values(env_file)

    return env_vars


def map_branch_to_env(branch: str):
    """Map Branch to env"""

    mapping = {"develop": "dev", "test": "test", "master": "prod"}
    env = mapping[branch]

    return env


def update_env_based_on_git_branch(branch: str, env_file_name: str):
    """Update Key Value pair in env file"""

    new_value = map_branch_to_env(branch)

    # Read the content of the existing .env file
    with open(env_file_name, "r") as file:
        lines = file.readlines()

    # Find and update the specified key
    for i in range(len(lines)):
        if lines[i].startswith("ENV="):
            lines[i] = f"ENV={new_value}\n"
            break

    # Write the updated content back to the .env file
    with open(env_file_name, "w") as file:
        file.writelines(lines)
