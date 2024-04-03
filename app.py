from shiny.express import input, render, ui
from shiny import reactive
from shinywidgets import render_plotly
import pysd
import plotly.express as px
import plotly.graph_objects as go


ui.page_opts(title="Bass diffusion model of new product adoption")

with ui.sidebar():
    ui.input_slider("marketing_effect", "Marketing effect:", 0.001, 0.01, 0.001, step=0.001)
    ui.input_slider("word_of_mouth_effect", "Word of mouth effect", 0, 0.25, 0.025, step=0.025)


@reactive.calc
def results():
    model.set_components({
        'marketing_effect' : input.marketing_effect(),
        'word_of_mouth_effect'  : input.word_of_mouth_effect()
    })
    mod = model.run()
    # mod.TIME = mod.`INITIAL TIME` + cumsum(mod.`TIME STEP`)
    mod = mod.reset_index()
    return mod


with ui.card(full_screen=True):
    @render_plotly
    def new_user_plot():
        mod = results()
        return create_plotly(mod, "New customers", "New users")
    
    @render_plotly
    def total_user_plot():
        mod = results()
        return create_plotly(mod, "Customers", "Total users")


def create_plotly(mod, col, title):
    lineplot = go.Figure()
    lineplot.add_scatter(
        x=mod["time"],
        y=mod[col],
        mode="lines",
        name = "Trial"
    )
    lineplot.add_scatter(
        x=baseline["time"],
        y=baseline[col],
        mode="lines",
        name = "Baseline",
    )
    lineplot.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title="New users",
    )        
    return lineplot



model = pysd.load("bass-diffusion.py")
model.set_components({
    'marketing_effect' : 0.001,
    'word_of_mouth_effect'  : 0.025
})

baseline = model.run()
baseline = baseline.reset_index()



