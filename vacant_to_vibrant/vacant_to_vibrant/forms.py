from django.forms import ModelForm

from recaptcha_works.fields import RecaptchaField


class CaptchaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CaptchaForm, self).__init__(*args, **kwargs)

        # if not logged in, add recaptcha. else, do nothing.
        if not user or user.is_anonymous():
            self.fields['recaptcha'] = RecaptchaField(label="Prove you're human")
