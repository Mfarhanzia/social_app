import os


def get_upload_path(instance, filename):
    """ creates unique-Path & filename for upload """
    ext = filename.split('.')[-1]
    filename = "%s%s.%s" % ('img', instance.pk, ext)

    return os.path.join(
        'profile_images', "user_id_{}".format(str(instance.id)),  filename
    )
