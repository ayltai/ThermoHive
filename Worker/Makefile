run:
	PYTHONPATH=. python main.py

venv:
	python3 -m venv venv

reset: clean upgrade

clean:
	pip uninstall -y -r <(pip freeze)

upgrade:
	pip install --upgrade --upgrade-strategy eager --prefer-binary -r requirements.txt

outdated:
	pip list --outdated

lint: autopep8 pycodestyle pylint

autopep8:
	autopep8 -i -r src --global-config setup.cfg

pycodestyle:
	pycodestyle src

pylint:
	pylint --recursive=y --fail-under=9.5 src

test:
	pytest --cov=src --cov-report=term --cov-report=lcov

flash:
	esptool erase-flash
	esptool --chip ESP32-C3 -b 460800 --before default-reset --after hard-reset write-flash 0 ~/Downloads/ESP32_GENERIC_C3-20250911-v1.26.1.bin

deploy:
	mpremote connect /dev/ttyACM0 cp -r ./src/ :/
	mpremote connect /dev/ttyACM0 cp ./main.py :/main.py

rm:
	mpremote connect /dev/ttyACM0 fs rm :/main.py
	mpremote connect /dev/ttyACM0 fs rm -r :/src

ls:
	mpremote connect /dev/ttyACM0 fs ls :/
