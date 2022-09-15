from projects.models import Project


def project(request):
    projects = Project.objects.all()
    # projectos
    projectos = []
    for project in projects:
        if project not in projectos:
            projectos.append(project)
    
    return {'projectos': projectos}
