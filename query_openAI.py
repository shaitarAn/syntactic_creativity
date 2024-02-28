import os
import openai
import requests
import json
from dataprep.keys import *

openai.organization = ORGANIZATION
openai.api_key = OPENAI_API_KEY

task = """
list_df <- split(combined_table, combined_table$lang)

# Calculate the number of pages needed to fit all the plots
num_plots <- length(list_df)
num_pages <- ceiling(num_plots / 10)

# Open a PDF device to save the plots
pdf("plots.pdf")

# Iterate over each page
for (page in 1:num_pages) {
  start_plot <- (page - 1) * 10 + 1
  end_plot <- min(start_plot + 9, num_plots)

  # Check if there are enough plots remaining to fill a complete page
  if (start_plot <= num_plots) {
    # Create a new page
    if (page > 1) {
      plot.new()
      plot.window(xlim = c(0, 1), ylim = c(0, 1), asp = 1)
    }

    # Use lapply to iterate over the plots for the current page
    plots <- lapply(list_df[start_plot:end_plot], function(df) {
      if(nrow(df) >= 8){
      p <- ggplot(df, aes(x = system, y = xwr_mean, fill = Level)) +
        geom_bar(stat = "identity", position = position_dodge(), width = 0.7) +
        geom_errorbar(aes(ymin = xwr_mean - xwr_std, ymax = xwr_mean + xwr_std),
                      position = position_dodge(width = 0.7), width = 0.25) +
        scale_fill_manual(
          values = c("Paragraph" = "#333333", "Sentence" = "#999999")
        ) +
        theme_minimal() +
        theme(axis.text.x = element_text(hjust = 0.5, size = 12),
              axis.text.y = element_text(size = 10),
              legend.position = "none") +
        labs(title = paste(unique(df$lang)),
             x = NULL,
             y = NULL,
             fill = NULL)
      # Return the plot
      return(p)
      } else{
        return(NULL)
      }
    })
    plots <- Filter(Negate(is.null), plots)
    # Arrange the plots in a grid layout and print them
    gridExtra::grid.arrange(grobs = plots, ncol = 2)
  }
}

# Close the PDF device
dev.off()

This creates 3 pages with the second page being empty. The first page contains 10 plots and the third page contains 10 plots. How can avoid creating an empty page?

"""

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {openai.api_key}'
    }

promptline = task
prompt =[{
    "role": "system",
    "content": f"You are an academic editor."
    },{
    "role": "user",
    "content": promptline
    }]
data = {
    'model': "gpt-4",
    'messages':prompt,
    "max_tokens":1500,
    "temperature":1,
    "frequency_penalty":1,
    "presence_penalty":0,
    "seed":23,
}

response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers,data=json.dumps(data))


# check 
if response.status_code == 200:
    result = response.json()

    raw_output = result["choices"][0]["message"]["content"]
    print(raw_output)

    