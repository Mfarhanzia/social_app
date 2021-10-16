import os


def get_post_file_upload_path(instance, filename):
    """ creates unique-Path & filename for upload """
    ext = filename.split('.')[-1]
    filename = "%s%s.%s" % ('img', instance.user.pk, ext)

    return os.path.join(
        'post_files', "user_id_{}".format(str(instance.user.id)),  filename
    )
