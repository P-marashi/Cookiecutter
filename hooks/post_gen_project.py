import os
import shutil


license = "{{cookiecutter.license}}"
jwt = "{{cookiecutter.use_jwt}}"
project_slug = "{{cookiecutter.project_slug}}"


def delete_resource(resource):
    if os.path.isfile(resource):
        print(f"removing file: {resource}")
        os.remove(resource)
    elif os.path.isdir(resource):
        print(f"removing directory: {resource}")
        shutil.rmtree(resource)


if license == "None":
    delete_resource("LICENSE")
if jwt == "n":
    delete_resource(f"{project_slug}/authentication/")
    delete_resource(f"{project_slug}/users/")

