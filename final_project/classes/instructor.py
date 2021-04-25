from final_project.models import Instructor
from abc import ABC, abstractmethod

class Instructor():
    @abstractmethod
    def __viewTAs__(self):
        pass