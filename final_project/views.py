from django.shortcuts import render, redirect
from django.views import View
from .models import User, Administrator, Professor, TA, Course, Lecture, Section, AccountType, TASectionAllocation
from .classes.administrator import Admin
from .classes.user import UserAccount


# Create your views here.

class Home(View):
    def get(self, request):
        request.session.pop("email", None)
        return render(request, "home.html", {})

    def post(self, request):
        noSuchUser = False
        badPassword = False
        try:
            m = User.objects.get(email=request.POST['email'])
            badPassword = (m.password != request.POST['password'])
        except:
            noSuchUser = True
        if noSuchUser or badPassword:
            return render(request, "home.html", {"message": "Email and password combination does not exist"})
        else:
            request.session["email"] = m.email
            return redirect("/dashboard/")


class Dashboard(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("/")

        u = User.objects.get(email=request.session["email"])
        username = u.name
        accountProfession = getProfession(u)
        isNotAdmin = accountProfession != "Administrator"
        courseHeader = "Assigned Courses"

        if not isNotAdmin:
            courses = Course.objects.all()
            courseHeader = "Active Courses"
        elif accountProfession == "Professor":
            courses = Course.objects.filter(lecture__profID__email=u.email).distinct()
        else:
            courses = Course.objects.filter(lecture__taID__email=u.email).distinct()

        formattedCourses = []
        for c in courses:
            formattedCourses.append((c.courseID, c.name, c.numLectures, c.numSections))

        formattedAdmins = []
        admins = Administrator.objects.all()
        for a in admins:
            formattedAdmins.append((a.name, "Administrator", a.email, a.phoneNumber))

        admins = Professor.objects.all()
        for p in admins:
            formattedAdmins.append((p.name, "Professor", p.email, p.phoneNumber))

        admins = TA.objects.all()
        for t in admins:
            formattedAdmins.append((t.name, "Teaching Assistant", t.email, t.phoneNumber))

        taAssignments = []
        if isNotAdmin:
            tas = TA.objects.all()
            for t in tas:
                assignedCourses = Course.objects.filter(lecture__taID__email=t.email).distinct()
                for c in assignedCourses:
                    numAllocations = 0
                    allocations = TASectionAllocation.objects.filter(ta=t, lec__course__courseID=c.courseID).distinct()
                    for a in allocations:
                        numAllocations += a.numSections
                    taAssignments.append((t.name, c.courseID, c.name, numAllocations))

        return render(request, "dashboard.html",
                      {"courses": formattedCourses, "admins": formattedAdmins, 'username': username,
                       'isNotAdmin': isNotAdmin, 'courseHeader': courseHeader,
                       'taAssignments': taAssignments})


class Error(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("/")
        return render(request, "error-page.html")


class CreateAccount(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("/")

        u = User.objects.get(email=request.session["email"])
        isAdmin = u.type == AccountType.Administrator
        if not isAdmin:
            return redirect("/error-page/")

        admins = Administrator.objects.all()
        formattedAdmins = []
        for a in admins:
            formattedAdmins.append((a.email, a.name, a.phoneNumber, a.homeAddress))

        prof = Professor.objects.all()
        formattedProf = []
        for p in prof:
            formattedProf.append((p.email, p.name, p.phoneNumber, p.homeAddress))

        tas = TA.objects.all()
        formattedTA = []
        for t in tas:
            formattedTA.append((t.email, t.name, t.phoneNumber, t.homeAddress))

        return render(request, "create-account.html", {"admins": formattedAdmins, "prof": formattedProf,
                                                       "tas": formattedTA})

    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        type = request.POST['type']
        phoneNum = request.POST['number']
        address = request.POST['address']

        admins = Administrator.objects.all()
        formattedAdmins = []
        for a in admins:
            formattedAdmins.append((a.email, a.name, a.phoneNumber, a.homeAddress))

        prof = Professor.objects.all()
        formattedProf = []
        for p in prof:
            formattedProf.append((p.email, p.name, p.phoneNumber, p.homeAddress))

        tas = TA.objects.all()
        formattedTA = []
        for t in tas:
            formattedTA.append((t.email, t.name, t.phoneNumber, t.homeAddress))

        try:
            a = Admin()
            a.__createAccount__(name, email, password, type, phoneNum, address)
        except ValueError:
            return render(request, "create-account.html", {"admins": formattedAdmins, "prof": formattedProf,
                                                           "tas": formattedTA, "message": "Account already exists"})
        except TypeError:
            return render(request, "create-account.html", {"admins": formattedAdmins, "prof": formattedProf,
                                                           "tas": formattedTA, "message": "Invalid input"})
        else:
            return redirect("/create-account/")


class CreateCourse(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("/")

        u = User.objects.get(email=request.session["email"])
        isAdmin = u.type == AccountType.Administrator
        if not isAdmin:
            return redirect("/error-page/")

        courses = Course.objects.all()
        formattedCourses = []
        for c in courses:
            formattedCourses.append((c.courseID, c.name))
        lectures = Lecture.objects.all()
        formattedLectures = []
        for l in lectures:
            formattedLectures.append((l.course.courseID, l.lectureID))
        sections = Section.objects.all()
        formattedSections = []
        for s in sections:
            formattedSections.append((s.course.courseID, s.sectionID))

        return render(request, "create-course.html",
                      {"courses": formattedCourses, "lectures": formattedLectures, "sections": formattedSections})

    def post(self, request):
        newCourseID = request.POST['courseID']
        newCourseName = request.POST['name']
        lectureNum = request.POST['lectureNum']
        sectionNum = request.POST['sectionNum']

        courses = Course.objects.all()
        formattedCourses = []
        for c in courses:
            formattedCourses.append((c.courseID, c.name))
        lectures = Lecture.objects.all()
        formattedLectures = []
        for l in lectures:
            formattedLectures.append((l.course.courseID, l.lectureID))
        sections = Section.objects.all()
        formattedSections = []
        for s in sections:
            formattedSections.append((s.course.courseID, s.sectionID))

        try:
            a = Admin()
            a.__createCourse__(newCourseID, newCourseName, lectureNum, sectionNum)
        except ValueError:
            return render(request, "create-course.html",
                          {"courses": formattedCourses, "lectures": formattedLectures, "sections": formattedSections,
                           "message": "Course already exists"})
        except TypeError:
            return render(request, "create-course.html",
                          {"courses": formattedCourses, "lectures": formattedLectures, "sections": formattedSections,
                           "message": "Invalid input"})
        else:
            return redirect("/create-course/")


class EditInformation(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("/")
        u = User.objects.get(email=request.session["email"])
        isTA = False

        accountProfession = getProfession(u)

        if u.type == AccountType.TA:
            isTA = True
            ta = TA.objects.get(email=u.email)
            return render(request, "edit-information.html", {"accountName": u.name, "accountEmail": u.email,
                                                             "accountProfession": accountProfession,
                                                             "accountPassword": u.password,
                                                             "accountPhoneNumber": u.phoneNumber,
                                                             "accountAddress": u.homeAddress,
                                                             "accountSkills": ta.skills,
                                                             "TA": isTA})

        return returnnomessage(request, "edit-information.html", u, accountProfession, isTA)

    def post(self, request):
        name = request.POST['name']
        password = request.POST['password']
        phoneNum = int(request.POST['number'])
        address = request.POST['address']
        u = User.objects.get(email=request.session["email"])

        isTA = False
        taSkills = ''
        if u.type == AccountType.TA:
            isTA = True
        # taSkills = request.POST['skills']

        accountProfession = getProfession(u)

        try:
            account = UserAccount()
            changesMade = account.__editContactInfo__(u.email, name, password, phoneNum, address, taSkills)
            message = 'No changes made'
            if changesMade:
                message = 'Information updated'
                u = User.objects.get(email=request.session["email"])

            if isTA:
                ta = TA.objects.get(email=u.email)
                return render(request, "view-information.html", {"accountName": u.name,
                                                                 "accountEmail": u.email,
                                                                 "accountProfession": accountProfession,
                                                                 "accountPassword": u.password,
                                                                 "accountPhoneNumber": u.phoneNumber,
                                                                 "accountAddress": u.homeAddress,
                                                                 "accountSkills": ta.skills,
                                                                 "message": message,
                                                                 "TA": isTA})

            return returnwmessage(request, "view-information.html", u, accountProfession, message, isTA)

        except TypeError:
            message = "Invalid input"
            return returnwmessage(request, "view-information.html", u, accountProfession, message, isTA)

        except ValueError:
            message = "Invalid email"
            return returnwmessage(request, "view-information.html", u, accountProfession, message, isTA)


class ViewInformation(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("/")
        u = User.objects.get(email=request.session["email"])
        isTA = False

        accountProfession = getProfession(u)

        if u.type == AccountType.TA:
            isTA = True
            ta = TA.objects.get(email=u.email)
            return render(request, "view-information.html", {"accountName": u.name, "accountEmail": u.email,
                                                             "accountProfession": accountProfession,
                                                             "accountPassword": u.password,
                                                             "accountPhoneNumber": u.phoneNumber,
                                                             "accountAddress": u.homeAddress,
                                                             "accountSkills": ta.skills,
                                                             "TA": isTA})

        return returnnomessage(request, "view-information.html", u, accountProfession, isTA)

    def post(self, request):

        u = User.objects.get(email=request.session["email"])

        isTA = False
        if u.type == AccountType.TA:
            isTA = True

        accountProfession = getProfession(u)

        try:
            account = UserAccount()
            message = 'No changes made'
            if isTA:
                ta = TA.objects.get(email=u.email)
                return render(request, "view-information.html", {"accountName": u.name,
                                                                 "accountEmail": u.email,
                                                                 "accountProfession": accountProfession,
                                                                 "accountPassword": u.password,
                                                                 "accountPhoneNumber": u.phoneNumber,
                                                                 "accountAddress": u.homeAddress,
                                                                 "accountSkills": ta.skills,
                                                                 "message": message,
                                                                 "TA": isTA})

            return returnwmessage(request, "view-information.html", u, accountProfession, message, isTA)

        except TypeError:
            message = "Invalid input"
            return returnwmessage(request, "view-information.html", u, accountProfession, message, isTA)
        except ValueError:
            message = "Invalid email"
            return returnwmessage(request, "view-information.html", u, accountProfession, message, isTA)


class AssignProfCourse(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("/")

        u = User.objects.get(email=request.session["email"])
        isAdmin = u.type == AccountType.Administrator
        if not isAdmin:
            return redirect("/error-page/")

        lectures = Lecture.objects.all()
        formattedLectures = []
        for l in lectures:
            formattedLectures.append((l.lectureID, l.course.courseID, l.course.name))

        prof = Professor.objects.all()
        formattedProf = []
        for p in prof:
            formattedProf.append((p.email, p.name))

        assignedLectures = []
        for p in prof:
            lecList = Lecture.objects.filter(profID=p)
            for l in lecList:
                assignedLectures.append((p.name, l.lectureID, l.course.courseID, l.course.name))

        return render(request, "assign-prof-course.html", {"lectures": formattedLectures, "profs": formattedProf,
                                                           "assignedLectures": assignedLectures})

    def post(self, request):
        profEmail = request.POST['prof']
        lecID = request.POST['lecture']

        lectures = Lecture.objects.all()
        formattedLectures = []
        for l in lectures:
            formattedLectures.append((l.lectureID, l.course.courseID, l.course.name))

        prof = Professor.objects.all()
        formattedProf = []
        for p in prof:
            formattedProf.append((p.email, p.name))

        assignedLectures = []
        for p in prof:
            lecList = Lecture.objects.filter(profID=p)
            for l in lecList:
                assignedLectures.append((p.name, l.lectureID, l.course.courseID, l.course.name))

        try:
            a = Admin()
            updatedAssignment = a.__assignProfessorLecture__(profEmail, lecID)

            if updatedAssignment:
                return redirect("/assign-prof-course/")

            return render(request, "assign-prof-course.html", {"lectures": formattedLectures, "profs": formattedProf,
                                                               "assignedLectures": assignedLectures,
                                                               "message": "Assignment already exists"})
        except TypeError:
            return render(request, "assign-prof-course.html", {"lectures": formattedLectures, "profs": formattedProf,
                                                               "assignedLectures": assignedLectures,
                                                               "message": "Invalid input"})
        except ValueError:
            return render(request, "assign-prof-course.html", {"lectures": formattedLectures, "profs": formattedProf,
                                                               "assignedLectures": assignedLectures,
                                                               "message": "Please select valid professor and lecture"})


class AssignTACourse(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("/")

        u = User.objects.get(email=request.session["email"])
        isAdmin = u.type == AccountType.Administrator
        if not isAdmin:
            return redirect("/error-page/")

        lectures = Lecture.objects.all()
        formattedLectures = []
        for l in lectures:
            formattedLectures.append((l.lectureID, l.course.courseID, l.course.name))

        tas = TA.objects.all()
        formattedTA = []
        for t in tas:
            formattedTA.append((t.email, t.name, t.skills))

        assignedLectures = []
        for t in tas:
            lecList = Lecture.objects.filter(taID=t)
            for l in lecList:
                allocation = TASectionAllocation.objects.filter(ta=t, lec=l)
                allocationNum = 0
                for al in allocation:
                    allocationNum += al.numSections
                assignedLectures.append((t.name, l.lectureID, l.course.courseID, l.course.name, allocationNum))

        return render(request, "assign-ta-course.html", {"lectures": formattedLectures, "tas": formattedTA,
                                                         "assignedLectures": assignedLectures})

    def post(self, request):
        taEmail = request.POST['ta']
        lecID = request.POST['lecture']

        lectures = Lecture.objects.all()
        formattedLectures = []
        for l in lectures:
            formattedLectures.append((l.lectureID, l.course.courseID, l.course.name))

        tas = TA.objects.all()
        formattedTA = []
        for t in tas:
            formattedTA.append((t.email, t.name, t.skills))

        assignedLectures = []
        for t in tas:
            lecList = Lecture.objects.filter(taID__in=[t])
            for l in lecList:
                allocation = TASectionAllocation.objects.filter(ta=t, lec=l)
                allocationNum = 0
                for al in allocation:
                    allocationNum += al.numSections
                assignedLectures.append((t.name, l.lectureID, l.course.courseID, l.course.name, allocationNum))

        try:
            a = Admin()
            updatedAssignment = a.__assignTALecture__(taEmail, lecID)

            if updatedAssignment:
                ta = TA.objects.get(email=taEmail)
                assignedTA = (ta.name, ta.email)

                lec = Lecture.objects.get(lectureID=lecID)
                assignedLecture = (lec.lectureID, lec.course.courseID, lec.course.name)

                sectionMax = lec.course.numSections

                return render(request, "allocate-sections.html", {'isAllocation': True,
                                                                  'assignedTA': assignedTA,
                                                                  'assignedLec': assignedLecture,
                                                                  'sectionMax': sectionMax})

            return render(request, "assign-ta-course.html", {"lectures": formattedLectures, "tas": formattedTA,
                                                             "assignedLectures": assignedLectures,
                                                             "message": "Assignment already exists"})
        except TypeError:
            return render(request, "assign-ta-course.html", {"lectures": formattedLectures, "tas": formattedTA,
                                                             "assignedLectures": assignedLectures,
                                                             "message": "Invalid input"})
        except ValueError:
            return render(request, "assign-ta-course.html", {"lectures": formattedLectures, "tas": formattedTA,
                                                             "assignedLectures": assignedLectures,
                                                             "message": "Please select valid TA and lecture"})


class AllocateSections(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("/")

        u = User.objects.get(email=request.session["email"])
        isAdmin = u.type == AccountType.Administrator
        if not isAdmin:
            return redirect("/error-page/")

        return render(request, "allocate-sections.html", {'isAllocation': False,
                                                          'message': 'Please assign a TA to a course first.'})

    def post(self, request):
        sectionNum = request.POST['sectionNum']
        taEmail = request.POST['taEmail']
        lecID = request.POST['lecID']

        message = ""
        try:
            a = Admin()
            isAllocated = a.__allocateSections__(taEmail, lecID, int(sectionNum))

            return redirect("/assign-ta-course/")

        except TypeError:
            message = "Invalid input"
            return render(request, "allocate-sections.html", {'isAllocation': False,
                                                              'message': message})
        except ValueError:
            message = "TA lecture assignment does not exist"
            return render(request, "allocate-sections.html", {'isAllocation': False,
                                                              'message': message})
        except SyntaxError:
            message = "Invalid number of sections selected"
            ta = TA.objects.get(email=taEmail)
            assignedTA = (ta.name, ta.email)

            lec = Lecture.objects.get(lectureID=lecID)
            assignedLecture = (lec.lectureID, lec.course.courseID, lec.course.name)

            sectionMax = lec.course.numSections

            return render(request, "allocate-sections.html", {'isAllocation': True,
                                                              'assignedTA': assignedTA,
                                                              'assignedLec': assignedLecture,
                                                              'sectionMax': sectionMax,
                                                              'message': message})


class AssignTASection(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("/")

        u = User.objects.get(email=request.session["email"])
        isAdmin = u.type == AccountType.Administrator
        if not isAdmin:
            return redirect("/error-page/")

        sections = Section.objects.all()
        formattedSections = []
        for s in sections:
            formattedSections.append((s.sectionID, s.course.courseID, s.course.name))

        tas = TA.objects.all()
        formattedTA = []
        for t in tas:
            formattedTA.append((t.email, t.name, t.skills))

        assignedSections = []
        for t in tas:
            secList = Section.objects.filter(taID=t)
            for s in secList:
                assignedSections.append((t.name, s.sectionID, s.course.courseID, s.course.name, ))

        return render(request, "assign-ta-section.html", {"sections": formattedSections, "tas": formattedTA,
                                                          "assignedSections": assignedSections})

    def post(self, request):
        taEmail = request.POST['ta']
        secID = request.POST['section']

        sections = Section.objects.all()
        formattedSections = []
        for s in sections:
            formattedSections.append((s.sectionID, s.course.courseID, s.course.name))

        tas = TA.objects.all()
        formattedTA = []
        for t in tas:
            formattedTA.append((t.email, t.name, t.skills))

        assignedSections = []
        for t in tas:
            secList = Section.objects.filter(taID=t)
            for s in secList:
                assignedSections.append((t.name, s.sectionID, s.course.courseID, s.course.name))

        try:
            a = Admin()
            updatedAssignment = a.__assignTASection__(taEmail, secID)

            if updatedAssignment:
                return redirect("/assign-ta-section/")
            else:
                message = "Assignment already exists"

        except TypeError:
            message = "Invalid input"
        except ValueError:
            message = "Please select valid TA and section"
        except SyntaxError:
            message = "TA has not been assigned to that course, or has already been assigned the maximum number of allocated sections"

        return render(request, "assign-ta-section.html", {"sections": formattedSections, "tas": formattedTA,
                                                          "assignedSections": assignedSections,
                                                          "message": message})


class EditAccount(View):
    def get(self, request):
        if not request.session.get("email"):
            return redirect("/")
        return render(request, "edit-account.html", {})


class ForgotPassword(View):
    def get(self, request):
        return render(request, "forgot-password.html", {})


def returnwmessage(req, url, u, pro, msg, ta):
    return render(req, url, {"accountName": u.name, "accountEmail": u.email,
                             "accountProfession": pro,
                             "accountPassword": u.password,
                             "accountPhoneNumber": u.phoneNumber,
                             "accountAddress": u.homeAddress,
                             "message": msg,
                             "TA": ta})


def returnnomessage(req, url, u, pro, ta):
    return render(req, url, {"accountName": u.name, "accountEmail": u.email,
                             "accountProfession": pro,
                             "accountPassword": u.password,
                             "accountPhoneNumber": u.phoneNumber,
                             "accountAddress": u.homeAddress,
                             "TA": ta})


def getProfession(u):
    if u.type == AccountType.TA:
        return "TA"

    if u.type == AccountType.Professor:
        return "Professor"

    if u.type == AccountType.Administrator:
        return "Administrator"
