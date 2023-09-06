version:
	python3 setup.py --version
	
package:
	python3 -m build --sdist --wheel --outdir dist/ .

make_proto:
	git submodule update --init
	git submodule update --remote
	bash ./proto_make.sh

install:
	git submodule update --init
	git submodule update --remote
	bash ./proto_make.sh
	pip install -e .
