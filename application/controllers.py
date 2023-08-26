
from flask import Flask, render_template,redirect,request,session,flash
from flask import current_app as app
from flask_login import login_required, login_user, logout_user, current_user
# app.secret_key='here'
from application.models import *
@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        name=request.form.get("username")
        passw=request.form.get("password")
        quer=User.query.filter_by(username=name).first()
        if quer is not None and quer.password==passw:
            login_user(quer,remember=name)
            return redirect('/dash')
        else:
            flash('incorrect credentials')
            
    return render_template("login.html",entry='User')
        

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        name=request.form.get("username")
        passw=request.form.get("password")
        if name is not None and passw is not None:
            quer=User(username=name,password=passw)
            db.session.add(quer)
            db.session.commit()
            return redirect('/')
        else:
            flash('enter username and password')
    return render_template("register.html")
    
@app.route('/admin',methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        name=request.form.get("username")
        passw=request.form.get("password")
        quer=Admin.query.filter_by(username=name).first()
        if quer is not None and quer.password==passw:
            return redirect('/home')
    return render_template("login.html",entry='Admin')


@app.route('/home',methods=['GET','POST'])

def home():
    ren={}
    
    category=Category.query.all()
    for cat in category:
        products = Product.query.filter_by(cat_id=cat.cat_id).all()
        ren[cat.cat_name]=products
    return render_template("index.html",ren=ren)

@app.route('/category',methods=['GET','POST'])
def cat():
    if request.method == 'POST':
        product_name = request.form.get("productName")
        entry= Category(cat_name=product_name)
        db.session.add(entry)
        db.session.commit()
        

        return redirect('/home')
    return render_template("createcat.html")

@app.route('/reg/<string:name>',methods=['GET','POST'])
def reg(name):
    if request.method == 'POST':
        cat_id=(Category.query.filter_by(cat_name=name).first()).cat_id
        name = request.form.get("productName")
        unit=request.form.get("unit")
        rate=request.form.get("rate")
        quantity=request.form.get("quantity")
        if name.isalpha():
            entry= Product(cat_id=cat_id,name=name,unit=unit,rate=rate,quantity=quantity)
            db.session.add(entry)
            db.session.commit()
        else:
            flash('check the format')
            

        return redirect('/home')
    return render_template("adminreg.html")


@app.route('/reg/delete/<string:name>',methods=['GET','POST'])
def delc(name):
    quer=Category.query.filter_by(cat_name=name).first()
    db.session.delete(quer)
    db.session.commit()
    return redirect('/home')


@app.route('/pro/delete/<int:pid>',methods=['GET','POST'])
def delp(pid):
    if pid is not None:
        quer=Product.query.filter_by(prod_id=pid).first()
        db.session.delete(quer)
        db.session.commit()
    return redirect('/home')
@app.route('/pro/edit/<int:pid>',methods=['GET','POST'])
def pedit(pid):
    if request.method=='POST':
        query=Product.query.filter_by(prod_id=pid).first()
        if query is not None:
            query.name = request.form.get("productName")
            query.unit=request.form.get("unit")
            query.rate=request.form.get("rate")
            query.quantity=request.form.get("quantity")
            db.session.commit()
        return redirect('/home')
    return render_template('editpro.html',pro=Product.query.filter_by(prod_id=pid).first())

@app.route('/cat/edit/<string:name>',methods=['GET','POST'])
def cedit(name):
    if request.method == 'POST':
        quer=Category.query.filter_by(cat_name=name).first()
        quer.cat_name = request.form.get("productName")
        
        
        db.session.commit()
        return redirect('/home')
    return render_template('createcat.html')
@app.route('/dash',methods=['GET','POST'])
@login_required
def dash():
    ren={}
    category=Category.query.all()
    for cat in category:
        products = Product.query.filter_by(cat_id=cat.cat_id).all()
        ren[cat.cat_name]=products
    return render_template("custdash.html",ren=ren)

@app.route('/add/<int:pid>',methods=['GET','POST'])
def add(pid):
    if 'cart' not in session:
        session['cart']={}
        
    coun=(request.form.get('quantity'))
    if pid not in session['cart']:
        session['cart'][pid]=int(coun)
    else:
        session['cart'][pid]+=int(coun)
    print(session['cart'])
    flash('Added to Cart')
    return redirect('/dash')

@app.route("/cart")
@login_required
def view_cart():
    cart_items = {}
    
    total_cost = 0

    if 'cart' in session:
        for item,coun in session['cart'].items():
            print(item)
            pro=Product.query.filter_by(prod_id=item).first()
            cart_items[pro]=(coun)
            
        print(cart_items)
        total_cost = sum(item.rate*int(quan) for item,quan in cart_items.items())
       

    return render_template("cart.html", cart_items=cart_items,total_cost=total_cost)
@app.route('/checkout')
@login_required
def check():
    
    for item,coun in session['cart'].items():
        pro=Product.query.filter_by(prod_id=item).first()
        flag=False
        if pro.quantity>=coun:
            pro.quantity-=coun
            db.session.commit()
            flag=True
            flash('Action completed successfully!', 'success')
        else:
            flag=False
            flash(pro.name+' out of stock')
            break
        if flag and 'cart' in session:
            session.pop('cart')
    return redirect("/cart")

@app.route('/search',methods=['GET','POST'])
@login_required
def search():
    if request.method=='POST':
        name=request.form.get('name')
        plist=Product.query.filter_by(name=name).all()
        rlist=Product.query.filter_by(rate=name).all()
        clist=Category.query.filter_by(cat_name=name).all()
        


        ren={}
        if clist is not None:
            for cat in clist:
                products = Product.query.filter_by(cat_id=cat.cat_id).all()
                ren[cat.cat_name]=products

        if plist is not None:
            for pro in plist:
                cat=Category.query.filter_by(cat_id=pro.cat_id).first()
                if cat.cat_name not in ren:
                    ren[cat.cat_name]=[pro]
                else:
                    ren[cat.cat_name].append(pro)
        if rlist is not None:
            for pro in rlist:
                cat=Category.query.filter_by(cat_id=pro.cat_id).first()
                if cat.cat_name not in ren:
                    ren[cat.cat_name]=[pro]
                else:
                    ren[cat.cat_name].append(pro)
        if clist or plist or rlist:
            flash('Product found!')
            return render_template("custdash.html",ren=ren)
        else:
            flash('Product not found!')


    return redirect('/dash')

@app.route('/logout')
@login_required
def logout():
    if 'cart' in session:
        session.pop('cart')
    logout_user()
    return redirect('/')

@app.route('/buy/<int:pid>')
@login_required
def buy(pid):
    pro=Product.query.filter_by(prod_id=pid).first()

    return render_template("buy.html",pro=pro)

@app.route('/remove/<int:pro>')
@login_required
def remove(pro):
    session['cart'].pop(pro)
    return redirect('/cart')
    