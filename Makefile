build: build-dir
	python3 -m build --outdir build

build-dir:
	mkdir -p build

install:
	python3 -m pip install build/*.whl

uninstall:
	python3 -m pip uninstall build/*.whl -y


clean:
	if [ -d build ]; then rm -r build; fi
