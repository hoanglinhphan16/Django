from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models.question import Question
from .models.choice import Choice
from .form import *

'''
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


# Create your views here.

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
'''


@login_required(login_url='/accounts/login/')
@permission_required('polls.view_choice')
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


class IndexView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    login_url = '/login/'
    permission_required = 'polls.view_choice'
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


'''
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
'''


@login_required(login_url='/accounts/login/')
@permission_required('polls.view_choice')
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


'''
def upload(request):
    if request.method == 'POST':
        student = StudentForm(request.POST, request.FILES)
        if student.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse("File uploaded successfuly")
    else:
        student = StudentForm()
        return render(request, "polls/upload.html", {'form': student})
'''


class Upload(FormView):
    form_class = StudentForm
    template_name = 'polls/upload.html'
    success_url = reversed('.polls')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            for x in request.FILES.getlist('file_filed'):
                def process(f):
                    with open('polls/static/upload/' + str(x), 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)

                process(x)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
