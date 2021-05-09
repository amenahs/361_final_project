from abc import ABC, abstractmethod

class Assign():
    @abstractmethod
    def __assignProfessorLecture__(self, profEmail, lecID):
         pass

    @abstractmethod
    def __assignTALecture__(self, taEmail, lecID):
         pass

    @abstractmethod
    def __assignTASection__(self, taEmail, secID):
        pass