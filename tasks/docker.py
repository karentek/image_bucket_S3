import platform

from invoke import task

from .config import (
    DOCKER_IMAGE_NAME,
    DOCKER_IMAGE_REGISTRY,
    DOCKER_REGISTRY_PASSWORD,
    DOCKER_REGISTRY_USER,
    PACKAGE_VERSION,
)


@task()
def build(context):
    """Build docker image."""
    print("Env variables")
    print(DOCKER_IMAGE_REGISTRY, DOCKER_REGISTRY_PASSWORD, DOCKER_REGISTRY_USER)
    cmd = f"{get_docker_build_command()} -t {DOCKER_IMAGE_NAME} ."
    context.run(cmd)
    print("deploy images")
    deploy_image(context, DOCKER_IMAGE_NAME, PACKAGE_VERSION)
    deploy_image(context, DOCKER_IMAGE_NAME, "latest")


def deploy_image(context, image_name: str, image_version: str):
    cmd = f"docker login -u {DOCKER_REGISTRY_USER} -p {DOCKER_REGISTRY_PASSWORD} {DOCKER_IMAGE_REGISTRY}"
    context.run(cmd)
    cmd = f"docker tag {image_name} {DOCKER_IMAGE_REGISTRY}/{image_name}:{image_version}"
    context.run(cmd)
    cmd = f"docker push {DOCKER_IMAGE_REGISTRY}/{image_name}:{image_version}"
    context.run(cmd)


def get_docker_build_command():
    processor = platform.processor()
    if "arm" in processor:
        print("Build cross platform image")
        return "docker buildx build --platform linux/amd64"
    return "docker build"
