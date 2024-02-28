# empty environment
rm(list=ls())

# Load the necessary library
# install.packages("data.table")
# install.packages("ggplot2")
library(data.table)
library(ggplot2)

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

list_df <- split(combined_table, combined_table$lang)

# Define a function to perform ANOVA for a given language dataframe
perform_anova <- function(lang_df) {
  # Filter data for Paragraph and Sentence levels separately
  paragraph_data <- lang_df[lang_df$Level == "Paragraph", ]
  sentence_data <- lang_df[lang_df$Level == "Sentence", ]
  
  # Extract data for the human system at paragraph level
  human_paragraph <- paragraph_data[paragraph_data$system == "human", ]
  
  # Print ANOVA results for Paragraph level
  cat("Language:", lang_df$lang[1], "\n")
  cat("Paragraph Level ANOVA:\n")
  paragraph_anova <- aov(xwr_mean ~ system, data = paragraph_data)
  print(summary(paragraph_anova))
  
  # Print ANOVA results for Sentence level
  cat("\nSentence Level ANOVA:\n")
  sentence_anova <- aov(xwr_mean ~ system, data = sentence_data)
  print(summary(sentence_anova))
  
  # Compare each system with the human system at paragraph level
  systems <- unique(paragraph_data$system)
  for (sys in systems) {
    if (sys != "human") {
      cat("\nComparison of", sys, "with human at Paragraph level:\n")
      diff_mean_paragraph <- mean(paragraph_data$xwr_mean[paragraph_data$system == sys]) - mean(human_paragraph$xwr_mean)
      diff_std_paragraph <- mean(paragraph_data$xwr_std[paragraph_data$system == sys]) - mean(human_paragraph$xwr_std)
      cat("Difference in mean:", diff_mean_paragraph, "\n")
      cat("Difference in standard deviation:", diff_std_paragraph, "\n")
      
      # Perform hypothesis test for mean difference at Paragraph level
      if (length(paragraph_data$xwr_mean[paragraph_data$system == sys]) >= 2) {
        ttest_mean_paragraph <- t.test(paragraph_data$xwr_mean[paragraph_data$system == sys], human_paragraph$xwr_mean, var.equal = TRUE)
        cat("p-value for mean difference at Paragraph level:", ttest_mean_paragraph$p.value, "\n")
      } else {
        cat("Not enough observations for t-test at Paragraph level\n")
      }
    }
  }
  
  # Compare each system with the human system at sentence level
  systems_sentence <- unique(sentence_data$system)
  for (sys in systems_sentence) {
    if (sys != "human") {
      cat("\nComparison of", sys, "with human at Sentence level:\n")
      diff_mean_sentence <- mean(sentence_data$xwr_mean[sentence_data$system == sys]) - mean(human_paragraph$xwr_mean)
      diff_std_sentence <- mean(sentence_data$xwr_std[sentence_data$system == sys]) - mean(human_paragraph$xwr_std)
      cat("Difference in mean:", diff_mean_sentence, "\n")
      cat("Difference in standard deviation:", diff_std_sentence, "\n")
      
      # Perform hypothesis test for mean difference at Sentence level
      if (length(sentence_data$xwr_mean[sentence_data$system == sys]) >= 2) {
        ttest_mean_sentence <- t.test(sentence_data$xwr_mean[sentence_data$system == sys], human_paragraph$xwr_mean, var.equal = TRUE)
        cat("p-value for mean difference at Sentence level:", ttest_mean_sentence$p.value, "\n")
      } else {
        cat("Not enough observations for t-test at Sentence level\n")
      }
    }
  }
}

# Iterate over each language dataframe in the list_df
for (lang_df in list_df) {
  perform_anova(lang_df)
}


