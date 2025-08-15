# 🛒 Amazon Parser - Professional Amazon Data Extraction Tool

**Enterprise-grade Amazon scraper with AI-powered automation, anti-detection, and real-time monitoring capabilities.**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![UnrealOn](https://img.shields.io/badge/UnrealOn-green.svg)](https://pypi.org/project/unrealon/)

## 🎯 Overview

**Amazon Parser** is a production-ready Python tool for extracting comprehensive product data from Amazon.com. Built on the **[UnrealOn](https://unrealon.com)** platform ([PyPI Package](https://pypi.org/project/unrealon/)), it provides enterprise-grade web scraping capabilities with AI-powered automation, anti-bot detection, and real-time orchestration.

**Perfect for**: E-commerce intelligence, price monitoring, product research, competitive analysis, and Amazon data collection at scale.

## 🚀 Ready-to-Use Project

**Get started immediately with our pre-configured Amazon parser:**
- **Complete Amazon parser** with all configurations and optimizations
- **Zero Setup**: Clone and run with minimal configuration
- **Production Ready**: Includes all enterprise features and optimizations

## 🚀 Key Features

### ✅ **AI-Powered Amazon Data Extraction**
- **Automatic Selector Generation**: AI identifies optimal CSS selectors for Amazon's dynamic layout
- **Smart Content Analysis**: Intelligent parsing of product listings, prices, ratings, and reviews
- **Adaptive Extraction**: Handles Amazon's frequent layout changes automatically

### ✅ **Anti-Detection & Stealth Technology**
- **Advanced Browser Automation**: Chromium with stealth plugins and anti-detection measures
- **Proxy Rotation**: Built-in proxy management for IP rotation
- **Human-like Behavior**: Realistic browsing patterns and timing
- **Cookie Management**: Persistent sessions and profile management

### ✅ **Enterprise-Grade Architecture**
- **Real-time Monitoring**: Live parser status and performance metrics
- **Scalable Design**: Horizontal scaling with load balancing
- **Error Recovery**: Automatic retry mechanisms and failover
- **Compliance Ready**: Audit trails and data governance features

### ✅ **Zero Configuration Setup**
- **Production Defaults**: Optimized settings for Amazon scraping
- **Auto-detection**: Automatic detection of Amazon page types
- **Smart Waiting**: Intelligent content loading and dynamic content handling

## 📊 What Data Can You Extract?

### 🛍️ **Product Information**
```json
{
  "asin": "B0DTW26PXY",
  "title": "Lenovo IdeaPad 3 15.6\" HD Laptop",
  "price": {
    "current": 799.99,
    "currency": "USD",
    "original": 899.99,
    "discount_percent": 11
  },
  "rating": {
    "rating": 4.5,
    "review_count": 1247,
    "rating_text": "4.5 out of 5 stars"
  },
  "availability": "In Stock",
  "prime_eligible": true,
  "images": [
    {
      "url": "https://m.media-amazon.com/images/I/71...",
      "is_primary": true
    }
  ],
  "url": "https://www.amazon.com/dp/B0DTW26PXY"
}
```

### 📋 **Search Results & Categories**
- Product listings from search results
- Category browsing and navigation
- Pagination handling
- Filter and sort options
- Sponsored vs organic listings

### 📈 **Pricing & Availability**
- Current and original prices
- Discount percentages
- Price history tracking
- Stock availability status
- Shipping information

### ⭐ **Reviews & Ratings**
- Star ratings (1-5)
- Review counts
- Rating distribution
- Review text extraction
- Verified purchase badges

## 🏗️ Architecture

### Core Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Amazon Parser │◄──►│  UnrealOn       │◄──►│  Amazon.com     │
│   (Client)      │    │  (Platform)     │    │  (Target)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Services   │    │   Browser       │    │   Proxy &       │
│   (LLM)         │    │   Automation    │    │   Stealth       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Module Structure

- **`catalog/`**: Product catalog parsing and data models
- **`extractor/`**: Simple extraction utilities
- **`amazon_config.py`**: Amazon-specific configuration
- **`config.env`**: Environment variables and API keys

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Poetry for dependency management
- OpenRouter API key (for AI-powered extraction)

### Installation

```bash
# Clone the repository
git clone https://github.com/markolofsen/unrealon-parser-amazon.git
cd unrealon-parser-amazon

# Install dependencies
poetry install

# Configure environment
cp config.env.example config.env
# Edit config.env with your API keys
```

### Basic Usage

```python
from catalog.parser import AmazonCatalogParser

async def main():
    # Initialize parser
    parser = AmazonCatalogParser()
    await parser.setup()
    
    # Search for products
    result = await parser.search_products("laptop", max_pages=2)
    
    if result.success:
        print(f"Found {len(result.data.products)} products")
        for product in result.data.products:
            print(f"- {product.title}: ${product.price.current}")
    
    await parser.cleanup()

# Run the parser
import asyncio
asyncio.run(main())
```

### Advanced Usage with AI

```python
from extractor.simple_extractor import SimpleExtractor

async def ai_extraction():
    extractor = SimpleExtractor()
    await extractor.setup()
    
    # AI-powered extraction with automatic selector generation
    result = await extractor.extract_products(
        "https://www.amazon.com/s?k=laptop"
    )
    
    print(f"AI extracted {len(result.products)} products")
    print(f"Confidence: {result.confidence}%")
    print(f"Cost: ${result.cost_usd:.4f}")
    
    await extractor.cleanup()
```

## ⚙️ Configuration

### Environment Variables

Create a `config.env` file:

```bash
# API Keys
UNREALON_OPENROUTER_API_KEY=sk-or-v1-your-openrouter-key

# Browser Settings
UNREALON_BROWSER_HEADLESS=true
UNREALON_BROWSER_TIMEOUT=30

# Runtime Limits
UNREALON_MAX_PAGES=5
UNREALON_LLM_DAILY_LIMIT=10.0

# Logging
UNREALON_LOG_LEVEL=INFO
```

### Custom Configuration

```python
from amazon_config import amazon_config, parser_instance_config

class CustomAmazonParser(AmazonCatalogParser):
    def __init__(self):
        super().__init__(
            parser_id="my_amazon_parser",
            parser_name="Custom Amazon Parser",
            config=amazon_config
        )
    
    async def parse_specific_category(self, category: str):
        """Parse specific Amazon category."""
        return await self.search_products(category, max_pages=3)
```

## 📈 Performance & Scalability

### Benchmarks

| Metric | Traditional Scrapers | Amazon Parser |
|--------|---------------------|---------------|
| **Success Rate** | 60-80% | 95%+ |
| **Detection Rate** | High | <5% |
| **Data Accuracy** | 70-85% | 95%+ |
| **Setup Time** | Days/Weeks | Minutes |
| **Maintenance** | High | Minimal |

### Scalability Features

- **Horizontal Scaling**: Add parser instances without code changes
- **Load Balancing**: Automatic distribution of parsing tasks
- **Rate Limiting**: Built-in Amazon-friendly request pacing
- **Proxy Rotation**: Automatic IP rotation and management
- **Session Management**: Persistent browser profiles

## 🔒 Security & Compliance

### Anti-Detection Measures

- **Stealth Browser**: Chromium with anti-detection plugins
- **Human-like Behavior**: Realistic mouse movements and timing
- **Header Rotation**: Dynamic User-Agent and header management
- **Cookie Handling**: Proper session management and persistence
- **Proxy Support**: Built-in proxy rotation and management

### Data Privacy

- **Local Processing**: Data processed on your infrastructure
- **No Data Storage**: No data stored on external servers
- **API Key Security**: Secure handling of API credentials
- **Audit Logging**: Comprehensive audit trails

## 🛠️ Development & Testing

### Testing Framework

```python
import pytest
from catalog.parser import AmazonCatalogParser

@pytest.mark.asyncio
async def test_product_extraction():
    parser = AmazonCatalogParser()
    await parser.setup()
    
    result = await parser.search_products("laptop", max_pages=1)
    
    assert result.success
    assert len(result.data.products) > 0
    assert all(p.asin for p in result.data.products)
    
    await parser.cleanup()
```

### CLI Interface

```bash
# Test mode
poetry run python -m catalog.parser

# Scheduled mode
poetry run python -m catalog.parser --schedule "every 1h"

# Daemon mode
poetry run python -m catalog.parser --daemon
```

## 📊 Use Cases & Applications

### 🏢 **E-commerce Intelligence**
- **Price Monitoring**: Track competitor pricing strategies
- **Product Research**: Analyze market trends and product performance
- **Inventory Tracking**: Monitor stock levels and availability
- **Competitive Analysis**: Benchmark against competitors

### 📈 **Market Research**
- **Trend Analysis**: Identify emerging product categories
- **Demand Forecasting**: Analyze search volume and interest
- **Customer Insights**: Study review patterns and sentiment
- **Market Positioning**: Understand product positioning

### 💰 **Investment & Finance**
- **Company Analysis**: Monitor Amazon's business performance
- **Market Sentiment**: Analyze customer satisfaction trends
- **Supply Chain**: Track product availability and shipping
- **Economic Indicators**: Monitor consumer spending patterns

### 🎓 **Academic Research**
- **Consumer Behavior**: Study purchasing patterns and preferences
- **Market Dynamics**: Analyze competition and pricing strategies
- **Data Science**: Large-scale e-commerce data collection
- **Social Research**: Study online shopping behavior

## 🔧 Troubleshooting

### Common Issues

**Q: Parser gets blocked by Amazon**
A: Enable stealth mode and use proxy rotation. The parser includes built-in anti-detection measures.

**Q: Missing product data**
A: Check if selectors need updating. The AI-powered extraction automatically adapts to layout changes.

**Q: High API costs**
A: Use traditional BeautifulSoup parsing for cost-free extraction, or optimize LLM usage with caching.

**Q: Slow performance**
A: Adjust browser settings, enable headless mode, and optimize page limits.

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable browser debugging
parser = AmazonCatalogParser()
parser.config.browser_config.debug_mode = True
```

## 📚 API Reference

### Core Classes

#### `AmazonCatalogParser`

Main parser class for Amazon product extraction.

```python
class AmazonCatalogParser(Parser):
    async def search_products(query: str, max_pages: int = 2) -> AmazonExtractionResult
    async def get_product_details(asin: str) -> AmazonExtractionResult
    async def parse() -> Dict[str, Any]
```

#### `AmazonProduct`

Pydantic model for product data.

```python
class AmazonProduct(BaseModel):
    asin: str
    title: str
    price: Optional[AmazonPrice]
    rating: Optional[AmazonRating]
    availability: Optional[str]
    images: List[AmazonImage]
    url: str
    prime_eligible: bool
```

### Data Models

#### `AmazonPrice`
```python
class AmazonPrice(BaseModel):
    current: Optional[float]
    original: Optional[float]
    currency: str = "USD"
    discount_percent: Optional[int]
```

#### `AmazonRating`
```python
class AmazonRating(BaseModel):
    rating: Optional[float]
    review_count: Optional[int]
    rating_text: Optional[str]
```

---

**Amazon Parser** - Professional Amazon data extraction powered by [UnrealOn](https://pypi.org/project/unrealon/).

*Built for developers, by developers. No vendor lock-in, predictable pricing, enterprise-grade reliability.*

**For enterprise features, managed hosting, and professional support, visit [unrealon.com](https://unrealon.com/).**
