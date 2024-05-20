from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import resolve


class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        urls_requiring_token_auth = ['api/all_books']
        resolver_match = resolve(request.path_info)
        current_url_path = resolver_match.route
        if current_url_path in urls_requiring_token_auth:
            if 'Authorization' in request.headers:
                auth_header = request.headers.get('Authorization')
                if auth_header.startswith('Bearer '):
                    token_key = auth_header.split()[1]
                    try:
                        token = RefreshToken(token_key)
                        request.user = token.user
                    except Exception as e:
                        return JsonResponse({'error': 'Token inválido'}, status=401)
                else:
                    return JsonResponse({'error': 'Esperado o formato Bearer Token'}, status=401)
            else:
                return JsonResponse({'error': 'Token de autorização ausente'}, status=401)

        return self.get_response(request)
