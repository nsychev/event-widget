import hmac
import hashlib


def verify(request, token):
    secret_key = hashlib.sha256(token.encode()).digest()

    args = dict(request.args)
    received_hash = args.pop("hash")

    actual_hash = hmac.new(
        secret_key,
        '\n'.join(
            f'{key}={value}'
            for key, value in sorted(args.items())
        ).encode(),
        'sha256'
    ).hexdigest()

    return received_hash == actual_hash


def get_info(request):
    if 'username' in request.args:
        return f'@{request.args["username"]}'
    return f'{request.args.get("first_name", "")} {request.args.get("last_name", "")}'
