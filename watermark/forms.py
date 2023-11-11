from django import forms


class WatermarkForm(forms.Form):
    video = forms.FileField()
    watermark_image = forms.ImageField()
    watermark_position = forms.ChoiceField(choices=[
        ('top-left', 'Top Left'),
        ('top-right', 'Top Right'),
        ('bottom-left', 'Bottom Left'),
        ('bottom-right', 'Bottom Right'),
        ('center', 'Center'),
    ])
    watermark_size = forms.IntegerField(min_value=1, initial=100, help_text="Width of the watermark in pixels.")
    padding = forms.IntegerField(min_value=0, initial=10, help_text="Padding from the edges in pixels.")

