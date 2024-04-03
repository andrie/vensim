library(reticulate)
library(ggplot2)

# reticulate::virtualenv_create("r-vensim")
# reticulate:: virtualenv_install("r-vensim", "pysd")
reticulate::use_virtualenv("r-vensim", required = TRUE)

pysd <- import("pysd")

target <- "bass-diffusion.mdl"
model <- pysd$read_vensim(target)

model <- pysd$load("bass-diffusion.py")

baseline <- model$run()
baseline
baseline$TIME <- baseline$`INITIAL TIME` + cumsum(baseline$`TIME STEP`)

results <- model$run(params = list(marketing_effect = 0.005))
results
results$TIME <- results$`INITIAL TIME` + cumsum(results$`TIME STEP`)

ggplot(mapping = aes(x = `TIME`, y = `New customers`)) +
  geom_line(data = baseline, aes(colour = "baseline")) +
  geom_line(data = results, aes(colour = "current")) +
  ggtitle("Bass diffusion curve") +
  scale_color_discrete("Scenario")


