from flask import Blueprint, render_template, redirect, url_for, g, request, flash
from flaskr.db import get_db
from flaskr.weather_api_request import get_weather

bp = Blueprint('weather', __name__)


@bp.route("/index", methods=('GET', 'POST'))
def index():
    db = get_db()
    user_cities_data = db.execute(
        "SELECT cities_ids FROM records WHERE user_id = ?",
        (g.user['id'],)
    ).fetchone()
    data = []
    if user_cities_data:
        ids = str((user_cities_data[0][1:-1])).replace('\'', '')
        cities_data = db.execute(
            "SELECT * FROM cities WHERE id in (" + ids + ") "
        ).fetchall()
        for row in cities_data:
            data.append([row[1], get_weather(row[1])])
    return render_template('weather/index.html', columns=['City', 'Temperature, C'], items=data)


@bp.route("/saveSelected", methods=['POST'])
def save_selected_cities():
    cities_ids = request.form.getlist('check')
    db = get_db()
    record = db.execute(
        'SELECT * FROM records WHERE id = ?', (g.user['id'],)
    ).fetchone()
    if record is None:
        db.execute(
            'INSERT INTO records (user_id, cities_ids) VALUES (?, ?)',
            (g.user['id'], str(cities_ids))
        )
    else:
        db.execute(
            'UPDATE records SET cities_ids = ? where user_id = ?',
            (str(cities_ids), g.user['id'])
        )
    db.commit()
    return redirect(url_for('weather.index'))


@bp.route("/selectCities", methods=('GET', 'POST'))
def load_select_cities():
    db = get_db()
    all_cities_data = db.execute(
        "SELECT * FROM cities"
    ).fetchall()
    selected = db.execute(
        "SELECT cities_ids FROM records WHERE user_id = ?",
        (g.user['id'],)
    ).fetchone()
    db.commit()
    if selected:
        return render_template("weather/selectCities.html", names=['ID', 'City'],
                               items=all_cities_data, cities_checked=selected[0])
    else:
        return render_template("weather/selectCities.html", names=['ID', 'City'],
                               items=all_cities_data, cities_checked=[])


@bp.route('/adminDashboard', methods=('GET', 'POST'))
def load_admin_dashboard():
    db = get_db()
    data = db.execute(
        "SELECT * FROM cities"
    ).fetchall()
    db.commit()
    return render_template('weather/adminDashboard.html', columns=['ID', 'City'], items=data)


@bp.route('/addCity', methods=['POST'])
def add_city():
    db = get_db()
    error = None
    if request.method == 'POST':
        city = request.form['addCity']
        if db.execute(
                'SELECT id FROM cities WHERE city = ?', (city,)
        ).fetchone() is not None:
            error = 'City {} is already added.'.format(city)

        if error is None:
            db.execute(
                'INSERT INTO cities (city) VALUES (?)', (city,)
            )
            db.commit()
            return redirect(url_for('weather.load_admin_dashboard'))
        flash(error)

    return redirect(url_for('weather.load_admin_dashboard'))


@bp.route('/deleteCity', methods=['POST'])
def delete_city():
    error = None
    if request.method == 'POST':
        db = get_db()
        city_id = request.form['deleteCity']
        if db.execute(
                'SELECT id FROM cities nolock WHERE id = ?', (city_id,)
        ).fetchone() is not None:
            db.execute(
                'DELETE FROM cities WHERE id = ?', (city_id,)
            )
            db.commit()
            return redirect(url_for('weather.load_admin_dashboard'))
        error = 'Wrong city ID'
        flash(error)
    return redirect(url_for('weather.load_admin_dashboard'))


'''@socketio.on('modify_database')
def database_modified(data):
    print('data sent')
    emit('Database modified', data, broadcast=True)'''
