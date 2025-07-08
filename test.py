# import shutil
# import requests

# url = 'https://barcodeapi.org/api/auto/345234'
# response = requests.get(url, stream=True)
# with open('test.png', 'wb') as out_file:
#     shutil.copyfileobj(response.raw, out_file)
barcode = 100000


def create_barcode_num():
    global barcode
    barcode += 1
    yield 


create_barcode_num()
create_barcode_num()
create_barcode_num()
print(barcode)