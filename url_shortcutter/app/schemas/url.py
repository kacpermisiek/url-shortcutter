from pydantic import BaseModel, Field, HttpUrl


class UrlCreateSchema(BaseModel):
    url: HttpUrl = Field(
        ...,
        description="The URL to be shortened",
        examples=["https://www.google.com", "https://www.example.com?q=1"],
    )


class CreatedBySchema(BaseModel):
    ip: str = Field(..., description="The IP address of the creator", examples=["192.168.1.1"])
    user_agent: str = Field(
        ...,
        description="The user agent of the creator",
        examples=[
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        ],
    )


class UrlCreateReturnSchema(BaseModel):
    short_url: HttpUrl = Field(..., description="The shortened URL", examples=["http://localhost:8000/abc123"])
    original_url: HttpUrl = Field(..., description="The original URL", examples=["https://www.google.com"])


class UrlStatsSchema(BaseModel):
    short_url: HttpUrl = Field(..., description="The shortened URL", examples=["http://localhost:8000/abc123"])
    original_url: HttpUrl = Field(..., description="The original URL", examples=["https://www.google.com"])
    visits: int = Field(..., description="The number of visits", examples=[0])
    created_by: CreatedBySchema = Field(..., description="The creator of the shortened URL")
