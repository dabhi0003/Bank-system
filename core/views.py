from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
import random
import string
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import generics
import csv
from django.core.mail import EmailMessage
from django.core.mail import send_mail



class CreateUserView(generics.GenericAPIView):                  
    serializer_class = UserSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.is_superuser :
            user = serializer.save()
            if request.data.get('is_staff'):
                user.is_staff = True
                user.save()
            if request.data.get('is_superuser'):
                user.is_superuser = True
                user.save()
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
            })
        else:
            return Response("Only admin can create user...",400)
        
    def get(self,request):
        user=User.objects.all()
        serializer=UserSerializer(instance=user,many=True)
        return Response(serializer.data)
    
    def put(self,request,id):
        user = User.objects.get(id=id)
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return Response("Success")
        except User.DoesNotExist:
            return Response("User not found")    

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    token_class = RefreshToken
    def validate(self, attrs):
        data = super().validate(attrs)
        expiration_time = datetime.now() + timedelta(minutes=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data

class BankApi(APIView):
    def post(self,request):
        if request.user.is_superuser:
            serilizer_class=BankSerializer(data=request.data)
            print(request.data)
            if serilizer_class.is_valid():
                serilizer_class.save()
                return Response(serilizer_class.data,200)
            else:
                return Response(serilizer_class.error_messages,400)
        else:
            return Response("Only Superuser can add a bank")

    def get(self,reqeust):
        if reqeust.user.is_superuser:
            bank=Bank.objects.all()
            serilizer=BankSerializer(instance=bank,many=True)
            return Response(serilizer.data)
        else:
            return Response("Only super user can show bank..")
        

    def put(self,request,id):
        if request.user.is_superuser:
            try:
                bank=Bank.objects.get(id=id)
                serilizer=UpdateBankSerializers(data=request.data, instance=bank, partial=True)
                if serilizer.is_valid():
                    serilizer.save()
                    return Response(serilizer.data,200) 
            except Bank.DoesNotExist:
                return Response("Bank not found")
        else:
            return Response("Only super user can update bank details.")
        
    def delete(self, request, id):
        if request.user.is_superuser:
            try:
                bank = Bank.objects.get(id=id)
                bank.delete()
                return Response("Success")
            except Bank.DoesNotExist:
                return Response("Bank not found")    
        else:
            return Response("Only super user can delete a bank.")

class AccountApi(APIView):
    def post(self,request):
        if request.user.is_superuser:
            serilizer_class=AccountSerializer(data=request.data)
            if serilizer_class.is_valid():
                N = 16
                first_four_digits = "2066"
                remaining_digits = ''.join(random.choices(string.digits, k=N - len(first_four_digits)))
                acc_no = first_four_digits + remaining_digits
                serilizer_class.save(acc_number=acc_no)
                email_subject = 'Account Details'
                email_body = f"Your Account is Created Successfully, Your Account No is: {acc_no}"
                email = EmailMessage(email_subject, email_body,from_email=settings.EMAIL_HOST_USER, to=[request.data['email']])
                email.send()
                return Response(f"Your Account is Created Succesfully,Your Account No is:{acc_no}")
            else:
                return Response(serilizer_class.error_messages,400)
        else:
            return Response("only superuser can add Account Details.")
   
    def get(self,reqeust):
        if reqeust.user.is_superuser:
            bank=Account.objects.all()
            serilizer=AccountSerializer(instance=bank,many=True)
            return Response(serilizer.data)
        else:
            return Response("Only super user can show the Account Details.")
        

    def put(self,request,id):
        if  request.user.is_superuser:
            try:
                bank=Account.objects.get(id=id)
                serilizer=UpdateAccountSerializers(data=request.data, instance=bank, partial=True)
                if serilizer.is_valid():
                    serilizer.save()
                    return Response(serilizer.data,200) 
            except Bank.DoesNotExist:
                return Response("Account not found")
        else:
            return Response("only superuser can update a account details..")
        
    def delete(self, request, id):
        if request.user.is_superuser:
            try:
                account = Account.objects.get(id=id)
                account.delete()
                return Response("Success")
            except Account.DoesNotExist:
                return Response("Account not found") 
        else:
            return Response("only superuser can delete account..")

class VerifyPan(APIView):
    def post(self, request):
        pan_number = request.data.get('pan_no')
        account_number = request.data.get('account_number')
        
        try:
            account = Account.objects.get(acc_number=account_number)
            if account.acc_number == account_number:
                csv_file_path = '/home/sumitdabhi/Downloads/pan_no.csv'
                with open(csv_file_path, 'r') as file:
                  reader = csv.reader(file)
                  for row in reader:
                      if row[0] == pan_number:
                        account.is_verified = True
                        account.save()
                        return Response({'valid': True})
                      else:
                          return Response({'valid':False,'message':'pan number is not register..'})
            else:
                return Response({'valid': False, 'message': 'Invalid name'})
        except Account.DoesNotExist:
            return Response({'valid': False, 'message': 'Invalid PAN number'})

class TransactionApi(APIView):
    def post(self,request):
        serializer=TrancationSerializer(data=request.data)
        if serializer.is_valid():
            acc_number = serializer.validated_data['account']
            amount = serializer.validated_data['amount']
            amount_type=serializer.validated_data['amount_type']
            try:
                account = Account.objects.get(acc_number=acc_number)
                balance = account.balance

                if amount_type == "credit":
                    new_balance = int(balance) + int(amount)
                    account.balance = new_balance
                else:
                    if int(amount) > int(balance):
                        return Response(f"Sorry, your balance is: {balance}")
                    else:
                        new_balance = int(balance) - int(amount)
                        account.balance = new_balance
                account.save()     
            except:
                return Response("Account Doesn't Exit...please check Account number")
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.error_messages)
        
class Statement(APIView):
    def post(self, request):
        account_number = request.data.get('account')
        if not account_number or len(account_number) != 16 or not account_number.isdigit():
            return Response({'message': 'Invalid account number. Please enter a 16-digit number.'})
        transactions = Transaction.objects.filter(account=account_number)
        if not transactions:
            return Response({'message': 'No transactions for this account'})
        response = HttpResponse(content_type='statement/csv')
        response['Content-Disposition'] = 'attachment; filename="file.csv"'
        fieldnames = [ 'account', 'amount', 'amount_type','time']
        writer = csv.DictWriter(response, fieldnames=fieldnames)
        writer.writeheader()
        for transaction in transactions:
            writer.writerow({
                'account': transaction.account,
                'amount': transaction.amount,
                'amount_type': transaction.amount_type,
                'time':transaction.time
            })
        return response

class CommonMessage(APIView):
    def post(self,request):
        message=request.data.get('message')
        emails = Account.objects.values_list('email', flat=True)
        print(emails)
        for email in emails:
            email1 = EmailMessage(subject=message,from_email=settings.EMAIL_HOST_USER, to=[email])
            email1.send()
        return Response(message)
    