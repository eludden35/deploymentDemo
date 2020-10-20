from django.db import models
from datetime import date
# Create your models here.

class TripManager(models.Manager):
    def tripValidator(self, post):

        errors = {}
        today = date.today()
# for key, value in resultsfromValidator.items()
        # destination
        if len(post['dest']) == 0:
            errors['destreq'] = "Destination is required."
        # description
        if len(post['desc']) == 0:
            errors['descreq'] = "Description is required."
        # travel date start
        if len(post['dtStart']) == 0:
            errors['startreq'] = "Start date is required."
        # Start date after todays date
        elif post['dtStart'] <= str(today):
            errors['startTimereq'] = "Trip must start after today."
        # travel date end
        if len(post['dtEnd']) == 0:
            errors['endreq'] = "End date is required."
        # End date after start date
        elif post['dtEnd'] <= post['dtStart']:
            errors['endTimereq'] = "Trip must end after trip start."

        
        return errors

class UserManager(models.Manager):

    # Registration validator:

    def regiValidator(self, post):

        errors = {}

        # name
        if len(post['name']) == 0:
            errors['namereq'] = "First name is required."
        elif len(post['name']) < 3:
            errors['namereq'] = "First name must be atleast 3 characters."
        # username
        if len(post['uName']) == 0:
            errors['uNamereq'] = "Username is required."
        elif len(post['uName']) < 3:
            errors['uNamereq'] = "Username must be atleast 3 characters."
        # password
        if len(post['pwd']) == 0:
            errors['pwdreq'] = "Password is required."
        elif len(post['pwd']) < 8:
            errors['pwdlenreq'] = "Password needs to be atleast 8 characters!!"
        if post['pwd'] != post['cpw']:
            errors['confirmpw'] = "Password does not match !"


        return errors

# Log-in validator:

    def logInValid(self, post):
            errors = {}

            userMatch = User.objects.filter(username= post['uName'])
            print(userMatch)
            print('*******************************************************')

            if len(post['uName']) == 0:
                errors['userReq'] = "Username is required."
            elif len(userMatch) == 0:
                errors['userNo'] = 'No matching username !!'
            else:
                if userMatch[0].password != post['pwd']:
                    errors['badPw'] = "Invalid password !!"

            return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    dest = models.CharField(max_length=255)
    desc = models.TextField()
    travStart = models.DateTimeField()
    travEnd = models.DateTimeField()
    plan = models.ForeignKey(User, related_name="tripPlans", on_delete = models.CASCADE, null = True)
    join = models.ManyToManyField(User, related_name="joinTrip")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

