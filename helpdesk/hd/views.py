from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from hd import models as hd_models, forms
from hd.api.serializers import ClaimSerializer, ForAdminSerializer, ForUserSerializer
from hd.api.permissions import IsOwner, IsSuperUser


class ClaimListView(ListView):
    model = hd_models.ClaimModel
    template_name = 'hd/claims_list.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                qsetadmin = Q(status='PN') | Q(status='IP')
                return hd_models.ClaimModel.objects.filter(qsetadmin)
            else:
                return hd_models.ClaimModel.objects.filter(author=self.request.user)

    def post(self, request, *args, **kwargs):
        claim_id = request.POST.get('claim_id', '')
        claim = hd_models.ClaimModel.objects.get(pk=claim_id)
        if 'decline' in request.POST:
            claim.status = 'DC'
            claim.declined_status_count += 1
        elif 'done' in request.POST:
            claim.status = 'DN'
        elif 'confirm' in request.POST:
            claim.status = 'IP'
        else:
            claim.status = 'PN'
        claim.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ClaimDetailView(DetailView):
    model = hd_models.ClaimModel

    def post(self, request, *args, **kwargs):
        claim_id = request.POST.get('claim_id', '')
        claim = hd_models.ClaimModel.objects.get(pk=claim_id)
        if 'decline' in request.POST:
            claim.status = 'DC'
            claim.declined_status_count += 1
        elif 'done' in request.POST:
            claim.status = 'DN'
        elif 'confirm' in request.POST:
            claim.status = 'IP'
        else:
            claim.status = 'PN'
        claim.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class NewClaimView(CreateView):
    model = hd_models.ClaimModel
    form_class = forms.NewClaimForm
    success_url = reverse_lazy('claims_list_page')

    def form_valid(self, form):
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class EditClaimView(UpdateView):
    model = hd_models.ClaimModel
    form_class = forms.EditClaimForm
    success_url = reverse_lazy('claims_list_page')


class ClaimDeleteView(DeleteView):
    model = hd_models.ClaimModel
    success_url = reverse_lazy('claims_list_page')


class NewCommentView(CreateView):
    model = hd_models.CommentModel
    form_class = forms.CommentForm
    success_url = reverse_lazy('claims_list_page')

    def get_initial(self):
        initial = {'claim': self.kwargs.get('pk')}
        return initial

    def form_valid(self, form):
        self.object = form.save()
        self.object.author = self.request.user
        self.object.claim_id = form.initial.get('claim')
        self.object.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Invalid DATA')
        return super(NewCommentView, self).form_invalid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if self.request.user.is_staff:
                claim_id = self.kwargs.get('pk')
                claim = hd_models.ClaimModel.objects.get(pk=claim_id)
                claim.status = 'DC'
                claim.declined_status_count += 1
                claim.save()
            else:
                return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ClaimViewSet(ModelViewSet):
    # queryset = hd_models.ClaimModel.objects.all()
    # serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsSuperUser]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ForAdminSerializer
        return ForUserSerializer

    def get_queryset(self):
        priority = self.request.GET.get('priority', None)
        if priority:
            return hd_models.ClaimModel.objects.filter(priority=priority)
        else:
            return hd_models.ClaimModel.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if self.request.user.is_staff:
            admin_filter = Q(status='PN') | Q(status='IP')
            queryset = queryset.filter(admin_filter)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = queryset.filter(author=self.request.user)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author == self.request.user or self.request.user.is_superuser:
            serializer = self.get_serializer(instance)
        else:
            raise exceptions.PermissionDenied()
        return Response(serializer.data)
