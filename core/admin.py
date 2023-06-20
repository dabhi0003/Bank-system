from django.contrib import admin
from .models import User,Bank,Account,Transaction
from django.contrib.admin import ModelAdmin
# Register your models here.



class UserAdmin(ModelAdmin):
        list_display = ('id', 'email', 'username', 'first_name', 'last_name' ,'profile_img','acivation_status')
        list_filter = ('is_superuser',)
        fieldsets = [
                (None, {'fields': ('email', 'password',)}),
                ('Personal info', {'fields': ('first_name', 'last_name', 'username','profile_img','acivation_status',)}),
                ('Permissions', {'fields': ('is_superuser',)}),
        ]

        add_fieldsets = (
                (None, {
                        'classes': ('wide',),
                        'fields': ( 'is_student','profile_img','acivation_status'),
                }),
        )
        search_fields = ('username',)
        ordering = ('id',)
        filter_horizontal = ()


admin.site.register(User, UserAdmin)

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ["ifsc_code", "state", "district", "branch", "name"][::-1]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["is_verified","balance","acc_number", "acc_type", "email", "pan_no", "phone", "address", "birth_date", "name", "bank"][::-1]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["time","amount_type", "amount", "account"][::-1]

