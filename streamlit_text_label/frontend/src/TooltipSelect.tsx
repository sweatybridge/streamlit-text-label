import React, { ReactNode } from "react"
import ReactTooltip from "react-tooltip"
import {
  ComponentProps,
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"

interface State {
  selectedText?: string
  selectedIndex?: number
}

class TooltipSelect extends StreamlitComponentBase<State> {
  constructor(props: ComponentProps) {
    super(props)
    this.state = {}
  }

  public render = (): ReactNode => {
    const { body, labels } = this.props.args
    return this.makeTooltip(body, labels)
  }

  private makeTooltip(body: string, labels: string[]) {
    return (
      <>
        <div
          data-for="tooltip-select"
          data-event="click focus"
          data-tip=""
          onMouseUp={() => {
            const text = window.getSelection()?.toString()
            this.setState({
              selectedIndex: undefined,
              selectedText: text?.length ? text : undefined,
            })
          }}
        >
          {body}
        </div>
        <ReactTooltip
          id="tooltip-select"
          place="right"
          globalEventOff="mousedown"
          clickable
        >
          {this.state.selectedText
            ? labels.map((text, index) => (
                <>
                  <input
                    type="checkbox"
                    id={`item-${index}`}
                    className="icon done"
                    checked={this.state.selectedIndex === index}
                    onChange={() =>
                      this.setState(
                        {
                          selectedIndex:
                            this.state.selectedIndex === index
                              ? undefined
                              : index,
                        },
                        () => {
                          Streamlit.setComponentValue([
                            this.state.selectedText,
                            this.state.selectedIndex,
                          ])
                        }
                      )
                    }
                  />
                  <label htmlFor={`item-${index}`} className="label">
                    {text}
                  </label>
                  <br />
                </>
              ))
            : null}
        </ReactTooltip>
      </>
    )
  }
}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(TooltipSelect)
