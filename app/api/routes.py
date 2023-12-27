from flask import Blueprint, request, jsonify, render_template
from ..helpers import token_required
from models import db, Contact, plant_schema, plants_schema, Plant

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'woot': 'poot'}

@api.route('/contacts', methods = ['POST'])
@token_required
def create_contact(current_user_token):
    name = request.json['name']
    email = request.json['email']
    phone_number = request.json['phone_number']
    address = request.json['address']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    contact = Contact(name, email, phone_number, address, user_token = user_token )

    db.session.add(contact)
    db.session.commit()

    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/contacts', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    contacts = Contact.query.filter_by(user_token = a_user).all()
    response = contacts_schema.dump(contacts)
    return jsonify(response)

@api.route('/contacts/<id>', methods = ['GET'])
@token_required
def get_single_contact(current_user_token, id):
    contact = Contact.query.get(id)
    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/contacts/<id>', methods = ['POST','PUT'])
@token_required
def update_contact(current_user_token,id):
    contact = Contact.query.get(id) 
    contact.name = request.json['name']
    contact.email = request.json['email']
    contact.phone_number = request.json['phone_number']
    contact.address = request.json['address']
    contact.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/contacts/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)


# Plant route
@api.route('/plants', methods=['POST'])
@token_required
def create_plant(current_user_token):
    try:
        plant_data = request.json  

        common_name = plant_data['common_name']
        scientific_name = plant_data['scientific_name']
        days_to_harvest = plant_data['days_to_harvest']
        sowing = plant_data['sowing']
        light = plant_data['light']
        row_spacing = plant_data['row_spacing']
        minimum_root_depth = plant_data['minimum_root_depth']
        soil_nutriments = plant_data['soil_nutriments']
        user_token = current_user_token.token

        print(f'BIG TESTER: {current_user_token.token}')

        plant = Plant(common_name, scientific_name, days_to_harvest, sowing, light, row_spacing, minimum_root_depth, soil_nutriments, user_token=user_token)

        db.session.add(plant)
        db.session.commit()

        response = plant_schema.dump(plant)
        return jsonify(response)

    except Exception as e:
        print(f"Error creating plant: {str(e)}")
        return jsonify({"error": f"Failed to create plant. Error: {str(e)}"}), 500

@api.route('/plants', methods = ['GET'])
@token_required
def get_plant(current_user_token):
    a_user = current_user_token.token
    plants = Plant.query.filter_by(user_token = a_user).all()
    response = plants_schema.dump(plants)
    return jsonify(response)

@api.route('/plants/<id>', methods = ['GET'])
@token_required
def get_single_plant(current_user_token, id):
    plant = Plant.query.get(id)
    response = plant_schema.dump(plant)
    return jsonify(response)

@api.route('/plants/<id>', methods = ['POST','PUT'])
@token_required
def update_plant(current_user_token,id):
    plant = Plant.query.get(id) 
    plant.common_name = request.json['common_name']
    plant.scientific_name = request.json['scientific_name']
    plant.days_to_harvest= request.json['days_to_harvest']
    plant.sowing = request.json['sowing']
    plant.light = request.json['light']
    plant.row_spacing= request.json['row_spacing']
    plant.minimum_root_depth = request.json['minimum_root_depth']
    plant.soil_nutriments = request.json['soil_nutriments']
    plant.user_token = current_user_token.token

    db.session.commit()
    response = plant_schema.dump(plant)
    return jsonify(response)

@api.route('/plants/<id>', methods = ['DELETE'])
@token_required
def delete_plant(current_user_token, id):
    plant = Plant.query.get(id)
    db.session.delete(plant)
    db.session.commit()
    response = plant_schema.dump(plant)
    return jsonify(response)


