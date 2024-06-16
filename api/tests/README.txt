docker build -t proficient-api-test -f ./api/Dockerfile.test ./api
docker run -di --name proficient-test -v "$(pwd)/api:/app" -p 5200:5200 proficient-api-test `
docker exec -it proficient-test bash
