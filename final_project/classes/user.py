from final_project.models import User
from abc import ABC, abstractmethod
class UserAccount():
    @abstractmethod
    def __getPublicInfo__(self):
        pass

    @abstractmethod
    def __editContactInfo__(self):
      pass

    @abstractmethod
    def __sendNotification__(self):
       pass