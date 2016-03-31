from hashlib import sha256
from app.models import BlockedClients, db
from datetime import date
from flask import current_app


def is_blocked(request):
    register_ip_address(request)
    hashed_ip = get_hashed_ip_addr(get_ip_addr(request))
    client = BlockedClients().query.filter_by(id=hashed_ip).first()
    if client.date == date.today() and client.calls > current_app.comfig['MAX_CALLS_PER_IP_PER_DAY']:
        return True
    else:
        return False


def get_ip_addr(request):
    if 'X-Forwarded-For' in request.headers and request.remote_addr == '127.0.0.1':
        return request.headers['X-Forwarded-For']
    return request.remote_addr


def get_hashed_ip_addr(address):
    return sha256(bytes(str(address), 'utf-8')).hexdigest()


def register_ip_address(request):
    hashed_ip = get_hashed_ip_addr(get_ip_addr(request))
    client = BlockedClients().query.filter_by(id=hashed_ip).first()
    if client is None:
        client = BlockedClients()
        client.id = hashed_ip
        client.calls = 1
        client.date = date.today()
        db.session.add(client)
    elif client.date != date.today():
        client.calls = 1
        client.date = date.today()
    else:
        client.calls += 1
    db.session.commit()
