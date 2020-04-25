from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
# from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView, View

from .models import Profile, Schedule, Attendence, Leave, Appointment, Visitor, Routine, Complaint

from django.contrib.auth.models import User
import datetime

# Create your views here.

def home(request):
	return render(request, 'hp/home.html', {})



class UserFormView(View):
	form_class = UserForm
	template_name = 'hp/registration_form.html'

	# display form blank
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form':form})
		# pass

	#process form data
	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():

			user = form.save(commit=False)

			# cleaned (normalized) data
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			user.set_password(password)
			user.save()

			# returns user objects if credentials are correct
			user = authenticate(username=username, password=password)
			if user is not None:

				if user.is_active:
					login(request,user)
					#request.user.username/pwd/....
					return redirect('hp:login')

		return render(request, self.template_name, {'form':form})



@login_required
def profile(request):
	q = Attendence.objects.filter(mark_status='Absent', dr=request.user)
	if q.exists():
		b = Profile.objects.get(user=request.user)
		b.absent_count=q.count()
		b.save()
		return render(request, 'hp/profile.html')
	else:
		# x = User.objects.filter(username=User.username)
		# y = x.first()
		# t = Profile.name
		# file = Profile.objects.filter(user=y).first()
		# if User.Profile.gender =='M' :
		# def get(self,request):
		return render(request, 'hp/profile.html')
	"""		
	def post(self,request):
		p = Attendence()
		p.dr = request.POST['user_id']
		p.date = request.POST['date']
		p.mark_status = 'Present'
	# else :
		# redirect('hp:enter')
	"""

"""
class Enter(CreateView):
	model = Profile
	fields = ['user' , 'name' , 'gender', 'work_area' , 'room' ,'profession'  ]
	success_url = reverse_lazy('hp:profile')
"""
"""
def favorite(request):
	album = get_object_or_404(Album, pk=album_id)
	try:
		selected_song = album.song_set.get(pk=request.POST['song'])
	except (KeyError, Song.DoesNotExist):
		return render(request, 'hp/profile.html', {
			'album':album,
			'error_msg': "You did not select a Song",
			})
	else:
		selected_song.is_favorite = True
		selected_song.save()
		return render(request, 'music/detail.html', {'album':album} )

"""




def enterProfile(request):
	if request.method=='GET':
		return render(request, 'hp/enterProfile.html')
	else:
		p = Profile()
		p.user = request.user
		p.name= request.POST['name']
		p.gender = request.POST['gender']
		p.work_area = request.POST['work_area']
		p.profession= request.POST['profession']
		p.room = request.POST['room']
		p.present_count = 0
		p.absent_count=0
		p.save()
		return redirect(reverse_lazy('hp:profile'))




# Doctor
def display_schedule(request):
	y = Profile.objects.get(user=request.user)
	if y.profession=='Patient' or y.profession=='Receiptionist':
		return render(request, 'hp/noAccess.html')
	else:
		x = datetime.date.today()
		data = { 'date_today' : x }
		return render(request, 'hp/schedule.html', data)




# Doctor and Receiptionist 
def mark(request):
	y = Profile.objects.get(user=request.user)
	if y.profession=='Patient':
		return render(request, 'hp/noAccess.html')
	else:
		if request.method=='GET':
			z = Attendence.objects.filter(present_date=datetime.date.today(), dr=request.user)
			x = z.first()
			a = Attendence()
			# a.present_date = datetime.date.today()
			# a.dr = request.user
			# a.mark_status = request.POST['status']
			if x is None:
				return render(request, 'hp/mark_attendence.html', {'y':True})
			if x.mark_status=='Present':
				return render(request, 'hp/mark_attendence.html', {'y':False})
			else:
				return render(request, 'hp/mark_attendence.html', {'y':True})
		else:
			a = Attendence()
			a.present_date = datetime.date.today()
			a.dr = request.user
			a.mark_status = request.POST['status']
			a.save()
			# q = Attendence.objects.filter(mark_status='Absent', dr=request.user)
			b = Profile.objects.get(user=request.user)
			# b.absent_count=q.count()
			b.present_count+=1
			b.save()
			return redirect(reverse_lazy('hp:profile'))


# doctor and receiptionist
def applyLeave(request):
	y = Profile.objects.get(user=request.user)
	if y.profession=='Patient':
		return render(request, 'hp/noAccess.html')
	else:
		if request.method=='GET':
			return render(request, 'hp/applyLeave.html')
		else:
			l = Leave()
			l.dr = request.user
			l.from_date = request.POST['from_date']
			l.to_date = request.POST['to_date']
			l.reason = request.POST['reason']
			l.grant_status = 'Not Answered'
			l.save()
			# b = Profile.objects.get(user=request.user)
			# b.present_count+=1
			# b.save()
			return redirect('hp:profile')


#doctor and receiptionist
def viewLeave(request):
	y = Profile.objects.get(user=request.user)
	if y.profession=='Patient' :
		return render(request, 'hp/noAccess.html')
	else:
		a = Leave.objects.filter(dr=request.user)
		return render(request, 'hp/viewLeave.html', {'all_leaves':a})

#doctor and receiptionist
def deleteLeave(request):
	y = Profile.objects.get(user=request.user)
	if y.profession=='Patient' :
		return render(request, 'hp/noAccess.html')
	else:
		if request.method=='GET':
			a = Leave.objects.filter(dr=request.user)
			return render(request, 'hp/deleteLeave.html', {'all_leaves':a})
		else:
			a = Leave.objects.filter(dr=request.user)
			if not a.exists():
				return redirect('hp:profile')
			else:
				leave_id = request.POST['leave_id']
				d = Leave.objects.get(pk=leave_id)
				d.delete()
				a = Leave.objects.filter(dr=request.user)
				return render(request, 'hp/viewLeave.html', {'all_leaves':a})




#rec
def addSchedule(request):
	y = Profile.objects.get(user=request.user)
	if y.profession != 'Receiptionist':
		return render(request, 'hp/noAccess.html')
	else:
		if request.method=='GET':
			return render(request,'hp/addSchedule.html', {'all_users':User.objects.all()})
		else:
			s = Schedule()
			p = request.POST['user']
			x = User.objects.get(username=p)
			s.dr = x
			s.work_date = request.POST['work_date']
			s.work_time = request.POST['work_time']
			s.work = request.POST['work']
			s.save()
			return redirect(reverse_lazy('hp:profile'))		


#rec
def addRoutine(request):
	y = Profile.objects.get(user=request.user)
	if y.profession !='Receiptionist':
		return render(request, 'hp/noAccess.html')
	else:
		if request.method=='GET':
			return render(request,'hp/addRoutine.html', {'all_users':User.objects.all()})
		else:
			s = Routine()
			p = request.POST['user']
			x = User.objects.get(username=p)
			s.pt = x
			s.routine_date = request.POST['routine_date']
			s.routine_time = request.POST['routine_time']
			s.routine = request.POST['routine']
			s.save()
			return redirect(reverse_lazy('hp:profile'))		



#rec
def addVisitor(request):
	y = Profile.objects.get(user=request.user)
	if y.profession !='Receiptionist':
		return render(request, 'hp/noAccess.html')
	else:
		if request.method=='GET':
			return render(request,'hp/addVisitor.html', {'all_users':User.objects.all()})
		else:
			s = Visitor()
			p = request.POST['user']
			x = User.objects.get(username=p)
			s.pt = x
			s.checkin = request.POST['checkin']
			s.checkout = request.POST['checkout']
			s.number = request.POST['number']
			s.visitor_details = request.POST['visitor_details']
			s.save()
			return redirect(reverse_lazy('hp:profile'))		



#rec
def replyComplaint(request):
	y = Profile.objects.get(user=request.user)
	if  y.profession != 'Receiptionist':
		return render(request, 'hp/noAccess.html')
	else:
		if request.method=='GET':
			c = Complaint.objects.filter(complaint_status='Not Attended')
			return render(request, 'hp/replyComplaint.html', {'all':c})
		else:
			complaint_id = request.POST['complaint_id']
			reply = request.POST['reply']
			if reply is None:
				return render(request, 'hp/replyC.html', {'c':Complaint.objects.get(pk=complaint_id)} )
			else:
				c = Complaint.objects.get(pk=complaint_id)
				c.reply = request.POST['reply']
				c.complaint_status = request.POST['complaint_status']
				c.save()
				return redirect(reverse_lazy('hp:profile'))


#rec
def replyC(request, complaint_id):
	y = Profile.objects.get(user=request.user)
	if y.profession != 'Receiptionist':
		return render(request, 'hp/noAccess.html')
	else:
		if request.method=='GET':
			c = Complaint.objects.get(pk=complaint_id)
			if c is not None:
				return render(request, 'hp/replyC.html', {'c':c})
			else:
				return redirect(reverse_lazy('hp:replyComplaint'))
		else:
			c = Complaint.objects.get(pk=complaint_id)
			c.reply = request.POST['reply']
			c.complaint_status = request.POST['complaint_status']
			c.save()
			return redirect(reverse_lazy('hp:replyComplaint'))



#rec
def replyAppointment(request):
	y = Profile.objects.get(user=request.user)
	if  y.profession != 'Receiptionist':
		return render(request, 'hp/noAccess.html')
	else:
		if request.method=='GET':
			c = Appointment.objects.filter(appointment_status='Not Confirmed')
			return render(request, 'hp/replyAppointment.html', {'all':c})


#rec
def replyA(request, appointment_id):
	y = Profile.objects.get(user=request.user)
	if y.profession != 'Receiptionist':
		return render(request, 'hp/noAccess.html')
	else:
		if request.method=='GET':
			c = Appointment.objects.get(pk=appointment_id)
			if c is not None:
				return render(request, 'hp/replyA.html', {'c':c})
			else:
				return redirect(reverse_lazy('hp:replyAppointment'))
		else:
			c = Appointment.objects.get(pk=appointment_id)
			c.remarks = request.POST['remarks']
			c.appointment_status = request.POST['appointment_status']
			c.save()
			return redirect(reverse_lazy('hp:replyAppointment'))









#Patient : 

def visitor(request):
	y = Profile.objects.get(user=request.user)
	if y.profession!='Patient':
		return render(request, 'hp/noAccess.html')
	else:
		x = Visitor.objects.filter(pt=request.user)
		return render(request,'hp/visitors.html', {'all_visitors':x})

def routine(request):
	y = Profile.objects.get(user=request.user)
	if y.profession!='Patient':
		return render(request, 'hp/noAccess.html')
	else:
		return render(request, 'hp/routine.html')



def makeAppointment(request):
	y = Profile.objects.get(user=request.user)
	if y.profession!='Patient':
		return render(request, 'hp/noAccess.html')
	else:
		if request.method=='GET':
			return render(request, 'hp/makeAppointment.html')
		else:
			a = Appointment()
			a.pt = request.user
			a.illness = request.POST['illness']
			a.a_date = request.POST['a_date']
			a.appointment_status = 'Not Confirmed'
			a.save()
			return redirect(reverse_lazy('hp:viewAppointment'))


def viewAppointment(request):
	y = Profile.objects.get(user=request.user)
	if y.profession!='Patient':
		return render(request, 'hp/noAccess.html')
	else:
		return render(request, 'hp/viewAppointment.html')



def makeComplaint(request):
	y = Profile.objects.get(user=request.user)
	if y.profession!='Patient':
		return render(request, 'hp/noAccess.html')
	else:
		if request.method=='GET':
			return render(request,'hp/makeComplaint.html')
		else:
			s = Complaint()
			# p = request.POST['user']
			x = Profile.objects.get(user=request.user)
			s.pt = request.user
			s.issue = request.POST['issue']
			# s.complaint_time = request.POST['complaint_time']
			s.room = x.room
			s.save()
			return redirect(reverse_lazy('hp:profile'))	


def viewComplaint(request):
	y = Profile.objects.get(user=request.user)
	if y.profession!='Patient':
		return render(request, 'hp/noAccess.html')
	else:
		a = Complaint.objects.filter(pt=request.user)
		return render(request, 'hp/viewComplaint.html', {'all_complaint':a})




def deleteComplaint(request):
	y = Profile.objects.get(user=request.user)
	if y.profession!='Patient':
		return render(request, 'hp/noAccess.html')
	else:
		if request.method=='GET':
			a = Complaint.objects.filter(pt=request.user)
			return render(request, 'hp/deleteComplaint.html', {'all_complaint':a})
		else:
			a = Complaint.objects.filter(pt=request.user)
			if not a.exists():
				return redirect(reverse_lazy('hp:profile'))
			else:
				complaint_id = request.POST['complaint_id']
				d = Complaint.objects.get(pk=complaint_id)
				d.delete()
				a = Complaint.objects.filter(pt=request.user)
				return render(request, 'hp/viewComplaint.html', {'all_complaint':a})



