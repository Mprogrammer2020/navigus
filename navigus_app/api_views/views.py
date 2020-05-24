
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import response, status
from rest_framework.utils import json
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from api_views.serializers import *
import traceback
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

# Create your views here.
@api_view(['POST'])
def loginuser(request):
    try:
        with transaction.atomic():
            #recieved_json_data=json.loads(request.body, strict=False)
            user=authenticate(username=request.data["username"],password=request.data["password"])
            if user is not None:
                token=""
                try:
                    user_with_token=Token.objects.get(user=user)
                except:
                    user_with_token=None
                if user_with_token is None:
                    token1=Token.objects.create(user=user)
                    token=token1.key
                else:
                    Token.objects.get(user=user).delete()
                    token1=Token.objects.create(user=user)
                    token=token1.key
                userSerializer = UserSerializer(user)
                return Response({"status":"1","message":"successfully done","token":token, "user" : userSerializer.data},status=status.HTTP_200_OK)
            else:
                return Response({"status":"0","message":"Username or password incorrect"},status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(traceback.format_exc())
        return Response({"status":"0","message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def signup(request):
    try:
        recieved_json_data=json.loads(request.body, strict=False)
        first_name=recieved_json_data["first_name"]
        last_name=recieved_json_data["last_name"]
        email=recieved_json_data["email"]
        username=recieved_json_data["username"]
        password=recieved_json_data["password"]
        user=User.objects.create(first_name=first_name,last_name=last_name,email=email,username=username,password=make_password(password))
        g=Group.objects.get(name="student")
        g.user_set.add(user)
        if user is not None:
            return Response({"status":"1","message":"successfully done"},status=status.HTTP_200_OK)
        else:
            return Response({"status":"0","message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        print(traceback.format_exc())
        return Response({"status":"0","message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def signupteacher(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                    checkGroup = user.is_superuser
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                
                if checkGroup:
                    recieved_json_data=json.loads(request.body, strict=False)
                    first_name=recieved_json_data["first_name"]
                    last_name=recieved_json_data["last_name"]
                    email=recieved_json_data["email"]
                    username=recieved_json_data["username"]
                    password=recieved_json_data["password"]
                    user=User.objects.create(first_name=first_name,last_name=last_name,email=email,username=username,password=make_password(password))
                    g=Group.objects.get(name="teacher")
                    g.user_set.add(user)
                    if user is not None:
                        return Response({"status":"1","message":"successfully done"},status=status.HTTP_200_OK)
                    else:
                        return Response({"status":"0","message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({"message" : "Sorry Something went wrong.", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : "Sorry Something went wrong.", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(traceback.format_exc())
        return Response({"status":"0","message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def getstudentslisting(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    print("1")
                    token1 = Token.objects.get(key=API_key)
                    print("2")
                    user = token1.user
                    print("3")
                    checkGroup = user.is_superuser
                    print("4")
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                
                if checkGroup:
                    user = token1.user
                    users=User.objects.filter(groups__name='student')
                    return Response({"status":"1","message":"successfully done", "list":UserSerializer(users, many=True).data},status=status.HTTP_200_OK)
                else:
                    return Response({"message" : "Sorry Something went wrong.", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                print("Helloooooooooooooooooo")
                return Response({"message" : "Sorry Something went wrong.", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(traceback.format_exc())
        return Response({"status":"0","message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getteacherslisting(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                    checkGroup = user.is_superuser
                    checkGroup2 = user.groups.filter(name='student').exists()
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                
                if checkGroup or checkGroup2:          
                    user = token1.user
                    users=User.objects.filter(groups__name='teacher')
                    return Response({"status":"1","message":"successfully done", "list":UserSerializer(users, many=True).data},status=status.HTTP_200_OK)
                else:
                    return Response({"message" : "Sorry Something went wrong.", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : "Sorry Something went wrong.", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(traceback.format_exc())
        return Response({"status":"0","message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def gettimeslotslisting(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                    checkGroup = user.groups.filter(name='teacher').exists()
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                
                if checkGroup:          
                    user = token1.user
                    timeslots=TimeSlots.objects.filter(teacher_id=user.id)
                    return Response({"status":"1","message":"successfully done", "list":TimeSlotsSerializer(timeslots, many=True).data},status=status.HTTP_200_OK)
                else:
                    return Response({"message" : "Sorry Something went wrong.", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : "Sorry Something went wrong.", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(traceback.format_exc())
        return Response({"status":"0","message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getteachertimeslotsbystudent(request):
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                    checkGroup = user.groups.filter(name='student').exists()
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                
                if checkGroup:          
                    user = token1.user
                    timeslots=TimeSlots.objects.all()
                    return Response({"status":"1","message":"successfully done", "list":TimeSlotsSerializer(timeslots, many=True).data},status=status.HTTP_200_OK)
                else:
                    return Response({"message" : "Sorry Something went wrong.", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : "Sorry Something went wrong.", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(traceback.format_exc())
        return Response({"status":"0","message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

import datetime
@api_view(['POST'])
def makeslots(request):
    
    def time_slots(start_time, end_time):
        t = start_time
        while t <= end_time:
            yield t.strftime('%H:%M')
            t = (datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), t) +
                 datetime.timedelta(minutes=60)).time()
    
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                    checkGroup = user.groups.filter(name='teacher').exists()
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                
                if checkGroup:          
                    user = token1.user
                    start_time = datetime.time(9, 0)
                    end_time = datetime.time(17, 0)
                    listT = list(time_slots(start_time, end_time))
                    num = 0
                    for l in listT:
                        if(num < listT.__len__() - 1):
                            start = listT[num]
                            end = listT[num + 1]
                            newDate = datetime.date.today() + datetime.timedelta(days=1)
                            TimeSlots.objects.create(dayDate = newDate,
                                                     startTime=start,
                                                     endTime=end,
                                                     status=1,
                                                     teacher_id=user.id)
                        num = num + 1
                    return Response({"status":"1","message":"successfully done", "list":[]},status=status.HTTP_200_OK)
                else:
                    return Response({"message" : "Sorry Something went wrong.", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : "Sorry Something went wrong.", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(traceback.format_exc())
        return Response({"status":"0","message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def bookslot(request):
    
    try:
        with transaction.atomic():
            API_key = request.META.get('HTTP_AUTHORIZATION')
            if API_key is not None:
                try:
                    token1 = Token.objects.get(key=API_key)
                    user = token1.user
                    checkGroup = user.groups.filter(name='student').exists()
                except:
                    return Response({"message" : "Session Expired!! Please Login Again", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
                
                if checkGroup:          
                    user = token1.user
                    newDate = datetime.date.today()
                    recieved_json_data=json.loads(request.body, strict=False)
                    timeSlot=recieved_json_data["timeSlot"]
                    Bookings.objects.create(timeSlot_id = timeSlot,
                                             student_id=user.id,
                                             bookingTime=newDate)
                    return Response({"status":"1","message":"successfully done", "list":[]},status=status.HTTP_200_OK)
                else:
                    return Response({"message" : "Sorry Something went wrong.", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"message" : "Sorry Something went wrong.", "status" : "0"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        print(traceback.format_exc())
        return Response({"status":"0","message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)