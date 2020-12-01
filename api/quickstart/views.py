from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from api.quickstart.serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from api.db_driver.mongo_driver import MongoDriver
import json
import jwt
import datetime
from functools import wraps


mongo_driver = MongoDriver('mate')

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]





def token_required(f):
    @wraps(f)
    @api_view(['GET','POST'])
    def decorated(*args, **kwargs):
        token = None
        request = args[0]
        if 'X-Access-Token' in request.headers:
            token = request.headers['X-Access-Token']
        if not token:
            return JsonResponse({'msg':'no token'}, safe=False)

        try: 
            data = jwt.decode(token, 'SECRET_KEY')
            current_user = data["user"]
            
        except:
            return JsonResponse({'msg':'no user'}, safe=False)

        return f(current_user, *args, **kwargs)

    return decorated


@token_required
def main_graph(request, current_user):
    data_str = mongo_driver.get_main_graph()
     
    response = JsonResponse(data_str, safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"

    return response


@api_view(['GET','POST'])
def login(request):
    

    params = {"user":request.data["user"],"pass":request.data["pass"]}


    user = mongo_driver.get_user(params)

    if isinstance(user, bool):

        print("NO EXISTE")

        mongo_driver.create_user(request.data)

        time_limit = datetime.datetime.utcnow() + datetime.timedelta(minutes=30) #set limit for user
        request.data['exp'] = time_limit
        payload = request.data
        del request.data['_id']
        print()
        print()
        print()
        print(payload)
        print()
        print()
        print()
        token = jwt.encode(payload,"SECRET_KEY").decode('UTF-8')

        data_str = mongo_driver.get_main_graph()

        return JsonResponse({'token':token, 'data':data_str}, safe=False)

    else:

        print("EXISTE")
        

        data_str = mongo_driver.get_main_graph()
        time_limit = datetime.datetime.utcnow() + datetime.timedelta(minutes=30) #set limit for user
        request.data['exp'] = time_limit
        payload = request.data
        token = jwt.encode(payload,"SECRET_KEY").decode('UTF-8')
        return JsonResponse({'token':token,'data':data_str}, safe=False)




@api_view(['GET','POST'])
def get_user_level(request):
    print(request.data)
    param = request.data
    user = mongo_driver.get_user_level(param)

    return JsonResponse({'msg':user}, safe=False)
