from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'hp'

urlpatterns = [

	# /$
	url(r'^$', views.home, name='home'),

	# /hp/register/
	url(r'^register/$', views.UserFormView.as_view(), name='register'),

	# /hp/login/
	url(r'^login/$', auth_views.LoginView.as_view(template_name='hp/login.html'), name='login' ),

	# /hp/logout/ template_name='music/logout.html'
	url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout' ),

	# /hp/profile/
	url(r'^profile/$', views.profile, name='profile' ),

	# /hp/enter/
	url(r'^enter/$', views.enterProfile, name='enter' ),

	# /hp/schedule/
	url(r'^schedule/$', views.display_schedule, name='schedule' ),

	# /hp/addSchedule/
	url(r'^addSchedule/$', views.addSchedule, name='addSchedule' ),

	# /hp/addRoutine/
	url(r'^addRoutine/$', views.addRoutine, name='addRoutine' ),

	# /hp/addVisitor/
	url(r'^addVisitor/$', views.addVisitor, name='addVisitor' ),

	# /hp/replyAppointment/
	url(r'^replyAppointment/$', views.replyAppointment, name='replyAppointment' ),
	
	# /hp/replyAppointment/replyA/<appointment_id>
	url(r'^replyAppointment/replyA/(?P<appointment_id>[0-9]+)/$' , views.replyA, name='replyA' ),
	
	# /hp/replyComplaint/
	url(r'^replyComplaint/$', views.replyComplaint, name='replyComplaint' ),

	# /hp/replyComplaint/replyC/<complaint_id>
	url(r'^replyComplaint/replyC/(?P<complaint_id>[0-9]+)/$' , views.replyC, name='replyC' ),

	# /hp/mark/
	url(r'^mark/$', views.mark, name='mark' ),

	# /hp/applyLeave
	url(r'^applyLeave', views.applyLeave, name='applyLeave'),

	# /hp/viewLeave
	url(r'^viewLeave', views.viewLeave, name='viewLeave'),

	# /hp/deleteLeave
	url(r'^deleteLeave', views.deleteLeave, name='deleteLeave'),
	
	# /hp/viewComplaint
	url(r'^viewComplaint', views.viewComplaint, name='viewComplaint'),

	# /hp/deleteLeave
	url(r'^deleteComplaint', views.deleteComplaint, name='deleteComplaint'),
	
	# /hp/routine/
	url(r'^routine/$', views.routine, name='routine' ),

	# /hp/visitor/
	url(r'^visitor/$', views.visitor, name='visitor' ),
	
	# /hp/makeComplaint/
	url(r'^makeComplaint/$', views.makeComplaint, name='makeComplaint' ),
	
	# /hp/makeAppointment/
	url(r'^makeAppointment/$', views.makeAppointment, name='makeAppointment' ),
	
	# /hp/viewAppointment/
	url(r'^viewAppointment/$', views.viewAppointment, name='viewAppointment' ),
	

]