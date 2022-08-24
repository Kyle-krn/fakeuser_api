from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views import generic
from . import serialzers
from . import utils
from rest_framework import status

class TemplateView(generic.TemplateView):
    template_name = "password.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@api_view(['POST'])
def hello_world(request):
    serializer = serialzers.PasswordInputSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        data = serializer.data
        password = utils.generate_password(length=data["password_length"],
                                easy_to_read=data["easy_to_read"],
                                characters=data["characters"])
        resp = Response({"password": password}, status=status.HTTP_200_OK)
        
        
    else:
        resp = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    resp['Access-Control-Allow-Origin'] = '*'
    return resp
