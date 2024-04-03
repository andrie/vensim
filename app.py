from shiny.express import input, render, ui
from shiny import reactive
from shinywidgets import render_plotly
import pysd
import plotly.express as px
import plotly.graph_objects as go


ui.page_opts(title="Bass diffusion model of new product adoption")

with ui.sidebar():
    ui.input_slider("marketing_effect", "Marketing effect:", 0, 0.01, 0.001, step=0.001)
    ui.input_slider("word_of_mouth_effect", "Word of mouth effect", 0, 1, 0.025, step=0.025)

with ui.card(full_screen=True):
    @render_plotly
    def bassplot():
        model.set_components({
            'marketing_effect' : input.marketing_effect(),
            'word_of_mouth_effect'  : input.word_of_mouth_effect()
        })
        results = model.run()
        # results.TIME = results.`INITIAL TIME` + cumsum(results.`TIME STEP`)
        results = results.reset_index()

        lineplot = go.Figure()

        lineplot.add_scatter(
            # data_frame=results,
            x=results["time"],
            y=results["New customers"],
            # labels={"New customers": "Model Results"},
            mode="lines",
            name = "trial"
        )
        lineplot.add_scatter(
            x=baseline["time"],
            y=baseline["New customers"],
            mode="lines",
            name = "Baseline",
        )
        lineplot.update_layout(
            title="New users",
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
# baseline.TIME = baseline.`INITIAL TIME` + cumsum(baseline.`TIME STEP`)



