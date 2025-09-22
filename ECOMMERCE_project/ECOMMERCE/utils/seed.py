from extensions import db
from models.user import User
from models.product import Product

def seed_data():
    # Check if data already exists
    if User.query.count() == 0:
        # Create admin user
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create regular user
        user = User(username='john', email='john@example.com')
        user.set_password('password123')
        db.session.add(user)
        
        db.session.commit()
        print("Created sample users")
    
    if Product.query.count() == 0:
        # Sample products
        products = [
            Product(
                name="Wireless Headphones",
                description="High-quality wireless headphones with noise cancellation",
                price=199.99,
                stock=25,
                category="Electronics",
                image="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400"
            ),
            Product(
                name="Smartphone",
                description="Latest smartphone with advanced camera features",
                price=899.99,
                stock=15,
                category="Electronics",
                image="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400"
            ),
            Product(
                name="Cotton T-Shirt",
                description="Comfortable cotton t-shirt in various colors",
                price=24.99,
                stock=50,
                category="Clothing",
                image="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400"
            ),
            Product(
                name="Programming Book",
                description="Comprehensive guide to web development",
                price=49.99,
                stock=30,
                category="Books",
                image="https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400"
            ),
            Product(
                name="Coffee Maker",
                description="Automatic coffee maker with timer",
                price=79.99,
                stock=20,
                category="Home",
                image="https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400"
            ),
            Product(
                name="Running Shoes",
                description="Comfortable running shoes for all terrains",
                price=129.99,
                stock=35,
                category="Sports",
                image="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"
            ),
            Product(
                name="Laptop",
                description="High-performance laptop for work and gaming",
                price=1299.99,
                stock=10,
                category="Electronics",
                image="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400"
            ),
            Product(
                name="Water Bottle",
                description="Insulated water bottle keeps drinks cold for 24 hours",
                price=34.99,
                stock=40,
                category="Sports",
                image="https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400"
            )
        ]
        
        for product in products:
            db.session.add(product)
        
        db.session.commit()
        print("Created sample products")