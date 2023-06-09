from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse ,  HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Question , Choice
from django.utils import timezone
from django.db.models import Count
# def index(request):
#     lates_question_list = Question.objects.all()
#     return render(request, "polls/index.html", {
#         "lates_question_list":lates_question_list
#     })


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})


# def result(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request , "polls/result.html", {"question": question})

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "lates_question_list"
    
    def get_queryset(self):
        """return the last five published question, that have at leat two choices"""
        question =  Question.objects.filter(pub_date__lte=timezone.now())
        question = question.alias(entries=Count("choice")).filter(entries__gte=2)
        return question.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """Excludes any question that arent published yet"""
        return Question.objects.filter(pub_date__lte=timezone.now())

    
class ResultlView(generic.DetailView):
    model = Question
    template_name = "polls/result.html"
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())   

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"]) 
    except (KeyError, Choice.DoesNotExist): 
        return render(request , "polls/datail.html", {
            "question": question,
            "error_message": "NO elegiste una respuesta"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:result", args=(question_id,)))