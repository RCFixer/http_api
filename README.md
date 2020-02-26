# http_api_currency_converter
Simple web-service on pure Python with Docker Compose. 
## Usage
* Start server: `docker-compose up`
* Stop server: `docker-compose down`

Server port: `5000`.

URL: http://localhost:2000/{key}

Example requests using curl: 
* curl -X GET localhost:2000/1
* curl -X GET localhost:2000/53
* curl -X GET localhost:2000/234234