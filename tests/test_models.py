import os
import sys
from unittest.mock import patch

import pytest
import yaml

from openapi_dataclasses.main import main

BASE_PATH = os.path.dirname(__file__)
TEST_MODELS_DIR = os.path.join(BASE_PATH, "model_tests")


@pytest.mark.parametrize("test_dir", os.listdir(TEST_MODELS_DIR))
def test_models(test_dir, tmp_path):
    output_dir = tmp_path / test_dir
    config_dir = os.path.join(TEST_MODELS_DIR, test_dir)

    with open(os.path.join(config_dir, "config.yaml")) as test_config_file:
        test_config = yaml.load(test_config_file.read(), Loader=yaml.CLoader)

    openapi_json = os.path.join(config_dir, test_config["openapi_json"])
    client_module = test_config["client_module"]

    args = ["", "-m", client_module, "-o", str(output_dir), openapi_json]
    with patch.object(sys, "argv", args):
        main()

    for file_comparison in test_config["file_comparisons"]:
        expected_model_path = os.path.join(config_dir, file_comparison["expected"])
        actual_model_path = os.path.join(output_dir, file_comparison["actual"])

        with open(expected_model_path, "r") as expected_model_file:
            expected_model = expected_model_file.read()
        with open(actual_model_path, "r") as actual_model_file:
            actual_model = actual_model_file.read()

        assert expected_model == actual_model
