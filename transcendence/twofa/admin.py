from django.contrib import admin
from django import forms
from django_otp.plugins.otp_totp.models import TOTPDevice

from .models import UserProfile, TwilioSMSDevice, EmailOTPDevice

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'chosen_2fa_method']
        
    def clean(self):
        cleaned_data = super().clean()
        chosen_2fa_method = cleaned_data.get("chosen_2fa_method")
        if chosen_2fa_method and chosen_2fa_method != '----':
            if chosen_2fa_method == 'sms' and not TwilioSMSDevice.objects.filter(user=self.instance.user).exists():
                self.add_error('chosen_2fa_method', 'TwilioSMSDevice is required for SMS 2FA method.')
            elif chosen_2fa_method == 'email' and not EmailOTPDevice.objects.filter(user=self.instance.user).exists():
                self.add_error('chosen_2fa_method', 'EmailOTPDevice is required for Email 2FA method.')
            elif chosen_2fa_method == 'qr' and not TOTPDevice.objects.filter(user=self.instance.user).exists():
                self.add_error('chosen_2fa_method', 'TOTPDevice is required for QR code 2FA method.')
        return cleaned_data

class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileForm
    list_display = ('user', 'chosen_2fa_method')

class EmailOTPDeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'confirmed', 'key')
    search_fields = ('user__username', 'user__email')

class TwilioSMSDeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'confirmed', 'key')
    search_fields = ('user__username', 'phone_number')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(TwilioSMSDevice, TwilioSMSDeviceAdmin)
admin.site.register(EmailOTPDevice, EmailOTPDeviceAdmin)
