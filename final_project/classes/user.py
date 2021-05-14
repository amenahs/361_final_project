from final_project.models import User, TA, AccountType
from abc import ABC, abstractmethod
class UserAccount():
    @abstractmethod
    def __getPublicInfo__(self):
        pass

    def __editContactInfo__(self, userEmail, name, password, phoneNum, address, skills):
        if not userEmail or not name or not password or not address:
            raise TypeError("Invalid input")

        try:
            u = User.objects.get(email=userEmail)
            changesMade = False

            if u.name != name:
                u.name = name
                changesMade = True
            if u.password != password:
                u.password = password
                changesMade = True
            if u.phoneNumber != phoneNum:
                u.phoneNumber = phoneNum
                changesMade = True
            if u.homeAddress != address:
                u.homeAddress = address
                changesMade = True
            if skills and u.skills != skills:
                if u.skills:
                    u.skills = u.skills + ", " + skills
                else:
                    u.skills = u.skills + skills
                changesMade = True

            u.save()
            return changesMade
        except:
           raise ValueError("User does not exist")

    @abstractmethod
    def __sendNotification__(self):
       pass