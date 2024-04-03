import pysd
import plotly.express as px






model = pysd.load("bass-diffusion.py")
baseline = model.run()
# baseline.TIME = baseline.`INITIAL TIME` + cumsum(baseline.`TIME STEP`)
baseline = baseline.reset_index()
print(baseline)


# model.set_components({
#     'marketing_effect' : input.marketing_effect,
#     'word_of_mouth_effect'  : input.word_of_mouth_effect
# })
# results = model.run()
# results.TIME = results.`INITIAL TIME` + cumsum(results.`TIME STEP`)

# lineplot = px.line(
#         data_frame=results,
#         x="TIME",
#         y="New customers",
#         title="Bass diffusion curve",
# )

