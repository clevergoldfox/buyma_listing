from firebase_admin import firestore
from datetime import datetime

# Get a reference to the Firestore service
# db = firestore.client()

def create_user(db, name: str, email: str, password: str, role: str = 'user', status: str = 'active'):
    
    # Create a new document in a collection
    users_ref = db.collection('users')
    docs = users_ref.stream()
    time_str = datetime.now().strftime("%Y%m%d%H%M%S%f")
    doc_ref = db.collection('users').document(f'user{time_str}')
    # doc_ref = db.collection('users').document("admin")
    doc_ref.set({
        'name': name,
        'email': email,
        'password': password,
        'role': role,
        'status': status,
        'createdAt': firestore.SERVER_TIMESTAMP
    })

def get_user_by_email(db, email: str):
    """Retrieve user document by email."""
    users_ref = db.collection('users')
    query = users_ref.where('email', '==', email).limit(1)
    results = query.get()
    print(results[0].to_dict())
    
    if results:
        return results[0].to_dict()
    else:
        return None