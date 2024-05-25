from django.shortcuts import render

class ValueErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except ValueError as e:
            return render(request, 'calorie_count/value_error.html', {'message': str(e)}, status=500)
        return response