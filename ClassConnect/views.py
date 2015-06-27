import sys

from django.core.exceptions import PermissionDenied
from django.http import (HttpResponse, HttpResponseNotFound,
    HttpResponseBadRequest, HttpResponseServerError)
from django.views.generic.base import View
from django.views.generic import TemplateView

from django.shortcuts import render

from django.contrib.auth.views import redirect_to_login
import requests
import json
import pdb


class ErrorView(View):
    """ HTTP 500: Internal Server Error """
    template_name = '500.html'
    status = 500
    
    def get(self, request):
        return render(request, self.template_name, status=self.status)
    
    
class PermissionDeniedView(ErrorView):
    """ HTTP 403: Forbidden """
    template_name = '403.html'
    status = 403
    
    
class NotFoundView(ErrorView):
    """ HTTP 404: Not Found """
    template_name = '404.html'
    status = 404

class LoginPage(TemplateView):
    template_name = 'login.html'

class MessagingPage(TemplateView):
    template_name = 'messaging.html'

class ClassesPage(TemplateView):
    template_name = 'classes.html'
    def get (self, request):
        r = requests.post('http://sandbox.api.hmhco.com/v1/sample_token?client_id=40694671-d66a-44b9-a1f5-471522046577.hmhco.com&grant_type=password&username=gandalf&password=password',
                        headers={'Vnd-HMH-Api-Key':'8ad2641f17b878c1e7df05ee2bb09dbb', 
                        'Content-Type':'application/x-www-form-urlencoded'})
        data = json.loads(r.text)
        # return HttpResponse(r)
        if data['roles'] == 'Instructor':
            classIDs = requests.get('http://sandbox.api.hmhco.com/v1/staffSectionAssociations',
                            headers={'Authorization': data['access_token'],
                            'Vnd-HMH-Api-Key':'8ad2641f17b878c1e7df05ee2bb09dbb', 
                            'Content-Type':'application/json',
                            'Accept':'application/json'})
            tempData = json.loads(classIDs.text)
            classes = []
            for section in tempData:
                if data['ref_id'] == section['staffPersonRefId']:
                    classID = section['sectionRefId']
                    temp = requests.get('http://sandbox.api.hmhco.com/v1/sections/' + str(classID),
                                headers={'Authorization': data['access_token'],
                                'Vnd-HMH-Api-Key':'8ad2641f17b878c1e7df05ee2bb09dbb', 
                                'Content-Type':'application/json',
                                'Accept':'application/json'})
                    classes.append(json.loads(temp.text))
            classes.append({"longName":"TempClass1"})
        return render(request, 'classes.html', {"classes": classes})
    
    
class IndexPage(TemplateView):
    """ The Index Page. """
    template_name = 'index.html'

    def get (self, request):
        r = requests.post('http://sandbox.api.hmhco.com/v1/sample_token?client_id=40694671-d66a-44b9-a1f5-471522046577.hmhco.com&grant_type=password&username=gandalf&password=password',
                        headers={'Vnd-HMH-Api-Key':'8ad2641f17b878c1e7df05ee2bb09dbb', 
                        'Content-Type':'application/x-www-form-urlencoded'})
        data = json.loads(r.text)
        # return HttpResponse(r)
        if data['roles'] == 'Instructor':
            classIDs = requests.get('http://sandbox.api.hmhco.com/v1/staffSectionAssociations',
                            headers={'Authorization': data['access_token'],
                            'Vnd-HMH-Api-Key':'8ad2641f17b878c1e7df05ee2bb09dbb', 
                            'Content-Type':'application/json',
                            'Accept':'application/json'})
            tempData = json.loads(classIDs.text)
            classes = []
            for section in tempData:
                if data['ref_id'] == section['staffPersonRefId']:
                    classID = section['sectionRefId']
                    temp = requests.get('http://sandbox.api.hmhco.com/v1/sections/' + str(classID),
                                headers={'Authorization': data['access_token'],
                                'Vnd-HMH-Api-Key':'8ad2641f17b878c1e7df05ee2bb09dbb', 
                                'Content-Type':'application/json',
                                'Accept':'application/json'})
                    classes.append(json.loads(temp.text))
            
        return render(request, 'index.html', {"data": data, "classes": classes})


    
def staff_only(view):
    """ Staff-only View decorator. """
    
    def decorated_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect_to_login(request.get_full_path())
            
        if not request.user.is_staff:
            raise PermissionDenied
            
        return view(request, *args, **kwargs)
        
    return decorated_view
    
    