default:
	@cat makefile | grep -E ".*:\s+#"

env:
	python3 -m venv env
	. env/bin/activate; pip install --upgrade pip

update: env
	. env/bin/activate; pip install -r requirements.txt

# Job to remove pathlib library
.PHONY: remove_pathlib
remove_pathlib: update
	. env/bin/activate; pip uninstall -y pathlib

# Job to scan downloads folder
.PHONY: scan
scan:
	python3 scanners.py

# Job to run cleaner.py
.PHONY: clean
clean:
	python3 cleaner.py

# Job to build the GUI exe
.PHONY: build_exe
build_exe: remove_pathlib
	. env/bin/activate; pyinstaller -w -F -i "icon.icns" "Downloads_Cleaner.py"
	#mv dist/Downloads_Cleaner.app .
	#rm -rf build dist Downloads_Cleaner.spec
