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
	python3 src/pkg_cleaner/scanners.py

# Job to run cleaner.py
.PHONY: clean
clean:
	python3 src/pkg_cleaner/cleaner.py

# Job to build the GUI exe
.PHONY: build_exe
build_exe: remove_pathlib
	. env/bin/activate; pyinstaller -w -F -i "icon.icns" "src/pkg_cleaner/Downloads_Cleaner.py"
	@# Check if running on macOS and perform actions accordingly
	@uname | grep -q 'Darwin' && mv dist/Downloads_Cleaner.app . && rm -rf build dist Downloads_Cleaner.spec || echo "Skipping macOS-specific commands"

# Job to create Downloads dir for testing and add various tester files
create_downloads:
	@mkdir -p tests/Downloads
	@bash -c "touch tests/Downloads/tester.png tests/Downloads/tester.py tests/Downloads/tester.pdf tests/Downloads/tester.mp4 tests/Downloads/tester.mp3"

# Job to remove the tests/Downloads dir before running pytests
drop_temp_downloads:
	@rm -rf tests/Downloads/Audio
	@rm -rf tests/Downloads/Coding
	@rm -rf tests/Downloads/Documents
	@rm -rf tests/Downloads/Images
	@rm -rf tests/Downloads/Videos

# Job to run tests
.PHONY: test
test:
	pytest tests -vvx