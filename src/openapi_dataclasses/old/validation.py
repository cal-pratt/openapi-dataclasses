# import subprocess
# import sys
#
#
# def validate_module(module_path: list[str], base_path: str = ".") -> None:
#     module_file_path = "/".join(module_path)
#     module_python_path = ".".join(module_path)
#
#     print(f"Running isort on {module_python_path}...")
#     isort_complete = subprocess.run(
#         [sys.executable, "-m", "isort", f"{module_file_path}"],
#         cwd=base_path,
#     )
#     if isort_complete.returncode != 0:
#         raise Exception(f"Running isort on {module_python_path} failed.")
#
#     print(f"Running black on {module_python_path}...")
#     black_complete = subprocess.run(
#         [sys.executable, "-m", "black", f"{module_file_path}/*"],
#         cwd=base_path,
#     )
#     if black_complete.returncode != 0:
#         raise Exception(f"Running black on {module_python_path} failed.")
#
#     print(f"Testing imports on {module_python_path}...")
#     model_import_complete = subprocess.run(
#         [sys.executable, "-c", f"from {module_python_path} import *"],
#         cwd=base_path,
#     )
#     if model_import_complete.returncode != 0:
#         raise Exception(f"Importing {module_python_path} package crashes.")
