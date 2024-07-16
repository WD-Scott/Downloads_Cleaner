default:
	@cat makefile | grep -E ".*:\s+#"

env:
	python3 -m -venv env; . env/bin/activate ; pip install --upgrade pip

update: env
	. env/bin/activate; pip install -r requirements.txt

# Job to scan downloads folder for the subdirectories and create if not found then scan for new files for moving
.PHONY: scan
scan:
	python3 scanners.py

# Job to run cleaner.py
.PHONY: clean
clean:
	python3 cleaner.py
