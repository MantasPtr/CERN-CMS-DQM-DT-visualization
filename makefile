export flaskApp = flaskController.py

server:
	FLASK_APP=$(flaskApp) flask run --host=0.0.0.0 --port=8080

debug: debugServer

debugServer:
	FLASK_APP=$(flaskApp) FLASK_DEBUG=1 FLASK_ENV=development flask run --host=0.0.0.0 --port=8080

test:
	python36 -m unittest machineLearning/test/modelTest.py
	python36 -m unittest machineLearning/test/transformTest.py

export:
	python36 export_import/exporting.py

import: $(file)
	python36 export_import/importing.py
