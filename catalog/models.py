"""
Amazon Product Models - Pydantic data models for Amazon products
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class AmazonPrice(BaseModel):
    """Amazon product price model."""

    current: Optional[float] = Field(default=None, description="Current price")
    original: Optional[float] = Field(default=None, description="Original price")
    currency: str = Field(default="USD", description="Price currency")
    discount_percent: Optional[int] = Field(
        default=None, description="Discount percentage"
    )


class AmazonRating(BaseModel):
    """Amazon product rating model."""

    rating: Optional[float] = Field(default=None, description="Product rating (1-5)")
    review_count: Optional[int] = Field(default=None, description="Number of reviews")
    rating_text: Optional[str] = Field(default=None, description="Rating text")


class AmazonImage(BaseModel):
    """Amazon product image model."""

    url: str = Field(description="Image URL")
    alt_text: Optional[str] = Field(default=None, description="Image alt text")
    is_primary: bool = Field(default=False, description="Is primary image")


class AmazonProduct(BaseModel):
    """Amazon product model."""

    asin: str = Field(description="Amazon Standard Identification Number")
    title: str = Field(description="Product title")
    price: Optional[AmazonPrice] = Field(default=None, description="Product price")
    rating: Optional[AmazonRating] = Field(default=None, description="Product rating")
    availability: Optional[str] = Field(
        default=None, description="Product availability"
    )
    images: List[AmazonImage] = Field(
        default_factory=list, description="Product images"
    )
    features: List[str] = Field(default_factory=list, description="Product features")
    description: Optional[str] = Field(default=None, description="Product description")
    specifications: Dict[str, Any] = Field(
        default_factory=dict, description="Product specifications"
    )
    url: str = Field(description="Product URL")
    category: Optional[str] = Field(default=None, description="Product category")
    brand: Optional[str] = Field(default=None, description="Product brand")
    seller: Optional[str] = Field(default=None, description="Product seller")
    prime_eligible: bool = Field(default=False, description="Prime eligible")
    free_shipping: bool = Field(default=False, description="Free shipping available")


class AmazonSearchResult(BaseModel):
    """Amazon search result model."""

    query: str = Field(description="Search query")
    total_results: Optional[int] = Field(
        default=None, description="Total results count"
    )
    products: List[AmazonProduct] = Field(
        default_factory=list, description="Found products"
    )
    pagination: Optional[Dict[str, Any]] = Field(
        default=None, description="Pagination info"
    )
    search_url: str = Field(description="Search URL")


class AmazonExtractionResult(BaseModel):
    """Amazon extraction result model."""

    success: bool = Field(description="Extraction success status")
    data: Optional[AmazonSearchResult] = Field(
        default=None, description="Extracted data"
    )
    cost_usd: float = Field(default=0.0, description="LLM cost in USD")
    processing_time: float = Field(
        default=0.0, description="Processing time in seconds"
    )
    error: Optional[str] = Field(default=None, description="Error message if failed")
