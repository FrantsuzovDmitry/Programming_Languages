import time
from queue import Queue
from threading import Thread

import requests
from bs4 import BeautifulSoup
from Parser import Parser

delay_in_seconds = 5 * 60  # every 5 minutes


def parse_and_put(parser, result_queue):
  while True:
    parser.ParseNews(result_queue)
    time.sleep(delay_in_seconds)


if __name__ == "__main__":
  result_queue = Queue()

  # Books news: https://readrate.com/rus/news
  params1 = {
      "url": 'https://readrate.com/rus/news',
      "news_tagName": "div",
      "news_className": 'container news-post',
      "title_tagName": "h5",
      "title_className": 'news-post-title',
      "description_tagName": "div",
      "description_className": 'subtitle d-none d-sm-block',
      "third_entity_tagName": "a",
      "third_entity_className":
      "category text-yellow text-decoration-underline",
      "third_entity_semanticName": 'Category'
  }

  # Polish news: https://www.gazetapolska.pl/
  params2 = {
      "url": 'https://www.gazetapolska.pl/',
      "news_tagName": "div",
      "news_className": 'boxshadowlarge',
      "title_tagName": "h2",
      "title_className": 'post-title',
      "description_tagName": "div",
      "description_className": 'post-body',
      "third_entity_tagName": "div",
      "third_entity_className": 'post-autor',
      "third_entity_semanticName": 'Author'
  }

  # Litres new books and audiobooks: https://www.litres.ru/new/
  params3 = {
      "url": 'https://www.litres.ru/new/',
      "news_tagName": "div",
      "news_className": 'ArtInfo-modules__wrapper_1qQAy',
      "title_tagName": 'p',
      "title_className": 'ArtInfo-modules__title_MkOVH',
      "description_tagName": "a",
      "description_className": 'ArtInfo-modules__author_Mai7W',
      "third_entity_tagName": "a",
      "third_entity_className": 'ArtInfo-modules__reader_6dqHK',
      "third_entity_semanticName": 'Third entity'
  }

  parser1 = Parser(**params1)
  parser2 = Parser(**params2)
  parser3 = Parser(**params3)

  t1 = Thread(target=parse_and_put, args=(parser1, result_queue))
  t1.start()

  t2 = Thread(target=parse_and_put, args=(parser2, result_queue))
  t2.start()

  t3 = Thread(target=parse_and_put, args=(parser3, result_queue))
  t3.start()

  while True:
    try:
      while not result_queue.empty():
        item = result_queue.get()
        print("Title:", item[0])
        print("Description:", item[1])
        print(item[2])
        print("------------------------")
    except KeyboardInterrupt:
      t1.join()
      t2.join()
      t3.join()
      print("Программа завершена.")
