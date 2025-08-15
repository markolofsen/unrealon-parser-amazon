"""
Amazon Catalog Parser - Full catalog parser with BeautifulSoup (NO LLM)
"""

import asyncio
import re
import time
from typing import Dict, Any
from bs4 import BeautifulSoup

from unrealon_driver.src.core.parser import Parser
from unrealon_driver.src.cli.simple import SimpleParser

from amazon_config import amazon_config, parser_instance_config
from catalog.models import (
    AmazonProduct,
    AmazonSearchResult,
    AmazonExtractionResult,
    AmazonPrice,
    AmazonRating,
    AmazonImage,
)


class AmazonCatalogParser(Parser):
    """Full Amazon catalog parser with BeautifulSoup (NO LLM)."""

    def __init__(self):
        super().__init__(
            parser_id=parser_instance_config.parser_id,
            parser_name="Amazon Catalog Parser (BeautifulSoup)",
            config=amazon_config,
        )
        self.results = []
        self._operation_timer = None
        self._start_time = time.time()

    async def setup(self):
        """Setup parser with logging."""
        self.logger.info("🚀 Amazon Catalog Parser initialized (NO LLM)")

    async def search_products(
        self, query: str, max_pages: int = 2
    ) -> AmazonExtractionResult:
        """Search for products with pagination using BeautifulSoup."""
        try:
            self.logger.info(f"🔍 Searching for: {query}")

            all_products = []
            start_time = asyncio.get_event_loop().time()

            for page in range(1, max_pages + 1):
                search_url = f"https://www.amazon.com/s?k={query}&page={page}"
                self.logger.info(f"📄 Processing page {page}: {search_url}")

                # Get HTML content directly using browser service
                html_content = await self.browser.get_html(search_url)

                # Parse with BeautifulSoup
                soup = BeautifulSoup(html_content, "html.parser")

                # Extract products using selectors
                page_products = self._extract_products_from_soup(soup)
                all_products.extend(page_products)

                self.logger.info(f"✅ Page {page}: Found {len(page_products)} products")

                if not page_products:
                    self.logger.warning(f"⚠️ Page {page}: No products found")
                    break

            processing_time = asyncio.get_event_loop().time() - start_time

            # Create search result
            search_result = AmazonSearchResult(
                query=query,
                total_results=len(all_products),
                products=all_products,
                search_url=f"https://www.amazon.com/s?k={query}",
            )

            return AmazonExtractionResult(
                success=True,
                data=search_result,
                cost_usd=0.0,  # No LLM cost
                processing_time=processing_time,
            )

        except Exception as e:
            self.logger.error(f"❌ Search failed: {e}")
            return AmazonExtractionResult(
                success=False,
                error=str(e),
                cost_usd=0.0,
                processing_time=(
                    processing_time if "processing_time" in locals() else 0.0
                ),
            )

    async def get_product_details(self, asin: str) -> AmazonExtractionResult:
        """Get detailed product information by ASIN using BeautifulSoup."""
        try:
            product_url = f"https://www.amazon.com/dp/{asin}"
            self.logger.info(f"📦 Getting details for ASIN: {asin}")

            start_time = asyncio.get_event_loop().time()

            # Get HTML content using browser service
            html_content = await self.browser.get_html(product_url)

            # Parse with BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract product details
            product = self._extract_product_details_from_soup(soup)

            processing_time = asyncio.get_event_loop().time() - start_time

            return AmazonExtractionResult(
                success=product is not None,
                data=product,
                cost_usd=0.0,  # No LLM cost
                processing_time=processing_time,
            )

        except Exception as e:
            self.logger.error(f"❌ Product details failed: {e}")
            return AmazonExtractionResult(success=False, error=str(e))

    def _extract_products_from_soup(self, soup) -> list:
        """Extract products from soup using selectors."""
        products = []

        # Use working selector from original parser
        containers = soup.find_all("div", {"data-component-type": "s-search-result"})
        self.logger.info(f"Found {len(containers)} product containers")

        for container in containers:
            try:
                product = self._extract_single_product_from_soup(container)
                if product and product.asin:
                    products.append(product)
            except Exception as e:
                self.logger.warning(f"Product extraction failed: {e}")

        return products

    def _extract_single_product_from_soup(self, container) -> dict:
        """Extract single product from container."""
        try:
            # Extract ASIN
            asin = container.get("data-asin")
            if not asin:
                return None

            # Extract title
            title = self._extract_title_from_soup(container)

            # Extract price
            price = self._extract_price_from_soup(container)

            # Extract rating
            rating = self._extract_rating_from_soup(container)

            # Extract image
            image_url = self._extract_image_from_soup(container)

            # Extract additional data
            review_count = self._extract_review_count_from_soup(container)
            availability = self._extract_availability_from_soup(container)
            prime_eligible = self._extract_prime_eligible_from_soup(container)

            # Build product URL
            product_url = f"https://www.amazon.com/dp/{asin}" if asin else None

            # Create proper Pydantic objects
            price_obj = None
            if price:
                try:
                    # Extract numeric value from price string
                    price_match = re.search(
                        r"[\d,]+\.?\d*", price.replace("$", "").replace(",", "")
                    )
                    if price_match:
                        price_value = float(price_match.group().replace(",", ""))
                        price_obj = AmazonPrice(current=price_value, currency="USD")
                except:
                    pass

            rating_obj = None
            if rating:
                rating_obj = AmazonRating(rating=rating, review_count=review_count)

            image_obj = None
            if image_url:
                image_obj = AmazonImage(url=image_url, is_primary=True)

            return AmazonProduct(
                asin=asin,
                title=title or f"Product {asin}",
                price=price_obj,
                rating=rating_obj,
                availability=availability,
                images=[image_obj] if image_obj else [],
                url=product_url or f"https://www.amazon.com/dp/{asin}",
                prime_eligible=prime_eligible,
            )

        except Exception as e:
            self.logger.warning(f"Single product extraction failed: {e}")
            return None

    def _extract_title_from_soup(self, container):
        """Extract title using selectors from original parser."""
        selectors = [
            "h2.a-size-medium a span",
            ".s-line-clamp-2 span",
            "h2 span",
            ".a-link-normal .a-text-normal span",
            "h2 a span",
            "h2 a",  # Fallback for direct link
            ".a-size-medium.a-color-base.a-text-normal",  # Direct text
        ]

        for selector in selectors:
            try:
                element = container.select_one(selector)
                if element and element.get_text(strip=True):
                    return element.get_text(strip=True)
            except:
                continue
        return None

    def _extract_price_from_soup(self, container):
        """Extract price using selectors from original parser."""
        selectors = [
            ".a-price .a-offscreen",
            ".a-price-whole",
            ".puis-price-instructions-style .a-price",
            ".a-price-range .a-offscreen",  # Price range
            ".a-price .a-price-whole",  # Whole price
            ".a-price .a-price-fraction",  # Fraction part
        ]

        for selector in selectors:
            try:
                element = container.select_one(selector)
                if element and element.get_text(strip=True):
                    return element.get_text(strip=True)
            except:
                continue
        return None

    def _extract_rating_from_soup(self, container):
        """Extract rating using selectors from original parser."""
        selectors = [
            ".a-icon-star-mini .a-icon-alt",
            ".a-icon-star .a-icon-alt",
            ".a-popover-trigger .a-icon-alt",
            ".a-icon-alt",  # General star icon
            ".a-star-mini .a-icon-alt",  # Mini star
        ]

        for selector in selectors:
            try:
                element = container.select_one(selector)
                if element:
                    aria_label = element.get("aria-label")
                    if aria_label:
                        # Extract rating from "4.5 out of 5 stars" format
                        match = re.search(r"(\d+\.?\d*)", aria_label)
                        if match:
                            return float(match.group(1))
            except:
                continue
        return None

    def _extract_image_from_soup(self, container):
        """Extract image URL using selectors from original parser."""
        selectors = [
            ".s-image",
            ".s-product-image-container img",
            "img.s-image",
            ".s-image-container img",  # Alternative container
            "img[data-image-latency]",  # Data attribute
        ]

        for selector in selectors:
            try:
                element = container.select_one(selector)
                if element and element.get("src"):
                    return element.get("src")
            except:
                continue
        return None

    def _extract_review_count_from_soup(self, container):
        """Extract review count from container."""
        selectors = [
            ".s-link-style .a-size-base",
            ".a-size-base.s-link-style",
            ".a-size-base",
            ".a-link-normal .a-size-base",
        ]

        for selector in selectors:
            try:
                element = container.select_one(selector)
                if element:
                    text = element.get_text(strip=True)
                    # Extract number from text like "1,234" or "1,234 reviews"
                    match = re.search(r"([\d,]+)", text)
                    if match:
                        return int(match.group(1).replace(",", ""))
            except:
                continue
        return None

    def _extract_availability_from_soup(self, container):
        """Extract availability status."""
        selectors = [
            ".a-size-base.a-color-secondary",
            ".a-size-base.a-color-price",
            ".a-color-secondary",
        ]

        for selector in selectors:
            try:
                element = container.select_one(selector)
                if element:
                    text = element.get_text(strip=True)
                    if text and len(text) < 50:  # Avoid long descriptions
                        return text
            except:
                continue
        return None

    def _extract_prime_eligible_from_soup(self, container):
        """Check if product is Prime eligible."""
        prime_selectors = [
            ".a-icon-prime",
            ".s-prime",
            "[data-prime]",
        ]

        for selector in prime_selectors:
            try:
                element = container.select_one(selector)
                if element:
                    return True
            except:
                continue
        return False

    def _extract_product_details_from_soup(self, soup):
        """Extract product details from product page."""
        try:
            # Extract basic product info
            title_elem = soup.select_one("#productTitle")
            title = title_elem.get_text(strip=True) if title_elem else None

            price_elem = soup.select_one(".a-price .a-offscreen")
            price = price_elem.get_text(strip=True) if price_elem else None

            return {"title": title, "price": price, "page_type": "product_details"}
        except Exception as e:
            self.logger.warning(f"Product details extraction failed: {e}")
            return None

    async def parse(self) -> Dict[str, Any]:
        """Default parse method for scheduled execution."""
        try:
            # Default search query
            # https://www.amazon.com/s?k=laptop&page=1
            
            query = "laptop"
            result = await self.search_products(query, max_pages=1)

            return {
                "success": result.success,
                "query": query,
                "products_count": len(result.data.products) if result.data else 0,
                "cost_usd": result.cost_usd,
                "processing_time": result.processing_time,
                "error": result.error,
            }

        except Exception as e:
            self.logger.error(f"❌ Parse failed: {e}")
            return {"success": False, "error": str(e)}

    async def cleanup(self):
        """Cleanup resources."""
        await super().cleanup()


class AmazonSchedulerWrapper(SimpleParser):
    """SimpleParser wrapper for AmazonCatalogParser with CLI capabilities."""

    def __init__(self):
        super().__init__(parser_instance_config)
        self.parser = AmazonCatalogParser()

    async def setup(self) -> None:
        """Setup - delegate to actual parser."""
        await self.parser.setup()

    async def cleanup(self) -> None:
        """Cleanup - delegate to actual parser."""
        await self.parser.cleanup()
        await super().cleanup()

    async def parse_data(self) -> dict:
        """Parse data - delegate to actual parser."""
        result = await self.parser.parse()
        return result


# CLI usage
if __name__ == "__main__":

    async def main():
        parser = AmazonCatalogParser()
        try:
            await parser.setup()

            # Test search
            result = await parser.search_products("laptop", max_pages=1)
            print(f"Search Result: {result.success}")
            print(f"Products Found: {len(result.data.products) if result.data else 0}")
            print(f"Cost: ${result.cost_usd:.4f}")
            print(f"Time: {result.processing_time:.2f}s")

        finally:
            await parser.cleanup()

    asyncio.run(main())
