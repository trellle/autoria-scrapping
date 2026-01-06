import scrapy
from scrapy.http.response import Response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Browser():
    def __init__(self):
        self.driver = self.init_driver()
    
    def init_driver(self):
        try:
            return webdriver.Firefox()
        except WebDriverException:
            return webdriver.Chrome()
    
    def __del__(self):
        self.driver.quit()


class AutoriaSpider(scrapy.Spider):
    name = "autoria"
    allowed_domains = ["auto.ria.com"]
    start_urls = ["https://auto.ria.com/uk/car/used/"]

    @staticmethod
    def split_str(raw_str: str, splitter: str) -> list[str]:
        if raw_str:
            return raw_str.split(splitter)
    
    def parse_number(self, link: str):
        browser = Browser()
        browser.driver.get(link)
        wait = WebDriverWait(browser.driver, 15)
        try:
            consent_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "fc-cta-do-not-consent")))
        except WebDriverException:
            consent_button = None
        if consent_button:
            consent_button.click()
        button = browser.driver.find_element(By.CLASS_NAME, "conversion")
        button.click()
        return wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".popup-body .conversion .common-text"))).text
    
    def parse_detail_page(self, response: Response):
        title_elems = response.css("#sideTitleTitle .common-text::text").get()
        if title_elems:
            title_elems = self.split_str(title_elems, " ")
            year = title_elems.pop()
        else:
            return
        mileage = response.css("#basicInfoTableMainInfo0 .common-text::text").get()
        car_number = response.css("#badges .car-number::text").get()
        params = self.split_str(response.css("#descCharacteristicsValue .common-text::text").get(), " •\xa0\xa0")
        description = response.css(".expandable-text-template span::text").get()
        engine = self.split_str(response.css("#descEngineEngine .common-text::text").get(), ", ")
        fuel_spend = self.split_str(response.css("#descFuelRateValue .common-text::text").get(), " •\xa0\xa0")
        data = {
            "url": response.meta["details_url"],
            "model": " ".join(title_elems),
            "year": int(year),
            "price_USD": int(response.css("#sidePrice .titleL::text").get().translate(str.maketrans("", "", "\xa0$"))),
            "price_UAH": int(response.css("#sidePrice .body::text").get().translate(str.maketrans("", "", "\xa0грн"))),
            "color": response.css("#descColorColor .common-text::text").get(),
            "odometer": 0 if mileage == "Без пробігу" else int(mileage.split(" ")[0]) * 1000,
            "gearbox": response.css("#basicInfoTableMainInfo1 .common-text::text").get(),
            "fuel": engine[0] if engine else None,
            "city_spend": float(fuel_spend[0].split(" ")[1]) if fuel_spend else None,
            "road_spend": float(fuel_spend[1].split(" ")[1]) if fuel_spend and len(fuel_spend) > 1 and "траса" in fuel_spend[1] else None,
            "mix_spend": float(fuel_spend[-1].split(" ")[1]) if fuel_spend and len(fuel_spend) > 2 and "змішаний" else None,
            "eco-standart": response.css("#descEcoStandartEcoStandart .common-text::text").get(),
            "engine_volume": float(engine[1].split(" ")[0]) if engine and len(engine) > 1 and "л" in engine[1] else None,
            "horse_power": float(engine[-1].split(" ")[0].lstrip("(")) if engine and len(engine) >= 2 and "(" in engine[-1] else None,
            "watt_power": float(engine[-1].split(" ")[3]) if engine and len(engine) >= 2 and "(" in engine[-1] else None,
            "address": response.css("#basicInfoTableMainInfoGeo span::text").get(),
            "tags": response.css("#badges .badge-template span::text").getall(),
            "car_number": car_number if car_number else None,
            "win_code": response.css("#badgesVinGrid .common-text::text").get(),
            "description": description.translate(str.maketrans("\n\t", "  ", "")) if description else None,
            "body_type": params[0].strip(" ") if params else None,
            "doors": int(params[1].split(" ")[0]) if params and len(params) > 1 and "дверей" in params else None,
            "seats": int(params[-1].split(" ")[0]) if params and len(params) > 2 and "місць" in params else None,
            "generation": response.css("#descGenerationBaseValue .common-text::text").get(),
            "drive": response.css("#descDriveTypeDriveType .common-text::text").get(),
            "condition": response.css("#descStateValue .common-text::text").get(),
            "security": self.split_str(response.css("#descSecurityValue .common-text::text").get(), " •\xa0\xa0"),
            "features": self.split_str(response.css("#descComfortValue .common-text::text").get(), " •\xa0\xa0"),
            "headlights": response.css("#descHeadlightsValue .common-text::text").get(),
            "optics": self.split_str(response.css("#descOpticsValue .common-text::text").get(), " •\xa0\xa0"),
            "conditioner": response.css("#descConditionerValue .common-text::text").get(),
            "parktronic": self.split_str(response.css("#descParktronicValue .common-text::text").get(), " •\xa0\xa0"),
            "multimedia": self.split_str(response.css("#descMultimediaValue .common-text::text").get(), " •\xa0\xa0"),
            "steering_adjustment": response.css("#descSteeringWheelAdjustmentValue .common-text::text").get(),
            "power_steering": response.css("#descPowerSteeringValue .common-text::text").get(),
            "extra_wheel": response.css("#descSpareWheelValue .common-text::text").get(),
            "paint_rate": response.css("#descPaintConditionValue .common-text::text").get(),
            "interior": self.split_str(response.css("#descSalonValue .common-text::text").get(), " •\xa0\xa0"),
            "seats_adjustment": response.css("#descSeatAdjustmentValue .common-text::text").get(),
            "seats_memory": response.css("#descMemorySeatModuleValue .common-text::text").get(),
            "seats_heat": response.css("#descSeatsHeatedValue .common-text::text").get(),
            "interior_material": response.css("#descInteriorMaterialsValue .common-text::text").get(),
            "interior_color": response.css("#descInteriorColorsValue .common-text::text").get(),
            "airbags": self.split_str(response.css("#descAirbagValue .common-text::text").get(), " •\xa0\xa0"),
            "window_lifters": response.css("#descWindowLifterValue .common-text::text").get(),
            "other_equipment": self.split_str(response.css("#descOthersValue .common-text::text").get(), " •\xa0\xa0"),
            "username": response.css("#sellerInfoUserName .common-text::text").get(),
            "images_count": int(response.css(".common-badge.alpha span:nth-child(2)::text").get()),
            "image_urls": response.css("#photoSlider .picture img::attr(data-src)").getall()
        }
        data["phone_number"] = self.parse_number(response.meta["details_url"])
        yield data

    def parse(self, response: Response):
        
        for car in response.css(".ticket-item"):
            details_url = car.css(".ticket-title a::attr(href)").get()
            yield scrapy.Request(
                details_url,
                callback=self.parse_detail_page,
                meta={"details_url": details_url}
            )
        next_page = response.css(".next a::attr(href)").get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)
