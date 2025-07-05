from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clothing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)


# Clothing Item Model
class ClothingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<ClothingItem {self.name}>'

# Create the database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    items = ClothingItem.query.all()
    return render_template('index.html', items=items)

@app.route('/shop')
def shop():
    items = ClothingItem.query.all()
    return render_template('shop.html', items=items)

@app.route('/new-arrivals')
def new_arrivals():
    # In a real app, you might filter by date added
    new_items = ClothingItem.query.order_by(ClothingItem.id.desc()).limit(8).all()
    return render_template('new_arrivals.html', new_items=new_items)

@app.route('/sale')
def sale():
    # In a real app, you might have a sale flag in your database
    sale_items = ClothingItem.query.filter(ClothingItem.price < 50).all()
    return render_template('sale.html', sale_items=sale_items)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        image_url = request.form['image_url']
        category = request.form['category']
        
        new_item = ClothingItem(
            name=name,
            description=description,
            price=price,
            image_url=image_url,
            category=category
        )
        
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('add_item.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = ClothingItem.query.get_or_404(id)
    
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.price = float(request.form['price'])
        item.image_url = request.form['image_url']
        item.category = request.form['category']
        
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('edit_item.html', item=item)

@app.route('/delete/<int:id>')
def delete_item(id):
    item = ClothingItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

   


