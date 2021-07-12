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
