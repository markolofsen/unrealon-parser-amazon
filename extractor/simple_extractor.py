"""
Amazon Simple Extractor - CLEAN AND SIMPLE

Just extract Amazon products. No bloat, no bullshit.
"""

import asyncio
import sys
from pathlib import Path


from unrealon_driver.src.core.parser import Parser
from amazon_config import amazon_config, parser_instance_config

test_url = "https://www.amazon.com/s?k=laptop"


class SimpleExtractor(Parser):
    """🔥 Simple Amazon extractor - ZERO SETUP REQUIRED!"""

    def __init__(self):
        # 🔥 USE EXTENDED AMAZON CONFIG DIRECTLY!
        super().__init__(
            parser_id=parser_instance_config.parser_id,
            parser_name="Amazon Simple Extractor",
            config=amazon_config,  # Pass the whole extended config!
        )

    async def setup(self):
        """🔥 NO SETUP NEEDED! BrowserLLMService is auto-activated in Parser!"""
        self.logger.info("✅ Amazon extractor ready - ZERO SETUP!")

    async def extract_products(self, url: str) -> dict:
        """🔥 Extract products - using auto-activated browser_llm service!"""
        try:
            clean_url = clean_amazon_url(url)
            self.logger.info(f"🛒 Extracting: {clean_url}")

            # 🔥 USE self.browser_llm - NO MANUAL INITIALIZATION!
            result = await self.browser_llm.extract_listing(clean_url)

            return {
                "products": result.data,
                "success": result.success,
                "cost": getattr(result, "cost_usd", 0.0) or 0.0,
            }

        except Exception as e:
            self.logger.error(f"❌ Failed: {e}")
            return {"products": None, "success": False, "cost": 0.0}

    async def extract_details(self, url: str) -> dict:
        """🔥 Extract product details - using auto-activated browser_llm service!"""
        try:
            clean_url = clean_amazon_url(url)
            self.logger.info(f"📦 Extracting details: {clean_url}")

            # 🔥 USE self.browser_llm - NO MANUAL INITIALIZATION!
            result = await self.browser_llm.extract_details(clean_url)

            return {
                "details": result.data,
                "success": result.success,
                "cost": getattr(result, "cost_usd", 0.0) or 0.0,
            }

        except Exception as e:
            self.logger.error(f"❌ Failed: {e}")
            return {"details": None, "success": False, "cost": 0.0}

    async def parse(self) -> dict:
        """Default parse method."""
        return await self.extract_products(test_url)

    async def cleanup(self):
        """🔥 Cleanup handled automatically by Parser base class!"""
        await super().cleanup()


# Utility functions
def clean_amazon_url(url: str) -> str:
    """Remove tracking garbage from Amazon URLs."""
    from urllib.parse import urlparse, parse_qs, urlencode

    parsed = urlparse(url)
    if "amazon.com" not in parsed.netloc:
        return url

    params = parse_qs(parsed.query)
    essential = {}
    for param in ["k", "i", "bbn", "rh", "node", "page"]:
        if param in params:
            essential[param] = params[param][0]

    clean_query = urlencode(essential) if essential else ""
    clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    if clean_query:
        clean_url += f"?{clean_query}"

    return clean_url


# CLI
if __name__ == "__main__":
    import sys

    async def main():
        extractor = SimpleExtractor()
        try:
            await extractor.setup()
            
            # Check if details mode is requested
            if len(sys.argv) > 1 and sys.argv[1] == "details":
                print("🚀 Amazon Simple Extractor - DETAILS MODE")
                print("=" * 60)
                test_details_url = "https://www.amazon.com/dp/B0D1XD1ZV3"
                result = await extractor.extract_details(test_details_url)
                print(f"📋 Testing details extraction: {test_details_url}")
            else:
                print("🚀 Amazon Simple Extractor - LISTING MODE")
                print("=" * 60)
                result = await extractor.parse()
                print(f"📋 Testing listing extraction: {test_url}")

            print(f"📊 Result: {'✅ Success' if result['success'] else '❌ Failed'}")
            print(f"💰 Cost: ${result['cost']:.4f}")
            
            if result.get("products"):
                products = result["products"].get("products", [])
                print(f"🛒 Products: {len(products)}")
            elif result.get("details"):
                print(f"📦 Details extracted successfully")
                
            print(f"🔥 Version: v4.0 (NEW LLM API)")

        finally:
            await extractor.cleanup()

    asyncio.run(main())
