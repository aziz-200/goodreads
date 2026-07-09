# currently we do not need it
# class SimpleMiddleware(object):
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#
#     def __call__(self, request):
#         print(f"Before request: {request.path}")
#         response = self.get_response(request)
#         print(f"After request: {request.path}")
#         return response