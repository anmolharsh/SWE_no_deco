from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import datetime

# Create your models here.

gender_choices = ( ('Male','Male'), ('Female','Female'), ('Others','Others') )
profession_choices = ( ('Receiptionist','Receiptionist') , ('Patient','Patient') , ('Nurse','Nurse') , ('Doctor','Doctor') , ('Staff','Staff') )
mark_choices = ( ('Present','Present') , ('Absent','Absent') )
grant_choices = ( ('Granted','Granted') , ('Not Answered', 'Not Answered') , ('Not Granted','Not Granted') )
complaint_choices = ( ('Attended', 'Attended') , ('Not Attended', 'Not Attended') )
appointment_choices = ( ('Confirmed','Confirmed') , ('Not confirmed' , 'Not confirmed') , ('Declined','Declined') )


class Profile(models.Model):
	user = models.OneToOneField(User,  on_delete=models.CASCADE)
	name = models.CharField(max_length=20, default=None)
	gender = models.CharField(max_length=7, choices=gender_choices)
	work_area = models.CharField(max_length=20)
	profession = models.CharField(max_length=17, choices=profession_choices)
	present_count = models.IntegerField(default=0)
	absent_count = models.IntegerField(default=0)
	room = models.CharField(max_length=5)


class Attendence(models.Model):
	dr = models.ForeignKey(User, on_delete=models.CASCADE)
	present_date = models.DateField()
	mark_status = models.CharField(max_length=10, default='Absent', choices=mark_choices)


class Schedule(models.Model):
	dr = models.ForeignKey(User, on_delete=models.CASCADE)
	work_date = models.DateField()
	work_time = models.TimeField()
	work = models.CharField(max_length=50)

	def get_a_feature(self):
		return self.schedule_set.filter(work_date=datetime.date.today())

	def __str__(self):
		if self.work_date == datetime.date(datetime.today()):
			return self.work + ' : ' + str(self.work_time) 
		else: 
			return ''

class Leave(models.Model):
	dr = models.ForeignKey(User, on_delete=models.CASCADE)
	from_date = models.DateField(blank=True,)
	to_date = models.DateField(blank=True,)
	reason = models.TextField(max_length=50)
	grant_status = models.CharField(max_length=20, blank=True, default='Not Answered', choices=grant_choices)


class Routine(models.Model):
	pt = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
	routine_date = models.DateField()
	routine_time = models.TimeField()
	routine = models.CharField(max_length=80)
	def __str__(self):
		if self.routine_date== datetime.date(datetime.today()) :
			return self.routine + ' : ' + str(self.routine_time) 
		else: 
			return ''

class Complaint(models.Model):
	pt = models.ForeignKey(User, on_delete=models.CASCADE)
	issue = models.CharField(max_length=30)
	complaint_status = models.CharField(max_length=15, default='Not Attended' , choices=complaint_choices)
	reply = models.CharField(max_length=50, default='Will be answered shortly')
	room = models.CharField(max_length=7, default='')
	complaint_datetime = models.DateTimeField(default=datetime.now())

class Appointment(models.Model):
	pt = models.ForeignKey(User, on_delete=models.CASCADE )
	illness = models.CharField(max_length=30)
	a_date = models.DateField()
	appointment_status = models.CharField(max_length=15, default=None, choices=appointment_choices)
	remarks = models.CharField(max_length=40, default='')


class Visitor(models.Model):
	pt = models.ForeignKey(User,  on_delete=models.CASCADE)
	number = models.IntegerField()
	checkin = models.DateTimeField(default=None)
	checkout = models.DateTimeField(default=None)
	visitor_details = models.CharField(max_length=300, default='No name')



