
# load_local_weaviate:

# 	python src/app/etl/create_vector_schema.py
# 	python src/app/etl/addcontent.py

run_vector_db:
	docker-compose -f docker/weaviate.yml up --remove-orphans

run_pgvector_db:
	docker-compose -f docker/pgvector.yml up

# docker run --name pgvector-demo -e POSTGRES_PASSWORD=password -p 5432:5432 ankane/pgvector