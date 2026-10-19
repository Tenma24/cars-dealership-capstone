class SecurityHeaders:
    def __init__(self, get_response):
        self.get_response=get_response
    def __call__(self, request):
        response=self.get_response(request)
        if not request.path.startswith('/admin/'):
            response['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' https: data:; object-src 'none'; base-uri 'self'; frame-ancestors 'none'"
        response['Referrer-Policy']='same-origin'
        return response
