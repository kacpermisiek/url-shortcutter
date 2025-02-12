# url-shortcutter

A simple URL shortcutter using Fastapi and Postgres db.

## How to start:
1. Clone the repository
2. Run `docker-compose up` in the root directory
3. Open `http://localhost:8000/docs` in your browser
4. Try out the API endpoints

## Endpoints:
### POST /shorten
It accepts a JSON payload with the following structure:
```json
{
  "url": "https://www.google.com"
}
```
It returns a JSON response with the shortened URL:
```json
{
  "shortened_url": "{BASE_URL}/abc123",
  "original_url": "https://www.google.com"
}
```

***If the URL is already shortened, it returns the existing shortened URL!***

### GET /{suffix}
It redirects to the original URL if the shortened URL exists in the database.

### GET /{suffix}/stats
It returns the stats of the shortened URL in JSON format:
```json
{
    "short_url": "{BASE_URL}/diGRcZchGjasoMbp",
    "original_url": "https://github.com/kacpermisiek",
    "visits": 9,
    "created_by": {
        "ip": "127.0.0.1",
        "user_agent": "PostmanRuntime/7.43.0"
    }
}
```

## Suffix creation:
Generated suffixes are ShortUUIDs. The length of the suffix is by default 16 characters.
It can be changed by adding the `SUFFIX_LENGTH` environment variable in `url_shortcutter/app/settings.py` file

## Tests:
There are few tests in the `tests` directory.
To run it, the database needs to be created:
```bash
docker compose up db -d
```

and virtual environment needs to be created:
```bash
python -m venv venv
source venv/bin/activate
poetry install
```

Then run the tests:
```bash
pytest
```
