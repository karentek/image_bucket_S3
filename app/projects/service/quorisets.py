from ..models import Image


def get_related_images(project_id, user_id):
    return (Image.objects.select_related('project', 'project__user')
                         .filter(
                                project=project_id,
                                project__user=user_id)
            )
