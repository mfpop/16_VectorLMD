from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class ContactForm(forms.Form):
    """Form for handling contact submissions."""

    name = forms.CharField(
        label="Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Your name"}),
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "your.email@example.com"}),
    )

    subject = forms.CharField(
        label="Subject",
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "What is this regarding?"}),
    )

    message = forms.CharField(
        label="Message",
        required=True,
        widget=forms.Textarea(
            attrs={"placeholder": "Please describe how we can help you...", "rows": 4}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "space-y-4"

        # Style all form fields with improved visibility and accessibility
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "w-full px-3 py-2 bg-white border border-blue-500 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 z-20"
                }
            )

        self.helper.layout = Layout(
            Field("name"),
            Field("email"),
            Field("subject"),
            Field("message", rows=4),
        )
