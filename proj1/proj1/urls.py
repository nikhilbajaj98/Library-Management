"""proj1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app import views
urlpatterns = [
    url(r'^$',views.start),
	url(r'^admin/', admin.site.urls),
    url(r'^reg/$',views.register),
    url(r'^login/$',views.login),
    url(r'^stu/$',views.student),
    url(r'^lib/$',views.librarian),
    url(r'^logout/$',views.logout),
    url(r'^book_details/$',views.summary),
    url(r'^profile/$',views.profile),
    url(r'^results/$',views.results),
    url(r'^forgetpassword/$',views.lostpass),
	url(r'^verify/$',views.verify),
	url(r'^verify1/$',views.verify1),
	url(r'^change/$',views.change),
	url(r'^requestbook/$',views.reqbook),
	url(r'^History/$',views.history),
	url(r'^Return/$',views.Return),
	url(r'^lib1/$',views.pickedup),
	url(r'^lib2/$',views.Return),
	
		
		

]
