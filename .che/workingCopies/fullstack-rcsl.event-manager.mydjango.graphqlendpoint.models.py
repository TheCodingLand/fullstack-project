from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.


class LoggedInUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='logged_in_user',on_delete=models.CASCADE)


class Category(models.Model):
    title = models.CharField(max_length=200, null=True)
    predecessor = models.IntegerField(null=True, blank=True)
    searchcode = models.CharField(max_length=200, null=True)
    ot_id = models.CharField(max_length=200, null=True)
    
    def create_from_json(self,data):
        self.title = data.get("Title")
        self.searchcode = data.get("SearchCode")
        self.ot_id = data.get("id")
    
    def __str__(self):
        return "%s" % self.title

class Call(models.Model):
    ucid = models.CharField(max_length=200, unique=True)
    state = models.CharField(max_length=200, null=True)
    origin = models.CharField(max_length=200, null=True)
    destination = models.CharField(max_length=200, null=True)
    call_type = models.CharField(max_length=200, null=True)
    start = models.DateTimeField(max_length=200, null=True)
    end = models.DateTimeField(max_length=200, null=True, blank=True)
    isContactCenterCall = models.BooleanField(default=False)
    history = models.CharField(max_length=600, null=True)


    def __str__(self):
        return "%s" % self.ucid
        
    def getTransfers(self):
        tf = Transfer.objects.filter(call=self).order_by('ttimestamp')
        return tf
   
    def updatehistory(self):
        self.history = ""
        for t in self.getTransfers():
            if t.torigin =="" and t.torigin:
                #first transfer
                self.history == t.tdestination
            else:
                #other transfers
                self.history = "%s -> %s" % (self.history, t.tdestination)
        self.save()


class Agent(models.Model):
    firstname = models.CharField(max_length=200, null=True)
    lastname = models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=False)
    ot_userloginname = models.CharField(max_length=200, null=True)
    ot_userdisplayname = models.CharField(max_length=200, null=True, blank=True)
    ot_id = models.CharField(max_length=200,null=True)
    user=models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    phone_login = models.CharField(max_length=200, null =True)
    phone_active = models.BooleanField(default=False)
    ext = models.CharField(max_length=200, null=True, unique=True)
    phone_state = models.CharField(max_length=200, default = "available", blank=True)
    avatar = models.ImageField(upload_to='userimage',blank=True)
    current_call = models.ForeignKey(Call,null=True, on_delete=models.SET_NULL, related_name='current_agent')
    def __str__(self):
        return "%s" % self.firstname
        
class Ticket(models.Model):
    creationdate = models.DateTimeField(null=True)
    title=models.DateTimeField(null=True)
    category =models.ForeignKey(Category, related_name='category_tickets', on_delete=models.DO_NOTHING, null=True)
    applicant = models.ForeignKey(Agent, related_name='tickets_created', on_delete=models.CASCADE, null=True)
    responsible = models.ForeignKey(Agent, related_name='tickets_responsible', on_delete=models.CASCADE, null=True)
    state = models.CharField(max_length=200, null=True)
    solution = models.CharField(max_length=200, null=True)
    ot_id = models.CharField(max_length=200, null=True)
   
    def __str__(self):
        return "%s" % self.title
 
       
class Event(models.Model):
    creationdate = models.DateTimeField(null=True)
    end=models.DateTimeField(null=True)
    ot_id = models.IntegerField(null=True)
    applicant = models.ForeignKey(Agent, related_name='events_applicant', on_delete=models.CASCADE, null=True)
    responsible = models.ForeignKey(Agent, related_name='events_responsible', on_delete=models.CASCADE, null=True)
    state = models.CharField(max_length=200, null=True)
    transferhistory = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    ticket = models.ForeignKey(Ticket, related_name='tickets', on_delete=models.CASCADE, null=True)
    call = models.ForeignKey(Call, on_delete=models.SET_NULL, null=True, related_name='event')
    def __str__(self):
        return  "%s" % self.ot_id    
    


        





class Transfer(models.Model):
    torigin = models.CharField(max_length=200, null=True)
    tdestination = models.CharField(max_length=200)
    ttimestamp = models.DateTimeField(max_length=200)
    call = models.ForeignKey(Call, on_delete=models.CASCADE)
    
    
    
class ActiveCalls(models.Model):
    call = models.OneToOneField(
        Call, related_name='active',on_delete=models.CASCADE)
.CASCADE)
)
CADE)
ASCADE)
ASCADE)



ADE)

SCADE)
DE)
DE)
CADE)
DE)
SCADE)
)
.CASCADE, null=True)
    event = models.OneToOneField(Event, on_delete=models.DO_NOTHING, null=True, related_name='event')
    def __str__(self):
        return  "%s" % self.ot_id    
    


        





class Transfer(models.Model):
    torigin = models.CharField(max_length=200, null=True)
    tdestination = models.CharField(max_length=200)
    ttimestamp = models.DateTimeField(max_length=200)
    call = models.ForeignKey(Call, on_delete=models.CASCADE)
    
    
    
class ActiveCalls(models.Model):
    call = models.OneToOneField(
        Call, related_name='active',on_delete=models.CASCADE)
els.CharField(max_length=200, null=True)
    ticket = models.ForeignKey(Ticket, related_name='tickets', on_delete=models.CASCADE, null=True)
    event = models.OneToOneField(Event, on_delete=models.DO_NOTHING, null=True, related_name='event')
    def __str__(self):
        return  "%s" % self.ot_id    
    


        


class Ticket(models.Model):
    creationdate = models.DateTimeField(null=True)
    title=models.DateTimeField(null=True)
    category =models.ForeignKey(Category, related_name='category_tickets', on_delete=models.DO_NOTHING, null=True)
    applicant = models.ForeignKey(Agent, related_name='tickets_created', on_delete=models.CASCADE, null=True)
    responsible = models.ForeignKey(Agent, related_name='tickets_responsible', on_delete=models.CASCADE, null=True)
    state = models.CharField(max_length=200, null=True)
    solution = models.CharField(max_length=200, null=True)
    ot_id = models.CharField(max_length=200, null=True)
   
    def __str__(self):
        return "%s" % self.title
 


class Transfer(models.Model):
    torigin = models.CharField(max_length=200, null=True)
    tdestination = models.CharField(max_length=200)
    ttimestamp = models.DateTimeField(max_length=200)
    call = models.ForeignKey(Call, on_delete=models.CASCADE)
    
    
    
class ActiveCalls(models.Model):
    call = models.OneToOneField(
        Call, related_name='active',on_delete=models.CASCADE)
