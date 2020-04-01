from abc import ABC, abstractmethod

class FaceNotFoundException(Exception): pass

class FaceInterface(ABC):
  @abstractmethod
  def encode(self, image_info):
    return NotImplemented

  @abstractmethod
  def detect(self, image_info):
    return NotImplemented

  @abstractmethod
  def search(self, image_info):
    return NotImplemented
