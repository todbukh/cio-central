from django import forms


class PollCreateForm(forms.Form):
    question = forms.CharField(
        max_length=200,
        required=True,
        error_messages={
            "required": "Poll question is required.",
            "max_length": "Poll question cannot exceed 200 characters.",
        },
    )
    option_1 = forms.CharField(max_length=100, required=True, label="Option 1")
    option_2 = forms.CharField(max_length=100, required=True, label="Option 2")
    option_3 = forms.CharField(max_length=100, required=False, label="Option 3")
    option_4 = forms.CharField(max_length=100, required=False, label="Option 4")

    def clean(self):
        cleaned_data = super().clean()
        options = []

        for field_name in ("option_1", "option_2", "option_3", "option_4"):
            value = (cleaned_data.get(field_name) or "").strip()
            if value:
                options.append(value)
                cleaned_data[field_name] = value

        if len(options) < 2:
            raise forms.ValidationError("Polls must have at least two options.")

        if len(options) != len(set(options)):
            raise forms.ValidationError("Poll options must be distinct.")

        cleaned_data["options"] = options
        return cleaned_data

    def get_options(self):
        return self.cleaned_data["options"]


class PollVoteForm(forms.Form):
    option = forms.ChoiceField(widget=forms.RadioSelect, required=True)

    def __init__(self, poll, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.poll = poll
        self.option_map = {str(option.id): option for option in poll.options.all()}
        self.fields["option"].choices = [
            (str(option.id), option.text)
            for option in poll.options.all()
        ]

    def clean_option(self):
        option_id = self.cleaned_data["option"]
        option = self.option_map.get(option_id)
        if option is None:
            raise forms.ValidationError("Select a valid option.")
        return option
