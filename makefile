build_package:
	@echo "Building package..."
	. venv/bin/activate && python3 -m build

upload_package: build_package
	. venv/bin/activate && python3 -m twine upload --repository pypi dist/django_error_logger-1.0.2*

.PHONY: build_package upload_package
