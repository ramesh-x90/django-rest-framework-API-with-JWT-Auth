from rest_framework.renderers import BaseRenderer
import json

class loginRenderer(BaseRenderer):
    media_type = "application/json"
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        
        response = {}
        if "detail" in data:
            response = {"error" : data["detail"]}
        else :
            response = data
        return json.dumps(response)
