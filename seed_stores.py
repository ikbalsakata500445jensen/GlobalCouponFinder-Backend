from database import SessionLocal
from models_sqlite import Store, Category
from sqlalchemy.orm import Session
import json

# AMERICA - RETAIL STORES (40 stores)
AMERICA_RETAIL_STORES = [
    {
        "name": "Amazon US",
        "slug": "amazon-us",
        "domain": "amazon.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "amazon",
        "affiliate_id": "tag-20",
        "scraper_config": {
            "type": "api",
            "api_endpoint": "https://api.amazon.com/coupons",
            "selectors": {}
        }
    },
    {
        "name": "Walmart",
        "slug": "walmart",
        "domain": "walmart.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "impact",
        "scraper_config": {
            "type": "generic",
            "coupon_list_url": "https://www.walmart.com/cp/coupons/1078524",
            "selectors": {
                "coupon_container": ".coupon-card",
                "code": ".coupon-code",
                "title": ".coupon-title",
                "description": ".coupon-description",
                "expiry": ".expiry-date"
            }
        }
    },
    {
        "name": "Target",
        "slug": "target",
        "domain": "target.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "shareasale",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Best Buy",
        "slug": "bestbuy",
        "domain": "bestbuy.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "electronics",
        "affiliate_network": "cj",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Macy's",
        "slug": "macys",
        "domain": "macys.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "rakuten",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Kohl's",
        "slug": "kohls",
        "domain": "kohls.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "shareasale",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Nordstrom",
        "slug": "nordstrom",
        "domain": "nordstrom.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "rakuten",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Home Depot",
        "slug": "homedepot",
        "domain": "homedepot.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "home-garden",
        "affiliate_network": "cj",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Lowe's",
        "slug": "lowes",
        "domain": "lowes.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "home-garden",
        "affiliate_network": "impact",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Sephora US",
        "slug": "sephora-us",
        "domain": "sephora.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "beauty",
        "affiliate_network": "rakuten",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Ulta Beauty",
        "slug": "ulta",
        "domain": "ulta.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "beauty",
        "affiliate_network": "impact",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "PetSmart",
        "slug": "petsmart",
        "domain": "petsmart.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "pet-supplies",
        "affiliate_network": "cj",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Chewy",
        "slug": "chewy",
        "domain": "chewy.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "pet-supplies",
        "affiliate_network": "cj",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Wayfair",
        "slug": "wayfair",
        "domain": "wayfair.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "home-garden",
        "affiliate_network": "cj",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Overstock",
        "slug": "overstock",
        "domain": "overstock.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "home-garden",
        "affiliate_network": "impact",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Newegg",
        "slug": "newegg",
        "domain": "newegg.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "electronics",
        "affiliate_network": "cj",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Nike US",
        "slug": "nike-us",
        "domain": "nike.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "sports",
        "affiliate_network": "cj",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Adidas US",
        "slug": "adidas-us",
        "domain": "adidas.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "sports",
        "affiliate_network": "rakuten",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Under Armour",
        "slug": "underarmour",
        "domain": "underarmour.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "sports",
        "affiliate_network": "cj",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Gap",
        "slug": "gap",
        "domain": "gap.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "rakuten",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Old Navy",
        "slug": "oldnavy",
        "domain": "oldnavy.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "rakuten",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Banana Republic",
        "slug": "bananarepublic",
        "domain": "bananarepublic.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "rakuten",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Forever 21",
        "slug": "forever21",
        "domain": "forever21.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "shareasale",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "H&M US",
        "slug": "hm-us",
        "domain": "hm.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Zara US",
        "slug": "zara-us",
        "domain": "zara.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "eBay US",
        "slug": "ebay-us",
        "domain": "ebay.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "ebay",
        "scraper_config": {"type": "api"}
    },
    {
        "name": "Etsy",
        "slug": "etsy",
        "domain": "etsy.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "awin",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "AliExpress US",
        "slug": "aliexpress-us",
        "domain": "aliexpress.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "admitad",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Shein US",
        "slug": "shein-us",
        "domain": "us.shein.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "cj",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Temu US",
        "slug": "temu-us",
        "domain": "temu.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "impact",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "JCPenney",
        "slug": "jcpenney",
        "domain": "jcpenney.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "rakuten",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Staples",
        "slug": "staples",
        "domain": "staples.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "office",
        "affiliate_network": "cj",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Office Depot",
        "slug": "officedepot",
        "domain": "officedepot.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "office",
        "affiliate_network": "cj",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "GameStop",
        "slug": "gamestop",
        "domain": "gamestop.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "electronics",
        "affiliate_network": "cj",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "CVS Pharmacy",
        "slug": "cvs",
        "domain": "cvs.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "health-wellness",
        "affiliate_network": "cj",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Walgreens",
        "slug": "walgreens",
        "domain": "walgreens.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "health-wellness",
        "affiliate_network": "rakuten",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "GNC",
        "slug": "gnc",
        "domain": "gnc.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "health-wellness",
        "affiliate_network": "shareasale",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Victoria's Secret",
        "slug": "victoriassecret",
        "domain": "victoriassecret.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "rakuten",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Bath & Body Works",
        "slug": "bathandbodyworks",
        "domain": "bathandbodyworks.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "beauty",
        "affiliate_network": "rakuten",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "American Eagle",
        "slug": "americaneagle",
        "domain": "ae.com",
        "region": "america",
        "country": "US",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "rakuten",
        "scraper_config": {"type": "generic"}
    },
]

# AMERICA - FOOD DELIVERY (10 stores)
AMERICA_FOOD_DELIVERY = [
    {
        "name": "Uber Eats US",
        "slug": "ubereats-us",
        "domain": "ubereats.com",
        "region": "america",
        "country": "US",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "impact",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "DoorDash",
        "slug": "doordash",
        "domain": "doordash.com",
        "region": "america",
        "country": "US",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "cj",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Grubhub",
        "slug": "grubhub",
        "domain": "grubhub.com",
        "region": "america",
        "country": "US",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "cj",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Postmates",
        "slug": "postmates",
        "domain": "postmates.com",
        "region": "america",
        "country": "US",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "impact",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Seamless",
        "slug": "seamless",
        "domain": "seamless.com",
        "region": "america",
        "country": "US",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "cj",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Instacart",
        "slug": "instacart",
        "domain": "instacart.com",
        "region": "america",
        "country": "US",
        "store_type": "food_delivery",
        "category": "food-grocery",
        "affiliate_network": "impact",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Uber Eats Canada",
        "slug": "ubereats-ca",
        "domain": "ubereats.ca",
        "region": "america",
        "country": "CA",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "impact",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "SkipTheDishes",
        "slug": "skipthedishes",
        "domain": "skipthedishes.com",
        "region": "america",
        "country": "CA",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "DoorDash Canada",
        "slug": "doordash-ca",
        "domain": "doordash.ca",
        "region": "america",
        "country": "CA",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "cj",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Rappi",
        "slug": "rappi",
        "domain": "rappi.com",
        "region": "america",
        "country": "MX",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "admitad",
        "scraper_config": {"type": "javascript"}
    },
]

# EUROPE - RETAIL STORES (30 stores)
EUROPE_RETAIL_STORES = [
    {
        "name": "Amazon UK",
        "slug": "amazon-uk",
        "domain": "amazon.co.uk",
        "region": "europe",
        "country": "GB",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "amazon",
        "scraper_config": {"type": "api"}
    },
    {
        "name": "Amazon Germany",
        "slug": "amazon-de",
        "domain": "amazon.de",
        "region": "europe",
        "country": "DE",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "amazon",
        "scraper_config": {"type": "api"}
    },
    {
        "name": "Amazon France",
        "slug": "amazon-fr",
        "domain": "amazon.fr",
        "region": "europe",
        "country": "FR",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "amazon",
        "scraper_config": {"type": "api"}
    },
    {
        "name": "Amazon Spain",
        "slug": "amazon-es",
        "domain": "amazon.es",
        "region": "europe",
        "country": "ES",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "amazon",
        "scraper_config": {"type": "api"}
    },
    {
        "name": "Amazon Italy",
        "slug": "amazon-it",
        "domain": "amazon.it",
        "region": "europe",
        "country": "IT",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "amazon",
        "scraper_config": {"type": "api"}
    },
    {
        "name": "Zalando",
        "slug": "zalando",
        "domain": "zalando.com",
        "region": "europe",
        "country": "DE",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "ASOS",
        "slug": "asos",
        "domain": "asos.com",
        "region": "europe",
        "country": "GB",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Tesco",
        "slug": "tesco",
        "domain": "tesco.com",
        "region": "europe",
        "country": "GB",
        "store_type": "retail",
        "category": "food-grocery",
        "affiliate_network": "awin",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Sainsbury's",
        "slug": "sainsburys",
        "domain": "sainsburys.co.uk",
        "region": "europe",
        "country": "GB",
        "store_type": "retail",
        "category": "food-grocery",
        "affiliate_network": "awin",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Argos",
        "slug": "argos",
        "domain": "argos.co.uk",
        "region": "europe",
        "country": "GB",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "awin",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "John Lewis",
        "slug": "johnlewis",
        "domain": "johnlewis.com",
        "region": "europe",
        "country": "GB",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "awin",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Currys",
        "slug": "currys",
        "domain": "currys.co.uk",
        "region": "europe",
        "country": "GB",
        "store_type": "retail",
        "category": "electronics",
        "affiliate_network": "awin",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "MediaMarkt",
        "slug": "mediamarkt",
        "domain": "mediamarkt.de",
        "region": "europe",
        "country": "DE",
        "store_type": "retail",
        "category": "electronics",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Saturn",
        "slug": "saturn",
        "domain": "saturn.de",
        "region": "europe",
        "country": "DE",
        "store_type": "retail",
        "category": "electronics",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Carrefour",
        "slug": "carrefour",
        "domain": "carrefour.fr",
        "region": "europe",
        "country": "FR",
        "store_type": "retail",
        "category": "food-grocery",
        "affiliate_network": "awin",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Decathlon",
        "slug": "decathlon",
        "domain": "decathlon.com",
        "region": "europe",
        "country": "FR",
        "store_type": "retail",
        "category": "sports",
        "affiliate_network": "awin",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "H&M Europe",
        "slug": "hm-eu",
        "domain": "hm.co.uk",
        "region": "europe",
        "country": "GB",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Zara Europe",
        "slug": "zara-eu",
        "domain": "zara.es",
        "region": "europe",
        "country": "ES",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Mango",
        "slug": "mango",
        "domain": "mango.com",
        "region": "europe",
        "country": "ES",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Pull & Bear",
        "slug": "pullandbear",
        "domain": "pullandbear.com",
        "region": "europe",
        "country": "ES",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Bershka",
        "slug": "bershka",
        "domain": "bershka.com",
        "region": "europe",
        "country": "ES",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Stradivarius",
        "slug": "stradivarius",
        "domain": "stradivarius.com",
        "region": "europe",
        "country": "ES",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Primark",
        "slug": "primark",
        "domain": "primark.com",
        "region": "europe",
        "country": "GB",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "awin",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Boots",
        "slug": "boots",
        "domain": "boots.com",
        "region": "europe",
        "country": "GB",
        "store_type": "retail",
        "category": "beauty",
        "affiliate_network": "awin",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Superdrug",
        "slug": "superdrug",
        "domain": "superdrug.com",
        "region": "europe",
        "country": "GB",
        "store_type": "retail",
        "category": "beauty",
        "affiliate_network": "awin",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Fnac",
        "slug": "fnac",
        "domain": "fnac.com",
        "region": "europe",
        "country": "FR",
        "store_type": "retail",
        "category": "electronics",
        "affiliate_network": "awin",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "El Corte Inglés",
        "slug": "elcorteingles",
        "domain": "elcorteingles.es",
        "region": "europe",
        "country": "ES",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "awin",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Douglas",
        "slug": "douglas",
        "domain": "douglas.de",
        "region": "europe",
        "country": "DE",
        "store_type": "retail",
        "category": "beauty",
        "affiliate_network": "awin",
        "scraper_config": {"type": "generic"}
    },
    {
        "name": "Notino",
        "slug": "notino",
        "domain": "notino.com",
        "region": "europe",
        "country": "CZ",
        "store_type": "retail",
        "category": "beauty",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "About You",
        "slug": "aboutyou",
        "domain": "aboutyou.de",
        "region": "europe",
        "country": "DE",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
]

# EUROPE - FOOD DELIVERY (10 stores)
EUROPE_FOOD_DELIVERY = [
    {
        "name": "Uber Eats UK",
        "slug": "ubereats-uk",
        "domain": "ubereats.co.uk",
        "region": "europe",
        "country": "GB",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "impact",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Deliveroo UK",
        "slug": "deliveroo-uk",
        "domain": "deliveroo.co.uk",
        "region": "europe",
        "country": "GB",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Just Eat UK",
        "slug": "justeat-uk",
        "domain": "just-eat.co.uk",
        "region": "europe",
        "country": "GB",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Uber Eats Germany",
        "slug": "ubereats-de",
        "domain": "ubereats.de",
        "region": "europe",
        "country": "DE",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "impact",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Lieferando",
        "slug": "lieferando",
        "domain": "lieferando.de",
        "region": "europe",
        "country": "DE",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Uber Eats France",
        "slug": "ubereats-fr",
        "domain": "ubereats.fr",
        "region": "europe",
        "country": "FR",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "impact",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Deliveroo France",
        "slug": "deliveroo-fr",
        "domain": "deliveroo.fr",
        "region": "europe",
        "country": "FR",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Just Eat Spain",
        "slug": "justeat-es",
        "domain": "just-eat.es",
        "region": "europe",
        "country": "ES",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Glovo",
        "slug": "glovo",
        "domain": "glovoapp.com",
        "region": "europe",
        "country": "ES",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Wolt",
        "slug": "wolt",
        "domain": "wolt.com",
        "region": "europe",
        "country": "FI",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
]

# ASIA - RETAIL STORES (30 stores)
ASIA_RETAIL_STORES = [
    {
        "name": "Lazada Singapore",
        "slug": "lazada-sg",
        "domain": "lazada.sg",
        "region": "asia",
        "country": "SG",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "lazada",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Lazada Malaysia",
        "slug": "lazada-my",
        "domain": "lazada.com.my",
        "region": "asia",
        "country": "MY",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "lazada",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Lazada Thailand",
        "slug": "lazada-th",
        "domain": "lazada.co.th",
        "region": "asia",
        "country": "TH",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "lazada",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Lazada Philippines",
        "slug": "lazada-ph",
        "domain": "lazada.com.ph",
        "region": "asia",
        "country": "PH",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "lazada",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Lazada Indonesia",
        "slug": "lazada-id",
        "domain": "lazada.co.id",
        "region": "asia",
        "country": "ID",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "lazada",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Lazada Vietnam",
        "slug": "lazada-vn",
        "domain": "lazada.vn",
        "region": "asia",
        "country": "VN",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "lazada",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Shopee Singapore",
        "slug": "shopee-sg",
        "domain": "shopee.sg",
        "region": "asia",
        "country": "SG",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "shopee",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Shopee Malaysia",
        "slug": "shopee-my",
        "domain": "shopee.com.my",
        "region": "asia",
        "country": "MY",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "shopee",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Shopee Thailand",
        "slug": "shopee-th",
        "domain": "shopee.co.th",
        "region": "asia",
        "country": "TH",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "shopee",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Shopee Philippines",
        "slug": "shopee-ph",
        "domain": "shopee.ph",
        "region": "asia",
        "country": "PH",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "shopee",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Shopee Indonesia",
        "slug": "shopee-id",
        "domain": "shopee.co.id",
        "region": "asia",
        "country": "ID",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "shopee",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Shopee Vietnam",
        "slug": "shopee-vn",
        "domain": "shopee.vn",
        "region": "asia",
        "country": "VN",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "shopee",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Shopee Taiwan",
        "slug": "shopee-tw",
        "domain": "shopee.tw",
        "region": "asia",
        "country": "TW",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "shopee",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Tokopedia",
        "slug": "tokopedia",
        "domain": "tokopedia.com",
        "region": "asia",
        "country": "ID",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "tokopedia",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Bukalapak",
        "slug": "bukalapak",
        "domain": "bukalapak.com",
        "region": "asia",
        "country": "ID",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "bukalapak",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Qoo10 Singapore",
        "slug": "qoo10-sg",
        "domain": "qoo10.sg",
        "region": "asia",
        "country": "SG",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "qoo10",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Taobao",
        "slug": "taobao",
        "domain": "taobao.com",
        "region": "asia",
        "country": "CN",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "alimama",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Tmall",
        "slug": "tmall",
        "domain": "tmall.com",
        "region": "asia",
        "country": "CN",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "alimama",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "JD.com",
        "slug": "jd",
        "domain": "jd.com",
        "region": "asia",
        "country": "CN",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "jd",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Flipkart",
        "slug": "flipkart",
        "domain": "flipkart.com",
        "region": "asia",
        "country": "IN",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "flipkart",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Amazon India",
        "slug": "amazon-in",
        "domain": "amazon.in",
        "region": "asia",
        "country": "IN",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "amazon",
        "scraper_config": {"type": "api"}
    },
    {
        "name": "Myntra",
        "slug": "myntra",
        "domain": "myntra.com",
        "region": "asia",
        "country": "IN",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "flipkart",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Ajio",
        "slug": "ajio",
        "domain": "ajio.com",
        "region": "asia",
        "country": "IN",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "cj",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Nykaa",
        "slug": "nykaa",
        "domain": "nykaa.com",
        "region": "asia",
        "country": "IN",
        "store_type": "retail",
        "category": "beauty",
        "affiliate_network": "admitad",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "BigBasket",
        "slug": "bigbasket",
        "domain": "bigbasket.com",
        "region": "asia",
        "country": "IN",
        "store_type": "retail",
        "category": "food-grocery",
        "affiliate_network": "admitad",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Snapdeal",
        "slug": "snapdeal",
        "domain": "snapdeal.com",
        "region": "asia",
        "country": "IN",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "admitad",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Meesho",
        "slug": "meesho",
        "domain": "meesho.com",
        "region": "asia",
        "country": "IN",
        "store_type": "retail",
        "category": "fashion",
        "affiliate_network": "meesho",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Rakuten Japan",
        "slug": "rakuten-jp",
        "domain": "rakuten.co.jp",
        "region": "asia",
        "country": "JP",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "rakuten",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Coupang",
        "slug": "coupang",
        "domain": "coupang.com",
        "region": "asia",
        "country": "KR",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "coupang",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Gmarket",
        "slug": "gmarket",
        "domain": "gmarket.co.kr",
        "region": "asia",
        "country": "KR",
        "store_type": "retail",
        "category": "general",
        "affiliate_network": "gmarket",
        "scraper_config": {"type": "javascript"}
    },
]

# ASIA - FOOD DELIVERY (15 stores)
ASIA_FOOD_DELIVERY = [
    {
        "name": "GrabFood Singapore",
        "slug": "grabfood-sg",
        "domain": "grab.com/sg/food",
        "region": "asia",
        "country": "SG",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "grab",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "GrabFood Malaysia",
        "slug": "grabfood-my",
        "domain": "grab.com/my/food",
        "region": "asia",
        "country": "MY",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "grab",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "GrabFood Thailand",
        "slug": "grabfood-th",
        "domain": "grab.com/th/food",
        "region": "asia",
        "country": "TH",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "grab",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "GrabFood Philippines",
        "slug": "grabfood-ph",
        "domain": "grab.com/ph/food",
        "region": "asia",
        "country": "PH",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "grab",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "GrabFood Indonesia",
        "slug": "grabfood-id",
        "domain": "grab.com/id/food",
        "region": "asia",
        "country": "ID",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "grab",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Foodpanda Singapore",
        "slug": "foodpanda-sg",
        "domain": "foodpanda.sg",
        "region": "asia",
        "country": "SG",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Foodpanda Malaysia",
        "slug": "foodpanda-my",
        "domain": "foodpanda.my",
        "region": "asia",
        "country": "MY",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Foodpanda Thailand",
        "slug": "foodpanda-th",
        "domain": "foodpanda.co.th",
        "region": "asia",
        "country": "TH",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Zomato India",
        "slug": "zomato-in",
        "domain": "zomato.com",
        "region": "asia",
        "country": "IN",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "admitad",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Swiggy",
        "slug": "swiggy",
        "domain": "swiggy.com",
        "region": "asia",
        "country": "IN",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "admitad",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Uber Eats India",
        "slug": "ubereats-in",
        "domain": "ubereats.in",
        "region": "asia",
        "country": "IN",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "impact",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Deliveroo Singapore",
        "slug": "deliveroo-sg",
        "domain": "deliveroo.com.sg",
        "region": "asia",
        "country": "SG",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "awin",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "GoFood",
        "slug": "gofood",
        "domain": "gofood.co.id",
        "region": "asia",
        "country": "ID",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "gojek",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "Shopeefood",
        "slug": "shopeefood",
        "domain": "shopeefood.vn",
        "region": "asia",
        "country": "VN",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "shopee",
        "scraper_config": {"type": "javascript"}
    },
    {
        "name": "LINE MAN",
        "slug": "lineman",
        "domain": "lineman.line.me",
        "region": "asia",
        "country": "TH",
        "store_type": "food_delivery",
        "category": "food-delivery",
        "affiliate_network": "line",
        "scraper_config": {"type": "javascript"}
    },
]

def seed_stores():
    """
    Seeds the database with 100+ stores across America, Europe, and Asia
    """
    db = SessionLocal()
    
    try:
        # Combine all stores
        all_stores = (
            AMERICA_RETAIL_STORES + 
            AMERICA_FOOD_DELIVERY + 
            EUROPE_RETAIL_STORES + 
            EUROPE_FOOD_DELIVERY + 
            ASIA_RETAIL_STORES + 
            ASIA_FOOD_DELIVERY
        )
        
        print(f"Seeding {len(all_stores)} stores...")
        
        for store_data in all_stores:
            # Check if store already exists
            existing = db.query(Store).filter(Store.slug == store_data['slug']).first()
            
            if existing:
                print(f"Store '{store_data['name']}' already exists, skipping...")
                continue
            
            # Convert scraper_config to JSON string for SQLite
            if 'scraper_config' in store_data and isinstance(store_data['scraper_config'], dict):
                store_data['scraper_config'] = json.dumps(store_data['scraper_config'])
            
            # Create new store
            store = Store(**store_data)
            db.add(store)
            print(f"Added: {store_data['name']} ({store_data['region']} - {store_data['country']})")
        
        db.commit()
        
        # Print summary
        total = db.query(Store).count()
        america_count = db.query(Store).filter(Store.region == 'america').count()
        europe_count = db.query(Store).filter(Store.region == 'europe').count()
        asia_count = db.query(Store).filter(Store.region == 'asia').count()
        food_delivery_count = db.query(Store).filter(Store.store_type == 'food_delivery').count()
        
        print("\n" + "="*60)
        print("STORE DATABASE SEEDING COMPLETE!")
        print("="*60)
        print(f"Total stores: {total}")
        print(f"America: {america_count}")
        print(f"Europe: {europe_count}")
        print(f"Asia: {asia_count}")
        print(f"Food Delivery: {food_delivery_count}")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"Error seeding stores: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting store database seeding...")
    seed_stores()
