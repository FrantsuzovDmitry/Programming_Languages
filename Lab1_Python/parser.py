import requests
import time
from queue import Queue
from bs4 import BeautifulSoup


class Parser:

  def __init__(self, url, news_tagName, news_className, title_tagName,
               title_className, description_tagName, description_className,
               third_entity_tagName, third_entity_className, third_entity_semanticName):
    self.url = url
    self.news_tagName = news_tagName
    self.news_className = news_className
    self.title_tagName = title_tagName
    self.title_className = title_className
    self.description_tagName = description_tagName
    self.description_className = description_className
    self.third_entity_tagName = third_entity_tagName
    self.third_entity_className = third_entity_className
    self.third_entity_semanticName = third_entity_semanticName
    self.parsed_titles = {}  # Словарь для хранения уже выведенных новостей

  def ParseNews(self, result_queue):
    response = requests.get(self.url).text
    soup = BeautifulSoup(response, features="html.parser")

    for news in soup.find_all(self.news_tagName, class_=self.news_className):
      title_element = news.find(self.title_tagName,
                        class_=self.title_className)
      if title_element:
        title = title_element.text.strip()
      else:
        break

      # Проверяем, есть ли уже такой заголовок в словаре
      if title not in self.parsed_titles:
          self.parsed_titles[title] = True
      else:
          continue 

      description_element = news.find(self.description_tagName,
                                      class_=self.description_className)
      if description_element:
        description = description_element.text.strip()
      else:
        description = 'None'
        
      third_entity_element = news.find(self.third_entity_tagName,
                                       class_=self.third_entity_className)
      if third_entity_element:
        third_entity = third_entity_element.text.strip()
      else:
        third_entity = 'None'
        
      result_queue.put((title, description, self.third_entity_semanticName + ": " + third_entity))
