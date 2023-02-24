from django import forms

from users.models import UserMaster


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = UserMaster

        fields = ["email", "first_name", "last_name", "password"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter email",
                    "aria-invalid": "true",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter first name",
                    "aria-invalid": "true",
                    "required": "true"
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter last name",
                    "aria-invalid": "true",
                    "required": "true"
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter password",
                    "aria-invalid": "true",
                }
            ),
        }

    def save(self, commit=True):
        password = self.cleaned_data.get("password")
        instance = super(CreateUserForm, self).save(commit=False)
        instance.set_password(password)
        instance.save()
        return super(CreateUserForm, self).save(commit=commit)


class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"placeholder": "Email", "class": "form-control"}
        ),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        ),
    )
