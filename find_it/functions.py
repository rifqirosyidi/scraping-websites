from lxml import html
from requests import ConnectionError
import requests


def handle_uqshop(target_url, header_url):
    try:
        page = requests.get(target_url, headers=header_url)
    except ConnectionError as err:
        print(err)

    tree = html.fromstring(page.content)

    title = tree.xpath('//h2[@class="woocommerce-loop-product__title"]/text()')
    price = tree.xpath('//span[@class="price"]/ins/span/text()')
    image = tree.xpath('//div[@class="product-image-box"]/a/img/@src')
    location = []
    link = tree.xpath('//a[@class="product-detail-link"]/@href')
    source = []


    for i in range(len(title)):
        location.append("Malang, Jawa Timur")
        source.append('uqshop')

    return zip(title, price, image, location, link, source)


def handle_olx(target_url, header_url):
    try:
        page = requests.get(target_url, headers=header_url)
    except ConnectionError as err:
        print(err)

    tree = html.fromstring(page.content)

    title = tree.xpath('//span[@class="_2tW1I"]/text()')
    price = tree.xpath('//span[@class="_89yzn"]/text()')
    image = tree.xpath('//figure[@class="_2grx4"]//img//@src')
    location = tree.xpath('//div[@class="_1KOFM"]/span[@class="tjgMj"]/text()')
    raw_link = tree.xpath('//span[@class="_2tW1I"]/ancestor::a/@href')

    site = 'https://www.olx.co.id'
    link = [site+list_item for list_item in raw_link]

    source = []
    for i in range(len(title)):
        source.append('olx')

    return zip(title, price, image, location, link, source)


def handle_elevenia(target_url, header_url):
    try:
        page = requests.get(target_url, headers=header_url)
    except ConnectionError as err:
        print(err)

    tree = html.fromstring(page.content)

    title = tree.xpath('//a[@class="pordLink notranslate"]/text()')
    price = tree.xpath('//div[@class="prc"]/strong/text()')
    image = tree.xpath('//div[@class="group"]/a/img/@src')
    location = tree.xpath('//ul[@class="sellerPlace"]/li/text()')
    link = tree.xpath('//a[@class="pordLink notranslate"]/@href')
    source = []

    for i in range(len(title)):
        source.append('elevenia')

    return zip(title, price, image, location, link, source)


def handle_sorabel(target_url, header_url):
    try:
        page = requests.get(target_url, headers=header_url)
    except ConnectionError as err:
        print(err)

    tree = html.fromstring(page.content)

    title = tree.xpath('//div[@data-qa-id="qa_common_card"]/div[@data-qa-id="qa_product_info"]/div/a/span/text()')
    price = tree.xpath('//div[@data-qa-id="qa_common_card"]/div[@data-qa-id="qa_product_info"]/div/a[2]/div/text()')
    image = tree.xpath('//div[@data-qa-id="qa_common_card"]/a/div/div/img/@src')
    location = []
    raw_link = tree.xpath('//div[@data-qa-id="qa_common_card"]/a/@href')
    source = []

    site = 'https://www.sorabel.com'
    link = [site + list_item for list_item in raw_link]

    for i in range(len(title)):
        location.append('Indonesia')
        source.append('sorabel')

    return zip(title, price, image, location, link, source)