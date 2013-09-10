#-*- coding:utf-8 -*-

from apps.settings.models import ProjectSettings, Tag
import datetime

def project(request):
    now = datetime.date.today()
    try:
        project = ProjectSettings.objects.filter(is_active=True).get()
        tags = Tag.objects.filter(is_active=True)
        name = project.name
        company = project.company
        owner = project.owner
        description = project.description
        creation = project.creation_date
        return {
            'ProjectName': name,
            'Company': company,
            'Owner': owner,
            'ProjectDescription': description,
            'Creation': creation,
            'Tags': tags,
            'Now': now,
        }
    except:
        return {
            'ProjectName': 'Project',
            'Company': 'Company',
            'Owner': 'Owner',
            'ProjectDescription': 'Description',
            'Creation': 'Creation date',
            'Now': now,
            'Tags': 'Tags',
        }
