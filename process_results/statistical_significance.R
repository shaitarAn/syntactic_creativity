# empty environment
rm(list=ls())

# Load the necessary library
# install.packages("data.table")
# install.packages("ggplot2")
library(data.table)
library(ggplot2)
# Install and load the effsize package
install.packages("effsize")
library(effsize)


# Read the first CSV file into a data frame
paras_table <- fread("../results/para_syntax_scores.csv")

# Read the second CSV file into a data frame
sents_table <- fread("../results/sent_syntax_scores.csv")

# Add a column to each data frame to indicate the level
paras_table$Level <- "Paragraph"
sents_table$Level <- "Sentence"

combined_table <- rbind(paras_table, sents_table)

# Convert 'system' and 'Level' to factor for better plotting control
combined_table$system <- factor(
  combined_table$system, levels = unique(combined_table$system)
)
combined_table$Level <- factor(
  combined_table$Level, levels = c('Paragraph', 'Sentence')
) # nolint

# order the levels of 'system' with "human" first
combined_table$system <- factor(
  combined_table$system, levels = c("human", "gpt3", "gpt4", "llama2", "nmt")
)

# select only the necessary columns in the combined table
combined_table <- combined_table[, .(lang, system, xwr_mean, xwr_std, xwr_observation, Level)]

list_df <- split(combined_table, combined_table$lang)

# Create an empty dataframe to store the results
results_df <- data.frame(Language = character(),
                         System = character(),
                         Level = character(),
                         Cohen_d = numeric(),
                         stringsAsFactors = FALSE)

# Function to calculate Cohen's d effect size
calculate_cohens_d <- function(lang_df) {
  # Filter data for Paragraph and Sentence levels separately
  paragraph_data <- lang_df[lang_df$Level == "Paragraph", ]
  sentence_data <- lang_df[lang_df$Level == "Sentence", ]
  
  # Get the human mean and standard deviation at paragraph level
  human_mean_paragraph <- paragraph_data[paragraph_data$system == "human", ]$xwr_mean
  human_sd_paragraph <- paragraph_data[paragraph_data$system == "human", ]$xwr_std
  
  # Loop through each system at both paragraph and sentence levels
  systems <- unique(c("gpt3", "gpt4", "llama2", "nmt"))
  for (sys in systems) {
    # Check if there is data available for the system at paragraph level
    if (any(paragraph_data$system == sys)) {
      # Get the mean and standard deviation for the system at paragraph level
      sys_mean_paragraph <- paragraph_data[paragraph_data$system == sys, ]$xwr_mean
      sys_sd_paragraph <- paragraph_data[paragraph_data$system == sys, ]$xwr_std
      
      # Calculate Cohen's d effect size at paragraph level
      cohens_d_paragraph <- (sys_mean_paragraph - human_mean_paragraph) / sqrt((human_sd_paragraph^2 + sys_sd_paragraph^2) / 2)
      
      # Add the results to the dataframe
      results_df <<- rbind(results_df, data.frame(Language = lang_df$lang[1],
                                                 System = sys,
                                                 Level = "Paragraph",
                                                 Cohen_d = cohens_d_paragraph,
                                                 stringsAsFactors = FALSE))
    }
    
    # Get the mean and standard deviation for the system at sentence level
    sys_mean_sentence <- sentence_data[sentence_data$system == sys, ]$xwr_mean
    sys_sd_sentence <- sentence_data[sentence_data$system == sys, ]$xwr_std
    
    # Calculate Cohen's d effect size at sentence level
    cohens_d_sentence <- (sys_mean_sentence - human_mean_paragraph) / sqrt((human_sd_paragraph^2 + sys_sd_sentence^2) / 2)
    
    # Add the results to the dataframe
    results_df <<- rbind(results_df, data.frame(Language = lang_df$lang[1],
                                               System = sys,
                                               Level = "Sentence",
                                               Cohen_d = cohens_d_sentence,
                                               stringsAsFactors = FALSE))
  }
}

# Iterate over each language dataframe in the list_df
for (lang_df in list_df) {
  calculate_cohens_d(lang_df)
}

# Print the combined results dataframe
print(results_df)

# Save the results dataframe to a CSV file
write.csv(results_df, file = "../results/cohen_d_effect_size.csv", row.names = FALSE)

# Plot the effect size results
ggplot(results_df, aes(x = System, y = Cohen_d, fill = Level)) +
  geom_bar(stat = "identity", position = "dodge") +
  facet_wrap(~Language, scales = "free") +
  theme_minimal() +
  theme(axis.text.x = element_text(hjust = 0.5)) +
  labs(title = "Cohen's d Effect Size for XWR as compared to human values",
       x = NULL,
       y = NULL,
       fill = "Level") +
  scale_fill_manual(values = c("Paragraph" = "lightblue", "Sentence" = "gray")) +
  theme(legend.position = "bottom") +
  theme(legend.title = element_blank()) +
  theme(legend.text = element_text(size = 12)) +
  theme(axis.text.x = element_text(size = 8)) +
  theme(axis.text.y = element_text(size = 8)) +
  theme(plot.title = element_text(size = 14)) +
  theme(strip.text = element_text(size = 10)) +  # Bold and size 12 subplot titles
  theme(legend.key.size = unit(0.5, "cm")) +
  theme(legend.key = element_rect(fill = "white", colour = "white")) +
  theme(legend.background = element_rect(fill = "white", colour = "white"))


# Save the plot to a file
ggsave("../results/cohen_d_effect_size.pdf", width = 12, height = 8, units = "in")

# Print the plot
print(ggplot(results_df, aes(x = System, y = Cohen_d, fill = Level)) +
        geom_bar(stat = "identity", position = "dodge") +
        facet_wrap(~Language, scales = "free") +
        theme_minimal() +
        theme(axis.text.x = element_text(hjust = 0.5)) +
        labs(title = "Cohen's d Effect Size for XWR as compared to human values",
             x = NULL,
             y = NULL,
             fill = "Level") +
        scale_fill_manual(values = c("Paragraph" = "lightblue", "Sentence" = "gray")) +
        theme(legend.position = "bottom") +
        theme(legend.title = element_blank()) +
        theme(legend.text = element_text(size = 8)) +
        theme(axis.text.x = element_text(size = 8)) +
        theme(axis.text.y = element_text(size = 8)) +
        theme(axis.title.x = element_text(size = 10)) +
        theme(axis.title.y = element_text(size = 10)) +
        theme(plot.title = element_text(size = 12)) +
        theme(legend.key.size = unit(0.5, "cm")) +
        theme(legend.key = element_rect(fill = "white", colour = "white")) +
        theme(legend.background = element_rect(fill = "white", colour = "white"))
)
