LABEL = "Hello World"
CATEGORY = "Examples"
TOOLTIP = "Show a greeting and the number of selected objects"
ORDER = 10


def run(context):
    message = f"Hello from VRS Tools! Selected objects: {len(context.selected_objects)}"
    print(message)
    return message
