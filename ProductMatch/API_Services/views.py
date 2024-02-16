from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .engine import *


class nav_history_latest(APIView):
    def get(self, request):

        userid = request.headers.get('user-id')
        if userid == None:
            return Response({"Error": "Missing userid parameter"}, status=status.HTTP_400_BAD_REQUEST)
        
        products = get_nav_history_latest(userid=userid)
        return Response({"user-id": userid, "products": products, "type": "personalized"}, status=status.HTTP_200_OK)
    
    def delete(self, request):

        userid = request.headers.get('user-id')
        if userid == None:
            return Response({"Error": "Missing userid parameter"}, status=status.HTTP_400_BAD_REQUEST)
        
        productid = request.headers.get('product-id')
        if productid == None:
            return Response({"Error": "Missing productid parameter"}, status=status.HTTP_400_BAD_REQUEST)
        
        delete_nav_history(userid=userid, productid=productid)
        return Response({"Message": "Transaction completed!"}, status=status.HTTP_200_OK)


class user_history_rec(APIView):
    def get(self, request):

        userid = request.headers.get('user-id')
        if userid == None:
            return Response({"Error": "Missing userid parameter"}, status=status.HTTP_400_BAD_REQUEST)

        top_10_products, personalized = history_recommendations(userid)
        return Response({"user-id": userid, "products": top_10_products, "type": personalized}, status=status.HTTP_200_OK)

