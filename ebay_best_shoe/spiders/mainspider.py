from os import name
import scrapy
from scrapy import *
from ebay_best_shoe.items import EbayBestShoeItem
from scrapy.loader import ItemLoader



headers = {
    'authority': 'www.ebay.com',
    'user-agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    'accept': '*/*',
    'sec-gpc': '1',
    'origin': 'https://www.ebay.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.ebay.com/b/Mens-Shoes/93427?mag=1&Brand=New%2520Balance&_udlo=0&_fsrp=0&rt=nc&_sacat=93427&Features=Lightweight%7CComfort%7CPerformance&US%2520Shoe%2520Size=11&_udhi=150&LH_ItemCondition=1000%7C1500',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'ak_bmsc=C23C7EFBDA260E269B9F6417711C3660~000000000000000000000000000000~YAAQXKAnF+5+DQ1/AQAA8toADw4h3HccwzZeNXroBCwRl/Sle/rOjMG8BrYt/e14U30ETIMiE5qnoTfPF3N7jFJbwzLx8YacziHh4l0aKgEYigQau63GT/4ApBr+ojuWWVi7qTrTsQ8OHii5aSMWgkFLYztbOgjUzr0mnYgZlHV63thvGH9GjFIX/0dd+XRL/2Tbn1SGLsP7dBPL+VfcvsvSt8vplVIdWd6FYcva/KPRWEo+Yu0t4ZT6SLIx3Pe7Vco2MFVml4SaOaS4YMjTqSmcTAhcfePNJ+OP0eSoQx69sPOkCblLjpN463AELIeUdsqarh4L0eutEt8WgGnE7sjwu3BAvQW29gxQ/QhIlUsamWPyyZd2diKS2A4QlZKvKU/62kMTCLgp; AMCVS_A71B5B5B54F607AB0A4C98A2%40AdobeOrg=1; AMCV_A71B5B5B54F607AB0A4C98A2%40AdobeOrg=-408604571%7CMCMID%7C72510726309907582485226049060912584157%7CMCOPTOUT-1645231766s%7CNONE%7CvVersion%7C4.6.0; s=CgAD4ACBiEXSNMGYwMGRhNzMxN2YwYWI4NWJiYTA5ZThkZmZmOWU2NjAirq8f; ebay=%5Ejs%3D1%5Esbf%3D%23000000%5E; bm_sv=8F5FA769634FC3739903F9D303FA8A82~1LNenoiN3roq5J2KbDExlbyNWGORnWQkiH/f4SWtDFMVjlRNji84D0xS/onhwKRcqWejKnm053T184GTFO50DC+SsNmD9PmBatMQmwXP0boc6QSBminV0IvPHnFgZziU+QE2vg7oC1opnD6KBog9F/caLT2GYiS98T1TGqyEfuo=; dp1=bu1p/QEBfX0BAX19AQA**65d28d7a^pbf/%23e000e0000000000000000063f159fa^bl/EG65d28d7a^; nonsession=BAQAAAX42/BiUAAaAADMABWPxWfoxMjYxMQDKACBl0o16MGYwMGRhNzMxN2YwYWI4NWJiYTA5ZThkZmZmOWU2NjAAywACYhAtgjU1nRZ7Z5OdaYbHYcRwFvlCjAcBx54*; npii=btguid/0f00da7317f0ab85bba09e8dfff9e66065d28d7a^cguid/0f01012d17f0adb933948ae4fd60015f65d28d7a^',
}

class MainspiderSpider(scrapy.Spider):
    name = 'mainspider'

    def start_requests(self):
        yield scrapy.Request('https://www.ebay.com/b/Mens-Shoes/93427?mag=1&Brand=New%2520Balance&_udlo=0&_fsrp=0&rt=nc&_sacat=93427&Features=Lightweight%7CComfort%7CPerformance&US%2520Shoe%2520Size=11&_udhi=150&LH_ItemCondition=1000%7C1500'
        ,headers = headers , meta={"playwright": True})


    def parse(self, response):
        for item in response.css('.s-item--bgcolored'):
            l = ItemLoader(item=EbayBestShoeItem(), response=response)
            if item.css('.s-item__logisticsCost::text').get() != 'Free shipping' and item.css('.s-item__logisticsCost::text').get() != None: #if it's dont have a free shipping
                shipping_price = item.css('.s-item__logisticsCost::text').get().replace(' shipping' , '').replace('$','')
                total_price = f"{float(item.css('.s-item__price::text').get().replace('$',''))+float(item.css('.s-item__logisticsCost::text').get().replace('$','').replace(' shipping' , ''))}"
            if item.css('.s-item__logisticsCost::text').get() == 'Free shipping': #if it's have a free shipping
                shipping_price = 'Free shipping'
                total_price = item.css('.s-item__price::text').get().replace('$','')
            if item.css('.s-item__logisticsCost::text').get() == None: #if it's shipping price not labeled
                total_price = item.css('.s-item__price::text').get().replace('$','')
                shipping_price = 'undefined'
            
            l.add_value('name' , item.css('.s-item__title::text').get())
            l.add_value('price' , item.css('.s-item__price::text').get().replace('$',''))
            l.add_value('shipping_price' , shipping_price)
            l.add_value('total_price' , total_price)
            l.add_value('product_link' , item.css('.s-item__info a.s-item__link::attr(href)').get())
            
            yield l.load_item()

        if response.css('.pagination__next::attr(href)').get() is not None:
            yield FormRequest(response.css('.pagination__next::attr(href)').get() , callback=self.parse )