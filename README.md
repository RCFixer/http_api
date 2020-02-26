# http_api_currency_converter
Simple web-service on pure Python with Docker Compose. 
## Usage
* Start server: `docker-compose up`
* Stop server: `docker-compose down`

Server port: `5000`.

URL: http://localhost:5000/{key}

Example requests using curl: 
* curl -X GET localhost:5000/1
* curl -X GET localhost:5000/53
* curl -X GET localhost:5000/234234