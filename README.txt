Hello!

1. It is better to create a venv for this project:
in pyCharm terminal: python -m venv venv

2. Activate venv:
in pyCharm terminal: venv/Scripts/Activate.ps1

3. Deactivate venv:
in pyCharm terminal: deactivate

4. If necessary to install python module:
in pyCharm terminal: python -m pip install <module_name>

5. If necessary to uninstall python module:
in pyCharm terminal: python -m pip uninstall <module_name>

6. To start web-service:
 in pyCharm terminal: uvicorn main:app --reload