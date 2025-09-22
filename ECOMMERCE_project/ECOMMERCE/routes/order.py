from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.order import Order, OrderItem
from models.cart import CartItem
from models.product import Product
from extensions import db
from datetime import datetime

order_bp = Blueprint('order', __name__)

@order_bp.route('/place', methods=['POST'])
@login_required
def place_order():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('cart.view_cart'))
    
    # Calculate total amount
    total_amount = 0
    for item in cart_items:
        product = Product.query.get(item.product_id)
        total_amount += product.price * item.quantity
    
    # Create order
    order = Order(user_id=current_user.id, total_amount=total_amount)
    db.session.add(order)
    db.session.flush()  # Get the order ID
    
    # Create order items
    for item in cart_items:
        product = Product.query.get(item.product_id)
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price
        )
        db.session.add(order_item)
        
        # Update product stock
        product.stock -= item.quantity
    
    # Clear cart
    CartItem.query.filter_by(user_id=current_user.id).delete()
    
    db.session.commit()
    flash('Order placed successfully!', 'success')
    return redirect(url_for('order.order_detail', order_id=order.id))

@order_bp.route('/history')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('order/history.html', orders=orders)

@order_bp.route('/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('You cannot view this order.', 'danger')
        return redirect(url_for('order.order_history'))
    
    # Get order items with product details
    order_items = []
    for item in order.order_items:
        product = Product.query.get(item.product_id)
        order_items.append({
            'product': product,
            'quantity': item.quantity,
            'price': item.price,
            'subtotal': item.quantity * item.price
        })
    
    return render_template('order/detail.html', order=order, order_items=order_items)

