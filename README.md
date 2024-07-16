This project combines FastAPI, Scrapy to create a scalable and efficient web scraping tool.
The project includes an API for initiating web scraping tasks, which are handled using command. Scrapy spiders are used to perform the actual web scraping, with retry mechanisms to handle temporary failures.


>python -m venv venv
> 
>source venv/bin/activate
> 
>pip install -r requirements.txt

Run Scrapper server:
> uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload 
> 
Curl: 

Get Add Scrape Request: 
> curl --location 'http://0.0.0.0:8000/api/v1/scrape/' \
--header 'Authorization: 0964-4204-atlys-be-4bf8b973-8b91-05d47ae57f8e' \
--header 'Content-Type: application/json' \
--data '{
	"url":"https://dental*****.com/shop",
	"proxy":"",
	"page":1, 
	"limit": 1
}' 

Get Task Result: 
> curl --location 'http://0.0.0.0:8000/api/v1/result/4d21339b-d0ea-4760-b64a-1feb7b2e693c' \
--header 'Authorization: 0964-4204-atlys-be-4bf8b973-8b91-05d47ae57f8e'
> 
 
Run Scrapper script:
>  scrapy runspider <scrapping file path> -a url=web_url
