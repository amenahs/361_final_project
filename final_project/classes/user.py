from final_project.models import User, TA, AccountType
from abc import ABC, abstractmethod
class UserAccount():
    @abstractmethod
    def __getPublicInfo__(self):
        pass

    def __editContactInfo__(self, userEmail, name, email, password, phoneNum, address, skills):
        if not userEmail or not name or not email or not password or not address:
            raise TypeError("Invalid input")

        try:
            u = User.objects.get(email=userEmail)
            changesMade = False

            if u.name != name:
                u.name = name
                changesMade = True
            if u.email != email:
                u.email = email
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

            if u.type==AccountType.TA:
                ta = TA.objects.get(email=userEmail)
                ta.save()
                if skills and ta.skills != skills:
                    ta.skills = skills
                    changesMade = True
                    ta.save()

            u.save()
            return changesMade
        except:
           raise ValueError("User does not exist")

    @abstractmethod
    def __sendNotification__(self):
       pass