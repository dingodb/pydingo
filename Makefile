unittest:
	PYTHONPATH=`pwd` python3 -m pytest tests --cov=pymilvus -v

package:
	python3 -m build --sdist --wheel --outdir dist/ .

make_proto:
	git submodule update --init
	./proto_make.sh

install:
	git submodule update --init
	./proto_make.sh
	pip install -e .
