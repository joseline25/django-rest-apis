from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from base.models import *
from .serializers import AdvocateSerializer, CompanySerializer
from django.shortcuts import render, redirect
from django.http import JsonResponse
# for class views
from rest_framework.views import APIView

# for permissions during authentication
from rest_framework.permissions import IsAuthenticated

# our endpoints for Advocate

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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
        # return redirect('advocates') # redirect to the name of the view we want
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
    # get a specific object
    def get_object(self, id):
        try:
            return Advocate.objects.get(id=id)
        except Advocate.DoesNotExist:
            raise JsonResponse('Advocate does not exist!')

    # method to get  the details of the object
    def get(self, request, id):
        # advocate = Advocate.objects.get(id=id)
        advocate = self.get_object(id)
        serializer = AdvocateSerializer(advocate, many=False)
        return Response(serializer.data)

    # method to update

    def put(self, request, id):
        # select the advocate
        # advocate = Advocate.objects.get(id=id)
        advocate = self.get_object(id)

        # update the fields of the selected advocate
        advocate.username = request.data['username']
        advocate.bio = request.data['bio']

        # serialize
        serializer = AdvocateSerializer(advocate, many=False)

        return Response(serializer.data)

    # method to delete
    def delete(self, request, id):
        # select the advocate
        # advocate = Advocate.objects.get(id=id) without the method get_object
        advocate = self.get_object(id)

        # delete the advocate
        advocate.delete()

        return Response('Advocate deleted')


# endpoints for Company

# list of Companies and post a company
@api_view(['GET', 'POST'])
def companies_list(request):
    if request.method == 'GET':
        # get the list of compnies querysets
        companies = Company.objects.all()
        # serialize by specifying that you serialize many
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        # create the object
        company = Company.objects.create(
            name=request.data['name'], bio=request.data['bio']
        )
        # serialize it by specifying that you only process one
        serializer = CompanySerializer(company, many=False)
        return Response(serializer.data)

# correct the POST in the class view


class CompanyList(APIView):

    # list of comapnies
    def get(self, request, format=None):
        """
        Return a list of all companies.
        """
        names = [company.name for company in Company.objects.all()]

        return Response(names)

    # post a company
    def post(self, request, id):
        """
        Post a new company       
        """

        # create a new company
        company = Company.objects.create(
            name=request.data['name'], bio=request.data['bio']
        )

        # serialize the new object
        serializer = CompanySerializer(advocate, many=False)

        return Response(serializer.data)


class CompanyDetails(APIView):
    # get a specific object
    def get_object(self, id):
        try:
            return Company.objects.get(id=id)
        except Company.DoesNotExist:
            raise JsonResponse('Company does not exist!')

    # get the details of a company

    def get(self, request, id):
        # get the company
        company = self.get_object(id)
        # serialize it
        serializer = CompanySerializer(company, many=False)
        return Response(serializer.data)

    # update a company's details
    def put(self, request, id):
        # get the company
        company = self.get_object(id)

        # update the fields
        company.name = request.data['name']
        company.bio = request.data['bio']
        
        # save the update
        company.save()

        # serialize it
        serializer = CompanySerializer(company, many=False)

        return Response(serializer.data)

    # delete a company
    def delete(self, request, id):
        # select the company
        company = self.get_object(id)

        # delete
        company.delete()
        return Response('Company deleted')
