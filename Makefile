local-up:
	docker-compose -f docker-compose-local.yml pull
	docker-compose -f docker-compose-local.yml up -d --build
log:
	docker-compose logs -f --tail=200
local-down:
	docker-compose -f docker-compose-local.yml down