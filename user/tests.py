from django.test import TestCase
from django.http import *
import json
from django.core.serializers import serialize
from .models import Advisor, User, Bookings
from rest_framework.authtoken.models import Token

# Create your tests here.

class test_Registration(TestCase):
    
    def testRegister(self):
        url = 'http://127.0.0.1:8000/user/register/'

        # normal registration - 200_OK
        print('\nNormal Registration - 200_OK\n')        
        data = {
            'uname' : 'Test User 0',
            'uemail' : 'testuser0@localhost.app',
            'pwd' : 'P@$$w0rd_0'
            }
        print(data)
        response = self.client.post(url, data)        
        print(json.loads(response.content))     # loads Authentication Token and User ID in JSON Format
        print('Status Code : ', response.status_code)             # Status Code

        print('\nEmail Exists - 200_OK\n')
        # Email exists
        data = {
                'uname' : 'TestUser Email_Exists',
                'uemail' : 'testuser0@localhost.app',
                'pwd' : 'P@$$w0rd'
                }
        print(data)
        response = self.client.post(url, data)
        print(response.status_code)        

        print('\nMissing Information - 400_BADREQUEST\n')
        # Empty fields
        for i in range(3):
            data = {
                'uname' : 'TestUser'+str(i+10),
                'uemail' : 'testuser'+str(i+10)+'@localhost.app',
                'pwd' : 'P@$$w0rd_'+str(i+10)
                }
            if i == 0:
                data['uname'] = ''
            elif i == 1:
                data['uemail'] = ''
            else:
                data['pwd'] = ''
            print(data)
            response = self.client.post(url, data)
            print(response.status_code)



class test_Login(TestCase):

    def testLogin(self):
        url = 'http://127.0.0.1:8000/user/login/'

        # Authorised login - 200_OK
        User.objects.create(uName='Test User 1',uEmail='testuser1@localhost.app',password='P@$$w0rd').save()        
        print('\nAuthorised login - 200_OK\n')
        data = {            
            'uemail' : 'testuser1@localhost.app',
            'pwd' : 'P@$$w0rd'
            }
        print(data)
        response = self.client.post(url, data)
        print(json.loads(response.content))     # loads Authentication Token and User ID in JSON Format
        print('Status Code : ',response.status_code)             # Status Code
        

        # Unauthorised login - 401_UNAUTHORISED (user doesn't exist)
        print('\nUnauthorised login - 401_UNAUTHORISED\n')
        data = {            
            'uemail' : 'testuser2@localhost.app',
            'pwd' : 'P@$$w0rd_0'
            }
        print(data)
        response = self.client.post(url, data)
        print('Status Code : ', response.status_code)
        print('Content : ', response.content)

        # Empty fields
        print('\nMissing Fields Login - 400_BADREQUEST\n')        
        for i in range(2):
            data = {                
                'uemail' : 'testuser'+str(i+1)+'@localhost.app',
                'pwd' : 'P@$$w0rd_'+str(i+1)
                }            
            if i == 0:
                data['uemail'] = ''
            else:
                data['pwd'] = ''
            print(data)
            response = self.client.post(url, data)
            print(response.status_code)


class test_AddAdvisor(TestCase):

    def testAddAdv(self):
        url = 'http://127.0.0.1:8000/admin/advisor/'

        # Normal Add - 200_OK
        print('\nNormal Addition - 200_OK\n')
        data = {            
            'aname' : 'Test Advisor 0',
            'img' : 'http://advisorpic0.localhost.app'
            }
        print(data)
        response = self.client.post(url, data)
        print('Status Code : ', response.status_code)

    # Empty fields
        print('\nMissing Fields - 400_BADREQUEST\n')
        for i in range(2):
            data = {                
                'aname' : 'Test Advisor '+str(i+1),
                'img' : 'http://advisorpic'+str(i+1)+'.localhost.app'
                }
            if i == 0:
                data['aname'] = ''
            else:
                data['img'] = ''
            print(data)
            response = self.client.post(url, data)
            print(response.status_code)


class test_ListAdvisrs(TestCase):

    def testAdvList(self):
        print('\nList Advisors - 200_OK\n')
        User.objects.create(uName='Test User 2',uEmail='testuser2@localhost.app',password='P@$$w0rd').save()
        Advisor.objects.create(advName='Test Advisor 1',imgURL='http://advisorpic1.localhost.app').save()        
        Advisor.objects.create(advName='Test Advisor 2',imgURL='http://advisorpic2.localhost.app').save()
        url = 'http://127.0.0.1:8000/user/1/advisor/'
        response = self.client.get(url)
        print(response.content.decode('utf-8'))
        print(response.status_code)



class test_Book(TestCase):

    def testBooking(self):
        
        User.objects.create(uName='Test User 3',uEmail='testuser3@localhost.app',password='P@$$w0rd').save()
        Advisor.objects.create(advName='Test Advisor 3',imgURL='http://advisorpic3.localhost.app').save()
        url = 'http://127.0.0.1:8000/user/1/advisor/2/'

        # query 200_OK
        print('\nBook Advisors - 200_OK\n')
        data = {                
                'book_time' : '2021-03-07T18:30:00+05:30'
                }
        response = self.client.post(url,data)
        print(response.status_code)



class test_ViewBooking(TestCase):

    def testViewBookings(self):        
        usr = User.objects.create(uName='Test User 4',uEmail='testuser4@localhost.app',password='P@$$w0rd')
        usr.save()
        adv1 = Advisor.objects.create(advName='Test Advisor 4',imgURL='http://advisorpic4.localhost.app')
        adv1.save()
        adv2 = Advisor.objects.create(advName='Test Advisor 5',imgURL='http://advisorpic5.localhost.app')
        adv2.save()
        Bookings.objects.create(time='2021-03-07T18:30:00+05:30',uID=usr,aID=adv1)
        Bookings.objects.create(time='2021-05-11T10:05:00+05:30',uID=usr,aID=adv2)
        url = 'http://127.0.0.1:8000/user/1/advisor/booking/'
        response = self.client.get(url)
        print(response.content.decode('utf-8'))
        print(response.status_code)

