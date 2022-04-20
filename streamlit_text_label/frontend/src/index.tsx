import { Streamlit, RenderData } from "streamlit-component-lib"
import LabelStudio from "label-studio"
import "label-studio/build/static/css/main.css"

let ls: any

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event: Event): void {
  if (ls) {
    console.debug("skipped")
    return
  }

  const data = (event as CustomEvent<RenderData>).detail
  const { config, interfaces, task } = data.args

  ls = new LabelStudio("root", {
    config,
    interfaces,
    task,

    onLabelStudioLoad: function (_ls: any) {
      console.debug("loaded")
    },

    onSubmitAnnotation: function (_ls: any, annotation: Record<string, any>) {
      console.debug("submitted")
      annotation = JSON.parse(JSON.stringify(annotation))
      Streamlit.setComponentValue(annotation)
    },

    onUpdateAnnotation: (_ls: any, annotation: Record<string, any>) => {
      console.debug("updated")
      annotation = JSON.parse(JSON.stringify(annotation))
      Streamlit.setComponentValue(annotation)
      // We tell Streamlit to update our frameHeight after each update event, in case
      // it has changed. (This isn't strictly necessary if the results sidebar is not
      // rendered because the component height stays fixed. But this is a low-cost
      // function, so there's no harm in doing it redundantly.)
      Streamlit.setFrameHeight()
    },

    onDeleteAnnotation: function (_ls: any, annotation: Record<string, any>) {
      console.debug("deleted")
      annotation = JSON.parse(JSON.stringify(annotation))
      Streamlit.setComponentValue(annotation)
      Streamlit.setFrameHeight()
    },
  })

  // Finally, tell Streamlit to update our initial height. We omit the
  // `height` parameter here to have it default to our scrollHeight.
  Streamlit.setFrameHeight()
}

// Attach our `onRender` handler to Streamlit's render event.
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
// Tell Streamlit we're ready to start receiving data. We won't get our
// first RENDER_EVENT until we call this function.
Streamlit.setComponentReady()
