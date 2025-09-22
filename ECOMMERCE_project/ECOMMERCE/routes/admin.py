from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.user import User
from models.product import Product
from models.order import Order, OrderItem
from extensions import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@login_required
def require_admin():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))

@admin_bp.route('/')
def dashboard():
    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    
    # Get recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_users=total_users,
                         total_products=total_products,
                         total_orders=total_orders,
                         recent_orders=recent_orders)

@admin_bp.route('/users')
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/products')
def products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@admin_bp.route('/orders')
def orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@admin_bp.route('/reports')
def reports():
    # Basic sales report
    total_sales = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    total_orders_count = Order.query.count()
    avg_order_value = total_sales / total_orders_count if total_orders_count > 0 else 0
    
    # Most popular products
    popular_products = db.session.query(
        Product, db.func.sum(OrderItem.quantity).label('total_sold')
    ).join(OrderItem).group_by(Product.id).order_by(db.desc('total_sold')).limit(5).all()
    
    return render_template('admin/reports.html',
                         total_sales=total_sales,
                         total_orders_count=total_orders_count,
                         avg_order_value=avg_order_value,
                         popular_products=popular_products)