from django.urls import path
from .views import * 

urlpatterns = [
    path("add-bank/",BankApi.as_view(),name="add-bank"),
    path("add-account/",AccountApi.as_view(),name="add-account"),
    path("login/",LoginView.as_view(),name="login"),
    path("update-bank/<int:id>/",BankApi.as_view(),name="update-bank"),
    path("update-account/<int:id>/",AccountApi.as_view(),name="update-account"),
    path("delete-bank/<int:id>/",BankApi.as_view(),name="delete-bank"),
    path("delete-account/<int:id>/",AccountApi.as_view(),name="delete-account"),
    path("create-user/",CreateUserView.as_view(),name="create-user"),
    path("update-user/<int:id>/",CreateUserView.as_view(),name="update-user"),
    path("verify-pan/",VerifyPan.as_view(),name="verify-pan"),
    path("transcation/",TransactionApi.as_view(),name="transcation"),
    path("statement/",Statement.as_view(),name="statement"),
    path("common/",CommonMessage.as_view(),name="common"),


]
