from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "potent-retina-350101",
  "private_key_id": "e29217becec58f76d21417628b6f3f4c09228509",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDhTdfAoKYCa54j\nqtWJ2qGX8dK/fxET+ufSLKDdanD49eZG17KSi85ykQYBpnawkIJyWL9LNsWGuyzQ\nvQj50T6cBNOL6f13tBKujIDFM/kwlASJSz0Pvj/aIkzGaxhUrPrBSnvmHwZGH1BX\n+bmP0btq8PgrJsojoI22A+PZh5qrwNC7qUt0TtOuZiR1th71fWyKho59Ueb2GRXX\nVphu3Mycb3TQ1JIthttnseQWUliiLHwp+0lDTVlkMD7+kZdletk6XD+J3f41ns20\noLgonk83Xt2tq9J3HpzbXqxdVc/iTGOsr48vp6/FFZ9XHBOQktABbdZvIYVzRo0X\npCdyFQVFAgMBAAECggEAE88+llT5q7JPJfcuDdAfj6bHPyeato1Dxz69ySID+1vR\niq6J6KkqtneKVehPPMCD+65SaXhQH0PDUbohOSfc76Zb/EwPSXBXiSnY453pfcwx\n5ulq3cC+R/1mjzaY3c8UwBx+rtHRASbdL1MJbfwElMdJpq+jK8VA2H1YkgaCgrHH\n2GC+B3uQYcK6/m0jDGgC43Z+LRP27v7e3PuG1a1nPHJ9WppSMmmEzNJSeR87j7sg\neonJLxPgVobeCc7dhmG+NjuMAWll3Yn5Gczg3GpypfxsjqYL+tDlR2Yq7/CDRfci\nO2LzASISaxKZJDu/nAGGUN6+d/Mh3ZVl16xF9Xbi+QKBgQD3T+RNOOG7B3hAt6X5\nAf+Sh/Rb4Uz/AZGTBLHpXBg0/O72rdQc+gtYi/5GPK/X0WtvX3XxF3+IbU5hvz8R\nYSKD1mgWXTfiUn08oPSCxCArqgPpbXnBPATiS5pUxH8Cu5uB5oZhwwKZ+04YM64P\naS7OUbVjI9dpL/oauVuZGdPp3QKBgQDpOAe/uW2oW/nLvq3jQ5/TQh5CT6/qojnK\nx24rOhNJoHgjXjn3aur6/CwiWz3eIAPH/+CN8e9cyrZvEky+ihpl5WzNmdUtoKc1\nUqB2J3gxo3RdTnaRdBsilewn92eDXqxXcw1LDbkWDF/4TTq7bTDVoWmOFgzdYLsh\nB77TgdV2iQKBgGwRrzPHbWxrATNWjOJY6zM+0ZrswtaT+ucBoDTXF4TgGhQVNaFL\n6nVRB1Xt4vEuBAJw9nrZx9L34M554bdYeNqfcHCFX4w4e51owC/8QAqUio0QV6oG\n7iNs4g20p8Or83I6J/LEYnijBicxPhhh4CAsOFUQLms6mdHfuZUXYjDJAoGAUyHO\n2U++v/GxNChPEaCsWwDJinefTHLxSNAX/D6iW29hA7J11TT+d+Ll1IVTo1ckIema\n4N4ppZj4uNT8GDtgN4w1YYCBVddbYw2F9zgQhxktxIjQiP6rIYPxfzmYY2Ke6jkv\ntt44aJyWpQraca71ZmE4IBbKFSuC6L47DmfMcIkCgYBmMq9conLnPpraGFdQEGxT\np84c5td0wmK+vwH7y7B4QCx1q+ylEDR2s8v6fbU1B0jZbfBDMDkDHktXcBonbAL6\nh2EJ0lZd2sojMUKE8qEwhXDg77TV1O4rEefTjUgtfVlwCjmseY6guXtetbljuXzw\noazjbu0jiSqqGgGKz6Co8Q==\n-----END PRIVATE KEY-----\n",
  "client_email": "544961028275-compute@developer.gserviceaccount.com",
  "client_id": "107025073637383838535",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/544961028275-compute%40developer.gserviceaccount.com"
  
}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('bucket-atv-4')
  blob = bucket.blob('bucket-atv-4.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
