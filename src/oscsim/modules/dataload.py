from abc import ABC, abstractmethod, abstractproperty
from threading import Lock
import random

class DataItem(ABC):
  """
  Abstract representation of feedable datarow.
  """

  itemname: str
  itemtype: str

  def getnameforitem(self) -> str:
    return self.itemname

  @abstractmethod
  def getdictionaryforitem(self) -> dict:
      """
      Build dictionary for data item consisting of Name, Type and Value.

      :return: Dict.
      """
      pass


class BaseNumberItem(DataItem):
  minvalue = None
  maxvalue = None

  def __init__(self, data:[str]):
    self.itemname = data[0]
    self.itemtype = "Number"
    if data[1] == "i" or data[1] == "lc":
      f = int(data[2])
      self.minvalue = f
      if len(data) > 3:
        self.maxvalue = int(data[3])

  @abstractmethod
  def getdictionaryforitem(self) -> dict:
      """
      Build dictionary for data item consisting of Name, Type and Value.

      :return: Dict.
      """
      pass


class LCIntegerNumberItem(BaseNumberItem):

  itemvalue = 0
  lock = None

  def __init__(self, data:[str], lock: Lock = None):
    super(LCIntegerNumberItem, self).__init__(data)
    self.lock = lock
    with lock:
      self.itemvalue = self.minvalue
    if self.maxvalue is None:
      self.maxvalue = 1000000000 # Unlimited magic number    

  def getdictionaryforitem(self) -> dict:
    attr = {}
    attr["type"] = self.itemtype
    with self.lock:
      attr["value"] = self.itemvalue
      if self.itemvalue < self.maxvalue:
        self.itemvalue += 1
    return attr


class RandomIntegerNumberItem(BaseNumberItem):

  def __init__(self, data:[str]):
    super(RandomIntegerNumberItem, self).__init__(data)

  def getdictionaryforitem(self) -> dict:
    value = self.minvalue
    if self.maxvalue is not None:
        value = random.randint(self.minvalue, self.maxvalue)

    itemdict = dict()
    itemdict["type"] = self.itemtype
    itemdict["value"] = value
    return itemdict


class RandomFloatNumberItem(BaseNumberItem):

  def __init__(self, data:[str]):
    super(RandomFloatNumberItem, self).__init__(data)
    self.minvalue = float(data[2])
    if len(data) > 3:
        self.maxvalue = float(data[3])

  def getdictionaryforitem(self) -> dict:
    value = self.minvalue
    if self.maxvalue is not None:
      value = round(random.uniform(self.minvalue, self.maxvalue), 1)
    itemdict = dict()
    itemdict["type"] = self.itemtype
    itemdict["value"] = value
    return itemdict
