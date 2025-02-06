import re
from django.core.exceptions import ValidationError

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        if not any(char.isdigit() for char in password):  
            raise ValidationError("Password must contain at least one digit.")

        if not any(char.islower() for char in password):  
            raise ValidationError("Password must contain at least one lowercase letter.")

        if not any(char.isupper() for char in password):  
            raise ValidationError("Password should ideally contain at least one uppercase letter for better security.")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):  
            raise ValidationError("Consider adding a special character (!@#$%^&* etc.) for extra security.")

    def get_help_text(self):
        return "Your password should be at least 8 characters long, contain at least one number, one lowercase letter, and ideally one uppercase letter or special character for better security."
