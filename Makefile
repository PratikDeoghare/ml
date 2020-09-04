.PHONY: jupy 

pull:
	docker pull floydhub/dl-docker:cpu

run: 
	ls $(PWD)/shared/
	docker run -it -p 8888:8888 -p 6006:6006 -v $(PWD)/shared:/root/shared floydhub/dl-docker:cpu bash

jupy: 
	ls $(PWD)/shared/
	docker run -it -p 8888:8888 -p 6006:6006 -v $(PWD)/shared:/root/shared floydhub/dl-docker:cpu jupyter notebook



