import requests
from lxml import html


def handle_elevenia_flashsale(target_url, header_url):
    try:
        page = requests.get(target_url, headers=header_url)
    except ConnectionError as err:
        print(err)

    tree = html.fromstring(page.content)

    title = tree.xpath('//div[@class="prdTitle"]/p[@class="link notranslate"]/a/text()')
    discount = tree.xpath('//span[@class="txtDisc notranslate"]/b/text() | //span[@class="txtDisc notranslate"][not(b)]/text()')
    price_before = tree.xpath('//p[@class="price notranslate"]/del/text()')
    price = tree.xpath('//p[@class="price notranslate"]/text()[2]')
    image = tree.xpath('(//img[@class="dailyDealsLazy"])[position()>1]/@data-original')
    source = []

    for i in range(len(title)):
        source.append('elevenia')

    return zip(title, discount, price_before, price, image, source)
