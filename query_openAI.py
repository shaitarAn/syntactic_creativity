import os
import openai
import requests
import json

openai.organization = "org-HjWBseLU0iDzg4cx01nO6JrY"
openai.api_key = "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"

task = """
# Calculate mean xwr_mean for paragraphs
paras_means <- paras_table[, .(MeanXWR = mean(xwr_mean)), by = system]

# Calculate mean xwr for sentences
sents_means <- sents_table[, .(MeanXWR = mean(xwr_mean)), by = system]

# calculate the standard deviation for paragraphs and sentences
paras_sd <- paras_table[, .(SD_XWR = sd(xwr_mean)), by = system]
sents_sd <- sents_table[, .(SD_XWR = sd(xwr_mean)), by = system]

# Add a column to each data frame to indicate the level
paras_means$Level <- "Paragraph"
sents_means$Level <- "Sentence"

# Combine the two tables
combined_means <- rbind(paras_means, sents_means)

combined_means <- combined_means[!(system == "human" & Level == "Sentence")]


# Convert 'system' and 'Level' to factor for better plotting control
combined_means$system <- factor(
  combined_means$system, levels = unique(combined_means$system)
)
combined_means$Level <- factor(
  combined_means$Level, levels = c("Paragraph", "Sentence")
)

# Now plot the combined table
ggplot(combined_means, aes(x = system, y = MeanXWR, fill = Level)) +
  geom_bar(stat = "identity", position = position_dodge(), width = 0.7) +
  scale_fill_manual(
    values = c("Paragraph" = "#333333", "Sentence" = "#999999")
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(hjust = 0.5,size = 25),
        axis.text.y = element_text(size = 20),   # Larger y-axis labels
        legend.position = "top",               # Move legend to top
        legend.box = "horizontal",             # Horizontal Legend
        legend.title = element_text(size = 20),  # Larger Legend Title
        legend.text = element_text(size = 20)) +
  # Larger Legend Text                               # Limit Y Axis
  labs(title = NULL,
       x = NULL,
       y = NULL,
       fill = NULL) + guides(fill = guide_legend(title.position = "top",
                                                 title.vjust = .5)
) How do i display the std for each bar in the plot?

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

    