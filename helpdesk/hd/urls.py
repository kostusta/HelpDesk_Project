from django.urls import path

from hd import views


urlpatterns = [
    path('', views.ClaimListView.as_view(), name='claims_list_page'),
    path('hd/<int:pk>', views.ClaimDetailView.as_view(), name='claim_detail'),
    path('hd/new', views.NewClaimView.as_view(), name='new_claim'),
    path('hd/edit/<int:pk>', views.EditClaimView.as_view(), name='edit_claim'),
    path('hd/delete/<int:pk>', views.ClaimDetailView.as_view(), name='claim_delete'),
    path('comment/<int:pk>/new', views.NewCommentView.as_view(), name='new_comment'),
]
