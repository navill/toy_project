def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': {
            'email': user.email, 'fist_name': user.first_name, 'last_name': user.last_name, 'phone': user.phone,
        }
    }
