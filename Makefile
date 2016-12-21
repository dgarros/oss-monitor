

install-lib:
	pip install -r requirements.txt -t ./

zip:
	zip -r awslambda.zip .
