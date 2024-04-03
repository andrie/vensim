#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#



library(shiny)
library(reticulate)
library(ggplot2)
# reticulate::use_virtualenv("r-vensim", required = TRUE)
# reticulate::py_config()
pysd <- import("pysd")

model <- pysd$load("bass-diffusion.py")

baseline <- model$run()
baseline$TIME <- baseline$`INITIAL TIME` + cumsum(baseline$`TIME STEP`)


# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Bass diffusion model"),

    # Sidebar with a slider input for number of bins
    sidebarLayout(
        sidebarPanel(
            sliderInput("marketing_effect",
                        "Marketing effect:",
                        min = 0,
                        max = 0.01,
                        value = 0.003,
                        step = 0.001),
            sliderInput("word_of_mouth_effect",
                        "Word of mouth effect",
                        min = 0,
                        max = 1,
                        value = 0.1,
                        step = 0.025)
        ),

        # Show a plot of the generated distribution
        mainPanel(
           plotOutput("bassPlot")
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {

    output$bassPlot <- renderPlot({
        # generate bins based on input$bins from ui.R
        # browser()
        model$set_components(
            params =
                list(
                    marketing_effect = input$marketing_effect,
                    word_of_mouth_effect  = input$word_of_mouth_effect

                ))
        results <- model$run()
        results$TIME <- results$`INITIAL TIME` + cumsum(results$`TIME STEP`)

        ggplot(mapping = aes(x = `TIME`, y = `New customers`)) +
            geom_line(data = baseline, aes(colour = "baseline")) +
            geom_line(data = results, aes(colour = "current")) +
            ggtitle("Bass diffusion curve") +
            scale_color_discrete("Scenario")
    })
}

# Run the application
shinyApp(ui = ui, server = server)
