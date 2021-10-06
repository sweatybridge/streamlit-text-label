import os
from dataclasses import asdict, dataclass
from hashlib import md5
from typing import Any, List, Mapping, Optional

import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = os.getenv("RELEASE", "").upper() != "DEV"

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name
        "label_select",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("label_select", path=build_dir)


# Constants used in defining xml config
FROM_NAME = "label"
TO_NAME = "text"
BODY_VALUE = "body"


@dataclass(frozen=True)
class Selection:
    start: int
    end: int
    text: str
    labels: List[str]

    def to_ls(self) -> Mapping[str, Any]:
        return {
            "from_name": FROM_NAME,
            "to_name": TO_NAME,
            "type": "labels",
            "value": asdict(self),
        }


def _make_rgb(key: str) -> str:
    k = key.encode()
    hash = md5(k).hexdigest()
    return hash[:6]


def _make_xml(labels: List[str]) -> str:
    tags = []
    tags.append("<View>")
    tags.append(f'<Labels name="{FROM_NAME}" toName="{TO_NAME}">')
    tags.extend(f'<Label value="{v}" background="#{_make_rgb(v)}"/>' for v in labels)
    tags.append("</Labels>")
    tags.append(f'<Text name="{TO_NAME}" value="${BODY_VALUE}"/>')
    tags.append("</View>")
    return "\n".join(tags)


def _make_task(body: str, values: List[Selection]) -> Mapping[str, Any]:
    return {
        "id": 1,
        "data": {BODY_VALUE: body},
        "annotations": [{"result": [v.to_ls() for v in values]}],
    }


def _get_selections(annotation: Mapping[str, Any]) -> List[Selection]:
    return [
        Selection(
            start=v["start"],
            end=v["end"],
            text=v["text"],
            labels=v["results"][0]["value"]["labels"],
        )
        for v in annotation["areas"].values()
    ]


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def label_select(
    body: str,
    labels: List[str],
    selections: Optional[List[Selection]] = None,
    interfaces: Optional[List[str]] = None,
) -> List[Selection]:
    """
    Creates a new instance of `label_select` component using Label Studio.

    :param body: The text body to display
    :type body: str
    :param labels: A list of available labels
    :type labels: List[str]
    :param selections: The initial selections, defaults to None
    :type selections: Optional[List[Selection]], optional
    :param interfaces: UI components to display, defaults to ["controls", "update"]
    :type interfaces: Optional[List[str]], optional
    :return: A list of all selections
    :rtype: List[Selection]
    """
    if interfaces is None:
        interfaces = ["controls", "update"]
    config = _make_xml(labels)
    task = _make_task(body, selections or [])
    # Arguments passed here will be sent to the frontend as "args" dictionary.
    annotation = _component_func(config=config, interfaces=interfaces, task=task)
    # Modify the value returned so that it can be used as default selections.
    return _get_selections(annotation) if annotation else None
