from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.ellipticCurve.ellipticCurve import EllipticCurve

router = APIRouter()

# Route 1: Generate Key Pair
@router.route('/curve/create', methods=['GET'])
def generate_key_pair():

    print("haha")
    
    # result = EC.cardinality()
    return {"result": 23234}

# # Route 2: Encrypt a Message
# @router.route('/encrypt', methods=['POST'])
# def encrypt_message():
#     public_key = request.json.get('publicKey')
#     message = request.json.get('message')
#     ciphertext = EllipticCurve.encrypt(public_key, message)
#     return jsonify({'ciphertext': ciphertext})

# # Route 3: Decrypt a Message
# @router.route('/decrypt', methods=['POST'])
# def decrypt_message():
#     private_key = request.json.get('privateKey')
#     ciphertext = request.json.get('ciphertext')
#     plaintext = EllipticCurve.decrypt(private_key, ciphertext)
#     return jsonify({'plaintext': plaintext})

# # Route 4: Sign a Message
# @router.route('/sign', methods=['POST'])
# def sign_message():
#     private_key = request.json.get('privateKey')
#     message = request.json.get('message')
#     signature = EllipticCurve.sign_message(private_key, message)
#     return jsonify({'signature': signature})

# # Route 5: Verify a Signature
# @router.route('/verify', methods=['POST'])
# def verify_signature():
#     public_key = request.json.get('publicKey')
#     message = request.json.get('message')
#     signature = request.json.get('signature')
#     is_valid = EllipticCurve.verify_signature(public_key, message, signature)
#     return jsonify({'isValid': is_valid})

# # Route 6: ECDH Key Exchange
# @router.route('/ecdh/exchange', methods=['POST'])
# def ecdh_key_exchange():
#     private_key = request.json.get('privateKey')
#     public_key = request.json.get('publicKey')
#     shared_secret = EllipticCurve.ecdh_key_exchange(private_key, public_key)
#     return jsonify({'sharedSecret': shared_secret})

# # Route 7: Point Addition
# @router.route('/curve/point-addition', methods=['POST'])
# def point_addition():
#     curve = request.json.get('curve')
#     point1 = request.json.get('point1')
#     point2 = request.json.get('point2')
#     result = EllipticCurve.point_addition(curve, point1, point2)
#     return jsonify({'result': result})

# # Route 8: Scalar Multiplication
# @router.route('/curve/scalar-multiplication', methods=['POST'])
# def scalar_multiplication():
#     curve = request.json.get('curve')
#     point = request.json.get('point')
#     scalar = request.json.get('scalar')
#     result = EllipticCurve.scalar_multiplication(curve, point, scalar)
#     return jsonify({'result': result})

# # Route 9: List Supported Curves
# @router.route('/curves', methods=['GET'])
# def list_curves():
#     curves = EllipticCurve.get_supported_curves()
#     return jsonify(curves)

# # Route 10: Hash a Message
# @router.route('/hash', methods=['POST'])
# def hash_message():
#     message = request.json.get('message')
#     algorithm = request.json.get('algorithm')
#     hashed_message = EllipticCurve.hash_message(message, algorithm)
#     return jsonify({'hashedMessage': hashed_message})

# # Route 11: Performance Benchmark
# @router.route('/performance', methods=['GET'])
# def performance_benchmark():
#     benchmarks = EllipticCurve.get_performance_benchmark()
#     return jsonify(benchmarks)




# POST /keys/generate                # Generate ECC keys
# GET  /keys/public/download          # Download public key
# GET  /keys/private/download         # Download private key
# POST /encrypt                       # Encrypt a message
# POST /decrypt                       # Decrypt a message
# POST /sign                          # Sign a message
# POST /verify                        # Verify a signature
# POST /curve/point-addition          # Perform point addition
# POST /curve/scalar-multiplication   # Perform scalar multiplication
# POST /ecdh/exchange                 # Perform ECDH key exchange
# GET  /curves                        # List supported elliptic curves
# POST /hash                          # Hash a message using SHA-2 or SHA-3
# GET  /performance                   # Get performance benchmark
