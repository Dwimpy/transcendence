all:
	@docker compose -f ./Core/docker-compose.yml up -d --build

down:
	@docker compose -f ./Core/docker-compose.yml down

re:
	@docker compose -f ./Core/docker-compose.yml up -d --build

clean:
	@rm -rdf /Users/arobu/data/
	@docker stop $$(docker ps -qa);\
	docker rm $$(docker ps -qa);\
	docker rmi -f $$(docker images -qa);\
	docker volume rm $$(docker volume ls -q);\
	docker network rm $$(docker network ls -q);\




.PHONY: all re down clean