install-front:
	cd front && npm install

install-back:
	cd back && npm install

install: install-front install-back

build:
	cd front && npm run build

run:
	make -j2 run-front run-back

run-front:
	cd front && npm run serve

run-back:
	cd back && ./node_modules/nodemon/bin/nodemon.js

lint:
	cd front && npm run lint --fix
