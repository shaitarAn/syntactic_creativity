import os
import openai
import requests
import json
from dataprep.keys import *

openai.organization = ORGANIZATION
openai.api_key = OPENAI_API_KEY

task = """
library(data.table)
library(ggplot2)

# Read the first CSV file into a data frame
paras_table <- fread("results/para_syntax_scores.csv")

# Read the second CSV file into a data frame
sents_table <- fread("results/sent_syntax_scores.csv")

# ############################################################
# # Plot the mean XWR scores by system for paragraphs and sentences
# ############################################################

# Calculate xwr means for paragraphs and sentences
paras_means <- paras_table[, .(MeanXWR = mean(xwr_mean)), by = system]
sents_means <- sents_table[, .(MeanXWR = mean(xwr_mean)), by = system]

# calculate the standard deviation for paragraphs and sentences
paras_sd <- paras_table[, .(SD_XWR = sd(xwr_mean)), by = system]
sents_sd <- sents_table[, .(SD_XWR = sd(xwr_mean)), by = system]

# Merge the means and standard deviations
paras_data <- merge(paras_means, paras_sd, by = "system")
sents_data <- merge(sents_means, sents_sd, by = "system")

# Add a column to indicate the level
paras_data$Level <- "Paragraph"
sents_data$Level <- "Sentence"

# Combine paragraphs and sentences table
combined_data <- rbind(paras_data, sents_data)

# Convert 'system' and 'Level' to factor for better plotting control
combined_data$system <- factor(
  combined_data$system, levels = unique(combined_data$system)
)
combined_data$Level  <- factor(
  combined_data$Level ,levels = c("Paragraph", "Sentence")
)

combined_data <- combined_data[!(system == "human" & Level == "Sentence")]

# View(combined_data)
# summary(combined_data)

# order the levels of 'system' with "human" first
combined_data$system <- factor(
  combined_data$system, levels = c("human", "gpt3", "gpt4", "llama2", "nmt")
)

# Now plot the combined table with error bars
ggplot(combined_data, aes(x = system, y = MeanXWR, fill = Level)) +
  geom_bar(stat = "identity", position = position_dodge(), width = 0.7) +
  geom_errorbar(
    aes(ymin = MeanXWR - SD_XWR, ymax = MeanXWR + SD_XWR),
    position = position_dodge(width = 0.7), width = 0.25
  ) +  # 95% CI
  scale_fill_manual(
    values = c("Paragraph" = "#333333", "Sentence" = "#999999")
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(hjust = 0.5, size = 25),
        axis.text.y = element_text(size = 20),
        legend.position = "right",
        legend.box = "vertical",
        legend.title = element_text(size = 20),
        legend.text = element_text(size = 20)) +
  labs(title = "Mean XWR and STD XWR Scores by System and Level",
       x = NULL,
       y = "Mean XWR",
       fill = "Level")

This plot is not being displayed. 

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

    