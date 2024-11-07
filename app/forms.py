from django import forms
from django.core.exceptions import ValidationError
from .models import Person, Payroll ,PersonReset
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import cv2
import pytesseract
from django.core.files.base import ContentFile
from io import BytesIO
from django.conf import settings
import os

# Define the required contents
required_contents = [
    "USALAMA WA RAIA SACCOS LTD",
    "FOMU YA KUJIUNGA KWENYE HUDUMA YA URA MOBILE",
    "Weka alama ya vyema kwenye aina ya huduma unayohitaji",
    "URA Mobile USSD",
    "URA Mobile App",
    "Majina ya Akaunti",
    "Jina la Kwanza",
    "Jina la Kati",
    "Jina la Mwisho",
    "Namba ya Uanachama",
    "Check No",
    "Namba ya simu",
    "Barua Pepe",
    "Sababu za kujiunga",
    "TAMKO LA MTEJA/MWANACHAMA",
    "Sahihi ya Mwanachama",
    "Tarehe",
    "Ninathibitisha kuwa, nimehakiki taarifa katika fomu hii dhidi ya taarifazilizohifadhiwa na URA Saccos Limited kwenye akaunti hiyo.",
    "Jina la Mwisho, (Kama yanavyosomeka kwenye vitambulisho vyako)",
    "(Itakayotumika katika huduma hii)",
    "Sababu za kujiunga:",
    "Kujiunga kwa mara ya kwanza",
    "Kubadili Namba ya Simu",
    "Kupotelewa na Simu",
    "Kusahau Namba ya Siri",
    "(Chagua iliyo sahihi)"
]

# Minimum percentage of required contents
MIN_PERCENTAGE = 0.035  # 3.5%

def validate_image(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Use Tesseract to extract text from the image
    text = pytesseract.image_to_string(img, lang='eng')

    # Split the extracted text into lines and normalize it
    extracted_lines = set(line.strip().lower() for line in text.split('\n') if line.strip())

    # Count the number of required contents present in the extracted lines
    matched_count = sum(1 for content in required_contents if content.lower() in extracted_lines)
    
    # Calculate the percentage of matched contents
    percentage_matched = matched_count / len(required_contents)

    # Check if the percentage matches the requirement
    is_valid = percentage_matched >= MIN_PERCENTAGE
    
    if not is_valid:
        message = (
            "The image could not be recognized, may not represent a valid URA Mobile Form, or may not be clearly visible."
        )
        return is_valid, percentage_matched * 100, message
    
    return is_valid, percentage_matched * 100, None

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['check_number', 'simu', 'image']  # Include image field

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

        # Set Bootstrap class and custom placeholders for each field
        self.fields['check_number'].widget.attrs['class'] = 'form-control'
        self.fields['check_number'].widget.attrs['placeholder'] = 'Check Number'

        self.fields['simu'].widget.attrs['class'] = 'form-control'
        self.fields['simu'].widget.attrs['placeholder'] = '0656******'

        # Image field customization for file upload
        self.fields['image'].widget.attrs['class'] = 'form-control-file'  # Bootstrap class for file input
        self.fields['image'].widget.attrs['accept'] = 'image/*,application/pdf'  # Accept image and PDF files

    def clean_simu(self):
        simu = self.cleaned_data.get('simu')

        # Validate phone number
        if simu:
            # Check if the phone number starts with '0' and is exactly 10 digits
            if not simu.startswith('0'):
                raise ValidationError("The phone number must start with '0'.")
            if not simu.isdigit() or len(simu) != 10:
                raise ValidationError("The phone number must be exactly 10 digits long.")
        
        return simu

    def clean_image(self):
     image = self.cleaned_data.get('image')

     if image:
        # Validate image file size (3 MB limit)
        if image.size > 3 * 1024 * 1024:  # 3 MB
            size_in_mb = round(image.size / (1024 * 1024), 2)
            raise ValidationError(f"The image file size should not exceed 3 MB. Your file size is {size_in_mb} MB.")
        
        # Validate image type
        if not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise ValidationError("Please upload an image in PNG, JPG, or JPEG format.")

        # Temporary save the uploaded image to validate its contents
        temp_image_path = f'{settings.MEDIA_ROOT}/{image.name}'  # Use settings.MEDIA_ROOT for the absolute path
        
        # Save the file temporarily to validate
        with open(temp_image_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # Validate image content using ML function
        valid, percentage, message = validate_image(temp_image_path)  # Pass the file path to the validation function
        if not valid:
            # Remove the temp file if validation fails
            os.remove(temp_image_path)
            raise ValidationError(message)

     return image


    def clean_check_number(self):
        check_number = self.cleaned_data.get('check_number')

        # Validate if check_number exists in Payroll model
        if not Payroll.objects.filter(checkNumber=check_number).exists():
            raise ValidationError(f"The check number does not exist")
               
        return check_number


class PersonFormReset(forms.ModelForm):
    class Meta:
        model = PersonReset
        fields = ['check_number', 'simu', 'image']  # Include image field

    def __init__(self, *args, **kwargs):
        super(PersonFormReset, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))

        # Set Bootstrap class and custom placeholders for each field
        self.fields['check_number'].widget.attrs['class'] = 'form-control bg-light'
        self.fields['check_number'].widget.attrs['placeholder'] = 'Check Number'

        self.fields['simu'].widget.attrs['class'] = 'form-control bg-light'
        self.fields['simu'].widget.attrs['placeholder'] = '0656******'

        # Image field customization for file upload
        self.fields['image'].widget.attrs['class'] = 'form-control-file'  # Bootstrap class for file input
        self.fields['image'].widget.attrs['accept'] = 'image/*,application/pdf'  # Accept image and PDF files

    def clean_simu(self):
        simu = self.cleaned_data.get('simu')

        # Validate phone number
        if simu:
            # Check if the phone number starts with '0' and is exactly 10 digits
            if not simu.startswith('0'):
                raise ValidationError("The phone number must start with '0'.")
            if not simu.isdigit() or len(simu) != 10:
                raise ValidationError("The phone number must be exactly 10 digits long.")
        
        return simu

    def clean_image(self):
     image = self.cleaned_data.get('image')

     if image:
        # Validate image file size (3 MB limit)
        if image.size > 3 * 1024 * 1024:  # 3 MB
            size_in_mb = round(image.size / (1024 * 1024), 2)
            raise ValidationError(f"The image file size should not exceed 3 MB. Your file size is {size_in_mb} MB.")
        
        # Validate image type
        if not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise ValidationError("Please upload an image in PNG, JPG, or JPEG format.")

        # Temporary save the uploaded image to validate its contents
        temp_image_path = f'{settings.MEDIA_ROOT}/{image.name}'  # Use settings.MEDIA_ROOT for the absolute path
        
        # Save the file temporarily to validate
        with open(temp_image_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # Validate image content using ML function
        valid, percentage, message = validate_image(temp_image_path)  # Pass the file path to the validation function
        if not valid:
            # Remove the temp file if validation fails
            os.remove(temp_image_path)
            raise ValidationError(message)

     return image

    def clean_check_number(self):
        check_number = self.cleaned_data.get('check_number')

        # Validate if check_number exists in Payroll model
        if not Payroll.objects.filter(checkNumber=check_number).exists():
            raise ValidationError(f"The check number does not exist")
               
        return check_number


class PersonStatusForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['status']


#message  or support



from .models import MessageLog
from crispy_forms.layout import Submit
 

class MessageLogForm(forms.ModelForm):
    message = forms.CharField(help_text='Maximum 500 words allowed.')

    class Meta:
        model = MessageLog
        fields = ['phone_number', 'message',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone_number

    def clean_message(self):
        message = self.cleaned_data.get('message')

        # Check if the message is not empty
        if not message.strip():  # Check if the message only contains spaces
            raise forms.ValidationError("Message cannot be empty.")
        
        # Check the word count of the message
        word_count = len(message.split())
        if word_count > 500:
            raise forms.ValidationError(f"Message is too long. It contains {word_count} words, but only 500 are allowed.")
        
        return message