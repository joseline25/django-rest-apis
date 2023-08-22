from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import *
from .serializers import AdvocateSerializer
from django.shortcuts import render, redirect
# for class views

from rest_framework.views import APIView

# our endpoints

# GET /advocates
# POST /advocates

# GET /advocates/:id
# PUT /advocates/:id (to update. We can also use PATCH but what is the difference?)
# DELETE /advocates/:id


@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})


@api_view(['GET'])
def endpoints(request):
    data = {"api's": ['/advocates', '/advocates/:username']}
    return Response(data)


# view for advocates note that we can have this ['GET', 'POST'] as argument of @api_view()
@api_view(['GET', 'POST'])
def advocate_list(request):
    if request.method == 'GET':
        # for queries
        # http://127.0.0.1:8000/api/advocates/?query=Jose returns Joseline
        # http://127.0.0.1:8000/api/advocates/?query=c returns Clovis
        query = request.GET.get('query')

        if query == None:
            query = ''

        # advocates = Advocate.objects.all().values()
        advocates = Advocate.objects.filter(username__icontains=query)
        # icontains, pour spécifier que c'est insensible à la casse
        serializer = AdvocateSerializer(advocates, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        advocate = Advocate.objects.create(
            username=request.data['username'], bio=request.data['bio']
        )
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)



# view for the details on an advocate from advocates
@api_view(['GET', 'PUT', 'DELETE'])
def advocate_details(request, id):
    # select an advocate based on the id
    advocate = Advocate.objects.get(id=id)
    
    # get the details of advocate
    if request.method == 'GET':
        serializer = AdvocateSerializer(advocate, many=False)
        # many ici est false car on va serialise une seul objet
        return Response(serializer.data)

    # update advocate
    if request.method == 'PUT':
        # update the fields of the selected advocate
        advocate.username = request.data['username']
        advocate.bio = request.data['bio']
        
        # save the updates
        advocate.save()
        
        # serialize the data for display with Json format
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)

    # delete advocate
    if request.method == 'DELETE':
        advocate.delete()
        #return redirect('advocates') # redirect to the name of the view we want
        return Response("Advocate deleted!")

# view to add an advocate object but it is also
# managed in the view to display the list of advocates


@api_view(['POST'])
def advocate_add(request):
    Advocate.objects.create(
        username=request.data['username']
    )
    return Response('added !!!')


# class based views as an alternative
# the advantage here is that you don't need to specify that it is a get or post or ... 
# request
# you just have to use the defined method of the class
# first of all, we will import 
# from rest_framework.views import APIView

class AdvocateDetails(APIView):
    # method to get 
    def get(self, request, id):
        return Response('username')