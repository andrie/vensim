from shiny.express import input, render, ui
from shiny import reactive
from shinywidgets import render_plotly
import pysd
import plotly.express as px
import plotly.graph_objects as go


ui.page_opts(title="Bass diffusion model of new product adoption")

defaults = {"me" : 0.001, "wom" : 0.02}

with ui.sidebar():
    ui.input_slider("marketing_effect", "Marketing effect:", 
                    0.001, 0.01, value = defaults["me"], step=0.001)
    ui.input_slider("word_of_mouth_effect", "Word of mouth effect", 
                    0, 0.2, value = defaults["wom"], step=0.01)
    ui.input_action_button("btn_reset", "Reset defaults")
    ui.input_checkbox("show_baseline", "Show baseline", False)


@reactive.calc
def results():
    model.set_components({
        'marketing_effect' : input.marketing_effect(),
        'word_of_mouth_effect'  : input.word_of_mouth_effect()
    })
    mod = model.run()
    mod = mod.reset_index()
    return mod

@reactive.effect
@reactive.event(input.btn_reset)
def _():
    ui.update_slider("marketing_effect", value = defaults["me"])
    ui.update_slider("word_of_mouth_effect", value = defaults["wom"])


card_height = 300

# with ui.card(full_screen=True):
with ui.card(height = card_height):
    @render_plotly
    def total_user_plot():
        mod = results()
        return create_plotly(mod, "Customers", "Total users")

with ui.card(height = card_height):
    @render_plotly
    def new_user_plot():
        mod = results()
        return create_plotly(mod, "New customers", "New users")


def create_plotly(mod, col, title):
    lineplot = go.Figure()
    lineplot.add_scatter(
        x=mod["time"],
        y=mod[col],
        mode="lines",
        name = "Trial"
    )
    if input.show_baseline():
        lineplot.add_scatter(
            x=baseline["time"],
            y=baseline[col],
            mode="lines",
            name = "Baseline",
        )
    lineplot.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title=title,
    )        
    return lineplot



model = pysd.load("bass-diffusion.py")
model.set_components({
    'marketing_effect' : defaults["me"],
    'word_of_mouth_effect'  : defaults["wom"]
})

baseline = model.run()
baseline = baseline.reset_index()



