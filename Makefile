PYTHON ?= python3

.PHONY: venv
venv:
	$(PYTHON) -m venv venv
	./venv/bin/python3 -m pip install --upgrade pip
	./venv/bin/python3 -m pip install -r requirements.txt

.PHONY: test
test:
	$(PYTHON) -m venv venv-test
	./venv-test/bin/python3 -m pip install ./dist/*.whl
	echo 'puts "ok' | ./venv-test/bin/openroad -exit -no_splash
	./venv-test/bin/python3 -c "import odb; print('ok')"

.PHONY: clean
clean:
	rm -rf .ruff_cache
	rm -f ./base_dir/openroad_bin/openroad.gz
	rm -f ./base_dir/openroad_bin/openroad
	rm -rf ./dist
	rm -rf ./dist_staging
	rm -rf ./venv-test
	rm -rf ./sandbox
