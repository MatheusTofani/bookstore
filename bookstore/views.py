from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import git

REPO_PATH = '/home/matheustofani/bookstore'

@csrf_exempt
def update(request):
    if request.method == "POST":
        try:
            repo = git.Repo(REPO_PATH)
            origin = repo.remotes.origin
            origin.pull()
            return JsonResponse({"status": "success", "message": "Updated code on PythonAnywhere"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed."}, status=405)

def hello_world(request):
    template = loader.get_template('hello_world.html')
    return HttpResponse(template.render({}, request))
