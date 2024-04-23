import mysql.connector
from flask import Flask, render_template, redirect, url_for, request, abort

app = Flask(__name__)

def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host="b09954e6654d",
            user="midtermizzetcemibik",
            password="12345Izo",
            database="19070001035_izzetcemibik_midtermdatabase"
        )
        if conn.is_connected():
            print('Connected to MySQL database')
        return conn

    except mysql.connector.Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

@app.route('/')
def home():
    conn = connect_to_mysql()
    if conn is None:
        abort(500)  
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT idSlider, text1Slider, text2Slider, imageSlider FROM slider")
        slider = cursor.fetchall()
        return render_template('home.html', slider=slider)
    except mysql.connector.Error as e:
        print(f"Error executing SQL query: {e}")
        abort(500)  
    finally:
        cursor.close()
        conn.close()  


@app.route('/products', methods=['GET', 'POST'])
def show_products():
    conn = connect_to_mysql()
    cursor = conn.cursor()

    if request.method == 'POST':
        search_text = request.form['search_text']
        query = f"SELECT MIN(idToys) AS idToys, topic, MIN(priceToys) AS priceToys, MIN(imageToys) AS imageToys FROM toys WHERE topic LIKE '%{search_text}%' GROUP BY topic"
    else:
        query = "SELECT MIN(idToys) AS idToys, topic, MIN(priceToys) AS priceToys, MIN(imageToys) AS imageToys FROM toys WHERE 1=1"

        yarinkapindaCheckbox = request.args.get('yarinkapindaCheckbox')
        if request.args.get('yarinkapindaCheckbox') == '1':
            query += " AND yarinkapindaToys = 1"
        elif request.args.get('yarinkapindaCheckbox') == '0':
            query += " AND (yarinkapindaToys = 0 OR yarinkapindaToys IS NULL)"

        location = request.args.get('locationSelect')
        if location:
            query += f" AND locationToys = '{location}'"

        query += " GROUP BY topic"  

    cursor.execute(query)
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/productdetails/<int:product_id>')
def product_details(product_id):
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query_product = f"SELECT idToys, topic, descriptionToys, priceToys, categoriesToys, colorToys, imageToys, productNo FROM toys WHERE idToys = {product_id}"
    cursor.execute(query_product)
    product = cursor.fetchone()

    if product is None:
        abort(404) 

    description = product[2]

    query_colors = f"SELECT colorToys, idToys, imageToys FROM toys WHERE descriptionToys = '{description}' AND idToys != {product_id}"  
    cursor.execute(query_colors)
    color_options = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('productdetails.html', product=product, color_options=color_options)

@app.route('/productdetails/<int:product_id>/<string:color>')
def product_details_color(product_id, color): #asdasdasda
    conn = connect_to_mysql()
    cursor = conn.cursor()

    query_product = f"SELECT idToys, topic, descriptionToys, priceToys, categoriesToys, colorToys, imageToys, productNo FROM toys WHERE idToys = {product_id} AND colorToys = '{color}'"
    cursor.execute(query_product)
    product = cursor.fetchone()

    if product is None:
        abort(404)  

    description = product[4]

    query_colors = f"SELECT colorToys, idToys, imageToys FROM toys WHERE descriptionToys = '{description}' AND idToys != {product_id}"
    cursor.execute(query_colors)
    color_options = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('productdetails.html', product=product, color_options=color_options)



if __name__ == "__main__":
    app.run(debug=True)