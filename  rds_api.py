from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch, NotFoundError
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)

# Elasticsearch client setup
es = Elasticsearch([{'host': '10.211.55.4', 'port': 9200}])

# Authentication middleware
def authenticate():
    token = request.headers.get('Authorization')
    # Your authentication logic here
    if token == 'Bearer YOUR_JWT_TOKEN':
        return True
    else:
        return False

# Events endpoints
@app.route('/events', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'Event received'
        },
        401: {
            'description': 'Unauthorized'
        }
    }
})
def receive_event():
    if not authenticate():
        return jsonify({'error': 'Unauthorized'}), 401
    event_data = request.json
    es.index(index='events', id=event_data['event_id'], body=event_data)
    return jsonify({'message': 'Event received'}), 201

@app.route('/events/<event_id>', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Event found',
            'schema': {
                'type': 'object'
            }
        },
        401: {
            'description': 'Unauthorized'
        },
        404: {
            'description': 'Event not found'
        }
    }
})
def get_event(event_id):
    if not authenticate():
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        res = es.get(index='events', id=event_id)
        return jsonify(res['_source']), 200
    except NotFoundError:
        return jsonify({'error': 'Event not found'}), 404

@app.route('/events/<event_id>', methods=['DELETE'])
@swag_from({
    'responses': {
        200: {
            'description': 'Event deleted'
        },
        401: {
            'description': 'Unauthorized'
        },
        404: {
            'description': 'Event not found'
        }
    }
})
def delete_event(event_id):
    if not authenticate():
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        es.delete(index='events', id=event_id)
        return jsonify({'message': 'Event deleted'}), 200
    except NotFoundError:
        return jsonify({'error': 'Event not found'}), 404

# Samples endpoints
@app.route('/samples', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'Sample request received'
        },
        401: {
            'description': 'Unauthorized'
        }
    }
})
def create_sample_request():
    if not authenticate():
        return jsonify({'error': 'Unauthorized'}), 401
    sample_data = request.json
    es.index(index='samples', id=sample_data['sample_id'], body=sample_data)
    return jsonify({'message': 'Sample request received'}), 201

@app.route('/samples/<sample_id>', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Sample found',
            'schema': {
                'type': 'object'
            }
        },
        401: {
            'description': 'Unauthorized'
        },
        404: {
            'description': 'Sample not found'
        }
    }
})
def get_sample(sample_id):
    if not authenticate():
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        res = es.get(index='samples', id=sample_id)
        return jsonify(res['_source']), 200
    except NotFoundError:
        return jsonify({'error': 'Sample not found'}), 404

# Status endpoints
@app.route('/status', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'Status received'
        },
        401: {
            'description': 'Unauthorized'
        }
    }
})
def receive_status():
    if not authenticate():
        return jsonify({'error': 'Unauthorized'}), 401
    status_data = request.json
    es.index(index='status', id=status_data['host'], body=status_data)
    return jsonify({'message': 'Status received'}), 201

@app.route('/status', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Status found',
            'schema': {
                'type': 'object'
            }
        },
        401: {
            'description': 'Unauthorized'
        }
    }
})
def get_status():
    if not authenticate():
        return jsonify({'error': 'Unauthorized'}), 401
    res = es.search(index='status', body={"query": {"match_all": {}}})
    statuses = {hit['_id']: hit['_source'] for hit in res['hits']['hits']}
    return jsonify(statuses), 200


if __name__ == '__main__':
    app.run(debug=True)
