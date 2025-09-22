from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from forms.product import ProductForm
from models.product import Product
from extensions import db

product_bp = Blueprint('product', __name__)

@product_bp.route('/')
def product_list():
    page = request.args.get('page', 1, type=int)
    products = Product.query.paginate(page=page, per_page=9)
    return render_template('product/list.html', products=products)

@product_bp.route('/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product/detail.html', product=product)

@product_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('product.product_list'))
    
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            category=form.category.data,
            image=form.image.data or None
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('product.product_list'))
    
    return render_template('product/form.html', form=form, title='Add Product')

@product_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('product.product_list'))
    
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        product.category = form.category.data
        product.image = form.image.data or None
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('product.product_list'))
    
    return render_template('product/form.html', form=form, title='Edit Product')

@product_bp.route('/delete/<int:id>')
@login_required
def delete_product(id):
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('product.product_list'))
    
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('product.product_list'))

@product_bp.route('/search')
def search_products():
    query = request.args.get('q', '')
    if query:
        products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    else:
        products = Product.query.all()
    
    return render_template('product/search.html', products=products, query=query)