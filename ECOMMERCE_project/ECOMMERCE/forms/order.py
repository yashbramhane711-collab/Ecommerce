from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional
# forms/order.py
from flask_wtf import FlaskForm
from wtforms import SubmitField

class DeleteOrderForm(FlaskForm):
    submit = SubmitField('Delete Order')

class CheckoutForm(FlaskForm):
    # existing fields...
    pass


class CheckoutForm(FlaskForm):
    """Form for checkout process - collecting shipping and payment information"""
    
    # Shipping information
    shipping_full_name = StringField('Full Name', validators=[
        DataRequired(), 
        Length(min=2, max=100, message='Name must be between 2 and 100 characters')
    ])
    
    shipping_address = StringField('Address', validators=[
        DataRequired(), 
        Length(min=5, max=200, message='Address must be between 5 and 200 characters')
    ])
    
    shipping_city = StringField('City', validators=[
        DataRequired(), 
        Length(min=2, max=100, message='City must be between 2 and 100 characters')
    ])
    
    shipping_state = StringField('State/Province', validators=[
        DataRequired(), 
        Length(min=2, max=100, message='State must be between 2 and 100 characters')
    ])
    
    shipping_zipcode = StringField('Zip/Postal Code', validators=[
        DataRequired(), 
        Length(min=3, max=20, message='Zip code must be between 3 and 20 characters')
    ])
    
    shipping_country = StringField('Country', validators=[
        DataRequired(), 
        Length(min=2, max=100, message='Country must be between 2 and 100 characters')
    ])
    
    # Contact information
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(message='Please enter a valid email address')
    ])
    
    phone = StringField('Phone', validators=[
        DataRequired(), 
        Length(min=10, max=20, message='Phone number must be between 10 and 20 characters')
    ])
    
    # Payment method
    payment_method = SelectField('Payment Method', choices=[
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash_on_delivery', 'Cash on Delivery')
    ], validators=[DataRequired()])
    
    # Additional notes (optional)
    notes = TextAreaField('Order Notes', validators=[
        Optional(), 
        Length(max=500, message='Notes cannot exceed 500 characters')
    ])
    
    submit = SubmitField('Place Order')


class OrderStatusForm(FlaskForm):
    """Form for admin to update order status"""
    
    status = SelectField('Order Status', choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded')
    ], validators=[DataRequired()])
    
    tracking_number = StringField('Tracking Number', validators=[
        Optional(),
        Length(max=50, message='Tracking number cannot exceed 50 characters')
    ])
    
    admin_notes = TextAreaField('Admin Notes', validators=[
        Optional(),
        Length(max=500, message='Notes cannot exceed 500 characters')
    ])
    
    submit = SubmitField('Update Status')


class OrderNoteForm(FlaskForm):
    """Simple form for adding notes to orders"""
    
    notes = TextAreaField('Add Note', validators=[
        DataRequired(),
        Length(min=1, max=500, message='Note must be between 1 and 500 characters')
    ])
    
    submit = SubmitField('Add Note')


# Optional: Form for order filtering/searching
class OrderFilterForm(FlaskForm):
    """Form for filtering orders in admin panel"""
    
    status = SelectField('Status', choices=[
        ('', 'All Statuses'),
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], validators=[Optional()])
    
    date_from = StringField('From Date', validators=[Optional()])
    date_to = StringField('To Date', validators=[Optional()])
    
    submit = SubmitField('Filter Orders')