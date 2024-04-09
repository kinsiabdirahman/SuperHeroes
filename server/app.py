from flask import Flask, jsonify, request
from models import db, Hero, Power, HeroPower
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def home():
    return "Code Challenge"



@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_list = [{
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name
    } for hero in heroes]
    return jsonify(heroes_list), 200



@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero is None:
        return jsonify({"error": "Hero not found"}), 404

    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "hero_powers": [{
            "id": hero_power.id,
            "strength": hero_power.strength,
            "power": {
                "id": hero_power.power.id,
                "name": hero_power.power.name,
                "description": hero_power.power.description
            }
        } for hero_power in hero.hero_powers.all()]  
    }

    return jsonify(hero_data), 200




@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_list = [{
        "id": power.id,
        "name": power.name,
        "description": power.description
    } for power in powers]
    return jsonify(powers_list), 200


@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({"error": "Power not found"}), 404
    power_data = {
        "id": power.id,
        "name": power.name,
        "description": power.description
    }
    return jsonify(power_data), 200



@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({"error": "Power not found"}), 404

    data = request.json  
    if 'description' not in data or len(data['description']) < 20:
        return jsonify({"errors": ["validation errors"]}), 400

    power.description = data['description']
    db.session.commit()

    power_data = {
        "id": power.id,
        "name": power.name,
        "description": power.description
    }
    return jsonify(power_data), 200  





@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json

    if 'hero_id' not in data or 'power_id' not in data:
        return jsonify({'error': 'hero_id and power_id are required'}), 400

    if 'strength' in data and data['strength'] not in ('Strong', 'Weak', 'Average'):
        return jsonify({'errors': ['validation errors']}), 400

    hero = Hero.query.get(data['hero_id'])
    power = Power.query.get(data['power_id'])

    if hero is None or power is None:
        return jsonify({'error': 'Hero or power not found'}), 404

    hero_power = HeroPower(
        strength=data.get('strength'),
        hero_id=data['hero_id'],
        power_id=data['power_id']
    )
    db.session.add(hero_power)
    db.session.commit()

    return jsonify({
        'id': hero_power.id,
        'hero_id': hero.id,
        'power_id': power.id,
        'strength': hero_power.strength,
        'hero': hero.name,
        'power': power.name
    }), 200




if __name__ == "__main__":
    app.run(port=5555)
