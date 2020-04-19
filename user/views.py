from rest_framework.viewsets import ViewSet
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from django.http import HttpResponse
from background_task import background
from .task import generate_pdf


def update_user_video_seen(request):
    category_question_id = request.GET.get('question_id')

    cq = CatalogQuestion.objects.filter(id=category_question_id).first()
    video_seen, created = DUSerVideoSeen.objects.get_or_create(seen_by=request.user, catalog_question=cq)    
    video_seen.save()

    #scheduling background task after 5 min 
    generate_pdf(video_seen_id,schedule=60*5)
    return Response({"message":"Succesfully updated"})

    


