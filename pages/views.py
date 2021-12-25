from django.forms.forms import Form
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, FormView
from django.contrib import messages

from .forms import ContactForm
from .models import Contact
import json
    
class JsonableResponseMixin:
    """
    Mixin to add JSON support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    
    # def form_invalid(self, form):
    #     response = super().form_invalid(form)
    #     if self.request.accepts('text/html'):
    #         return response
    #     else:
    #         return JsonResponse(form.errors, status=400)

    # def form_valid(self, form):
    #     # We make sure to call the parent's form_valid() method because
    #     # it might do some processing (in the case of CreateView, it will
    #     # call form.save() for example).
    #     response = super().form_valid(form)
    #     if self.request.accepts('text/html'):
    #         return response
    #     else:
    #         data = {
    #             'pk': self.object.pk,
    #         }
    #         return JsonResponse(data)
        
class HomePageView(JsonableResponseMixin, CreateView):
    template_name = 'home.html'
    form_class = ContactForm
    # success_url = reverse_lazy('pages:home')
    
    # def get_success_url(self):
    #     return reverse('pages:home')

# class HomePageView(CreateView):
#     template_name = 'home.html'
#     form_class = ContactForm


def SubmitContact(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            contact_data = data.get('payload')
            Contact.objects.create(
               name = contact_data['name'],
               subject = contact_data['subject'],
               email = contact_data['email'],
               message = contact_data['message'],
            )
            messages.success(request, 'Contact Submitted!')
            return JsonResponse({'status': 'Contact Submitted!'})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')
    
    