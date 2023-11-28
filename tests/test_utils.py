import pathlib
from unittest.mock import mock_open, patch
import shutil

from src.utils import load_env_vars, update_env_based_on_git_branch


def test_load_env_vars_successfully():
    m = mock_open()
    with patch("__main__.open", m, create=False):
        test_file_name = "test.env"

        with open(test_file_name, "w") as f:
            f.write("ENV=dev")

        env_vars = load_env_vars(test_file_name)
        pathlib.Path.unlink(pathlib.Path(test_file_name))

        assert len(env_vars) > 0
        assert isinstance(env_vars, dict)


def test_update_env_based_on_git_branch_sucessfully():
    test_file_name = "test.env"
    root_dir = pathlib.Path.cwd()

    shutil.copy(root_dir / ".env", root_dir / test_file_name)

    update_env_based_on_git_branch("master", root_dir / test_file_name)

    env_line = []

    with open(root_dir / test_file_name, "r") as fp:
        lines = fp.readlines()
        for line in lines:
            if line.startswith("ENV"):
                line = line.replace("\n", "")
                env_line.append(line)

        pathlib.Path.unlink(pathlib.Path(root_dir / test_file_name))

        assert len(env_line) > 0
        assert env_line[0] == "ENV=prod"
