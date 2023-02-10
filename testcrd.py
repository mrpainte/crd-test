
from pprint import pprint

from kubernetes import client, config


def main():
    config.load_kube_config()

    api = client.CustomObjectsApi()

    # it's my custom resource defined as Dict
    my_resource = {
        "apiVersion": "stable.example.com/v1",
        "kind": "CronTab",
        "metadata": {"name": "my-new-cron-object"},
        "spec": {
            "cronSpec": "* * * * */5",
            "image": "my-awesome-cron-image"
        }
    }

    # patch to update the `spec.cronSpec` field
    patch_body = {
        "spec": {"cronSpec": "* * * * */10", "image": "my-awesome-cron-image"}
    }

    # create the resource
    api.create_namespaced_custom_object(
        group="stable.example.com",
        version="v1",
        namespace="default",
        plural="crontabs",
        body=my_resource,
    )
    print("Resource created")

    # get the resource and print out data
    resource = api.get_namespaced_custom_object(
        group="stable.example.com",
        version="v1",
        name="my-new-cron-object",
        namespace="default",
        plural="crontabs",
    )
    print("Resource details:")
    pprint(resource)

    # patch the namespaced custom object to update the `spec.cronSpec` field
    patch_resource = api.patch_namespaced_custom_object(
        group="stable.example.com",
        version="v1",
        name="my-new-cron-object",
        namespace="default",
        plural="crontabs",
        body=patch_body,
    )
    print("Resource details:")
    pprint(patch_resource)

    # delete it
    api.delete_namespaced_custom_object(
        group="stable.example.com",
        version="v1",
        name="my-new-cron-object",
        namespace="default",
        plural="crontabs",
        body=client.V1DeleteOptions(),
    )
    print("Resource deleted")


if __name__ == "__main__":
    main()