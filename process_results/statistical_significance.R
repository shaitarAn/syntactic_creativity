# empty environment
rm(list=ls())
dev.off()

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

t_test_results_df <- data.frame(Language = character(),
                         System = character(),
                         Level = character(),
                         t_statistic = numeric(),
                         p_value = numeric(),
                         stringsAsFactors = FALSE)

# Function to calculate Cohen's d effect size
calculate_cohens_d <- function(lang_df) {
  # Filter data for Paragraph and Sentence levels separately
  paragraph_data <- lang_df[lang_df$Level == "Paragraph", ]
  sentence_data <- lang_df[lang_df$Level == "Sentence", ]
  
  # Get the human mean and standard deviation at paragraph level
  human_mean_paragraph <- paragraph_data[paragraph_data$system == "human", ]$xwr_mean
  human_sd_paragraph <- paragraph_data[paragraph_data$system == "human", ]$xwr_std
  human_observation <- paragraph_data[paragraph_data$system == "human", ]$xwr_observation
  
  # Loop through each system at both paragraph and sentence levels
  systems <- unique(c("gpt3", "gpt4", "llama2", "nmt"))
  for (sys in systems) {
    # Check if there is data available for the system at paragraph level
    if (any(paragraph_data$system == sys)) {
      # Get the mean and standard deviation for the system at paragraph level
      sys_mean_paragraph <- paragraph_data[paragraph_data$system == sys, ]$xwr_mean
      sys_sd_paragraph <- paragraph_data[paragraph_data$system == sys, ]$xwr_std
      sys_observation <- paragraph_data[paragraph_data$system == sys, ]$xwr_observation

      # total number of observations
      total_observation <- human_observation + sys_observation

      # calculate the pooled standard deviation
      pooled_sd <- sqrt(((human_observation - 1) * human_sd_paragraph^2 + (sys_observation - 1) * sys_sd_paragraph^2) / (human_observation + sys_observation - 2))
      
      # Calculate Cohen's d effect size at paragraph level with hedge's g correction
      cohens_d_paragraph <- (sys_mean_paragraph - human_mean_paragraph) / pooled_sd * sqrt((total_observation - 3) / (total_observation - 2.25))
      # cohens_d_paragraph <- (sys_mean_paragraph - human_mean_paragraph) / sqrt((human_sd_paragraph^2 + sys_sd_paragraph^2) / 2)
      
      # Add the results to the dataframe
      results_df <<- rbind(results_df, data.frame(Language = lang_df$lang[1],
                                                 System = sys,
                                                 Level = "Paragraph",
                                                 Cohen_d = cohens_d_paragraph,
                                                 stringsAsFactors = FALSE))
    }
    # Check if there is data available for the system at sentence level
    if (any(sentence_data$system == sys)) {
    
    # Get the mean and standard deviation for the system at sentence level
    sys_mean_sentence <- sentence_data[sentence_data$system == sys, ]$xwr_mean
    sys_sd_sentence <- sentence_data[sentence_data$system == sys, ]$xwr_std
    sys_observation <- sentence_data[sentence_data$system == sys, ]$xwr_observation

    # total number of observations
    total_observation <- human_observation + sys_observation

    # calculate the pooled standard deviation
    pooled_sd_sentence <- sqrt(((human_observation - 1) * human_sd_paragraph^2 + (sys_observation - 1) * sys_sd_sentence^2) / (human_observation + sys_observation - 2))
    
    # Calculate Cohen's d effect size at sentence level with hedge's g correction
    cohens_d_sentence <- (sys_mean_sentence - human_mean_paragraph) / pooled_sd_sentence * sqrt((total_observation - 3) / (total_observation - 2.25))
    
    
    # Add the results to the dataframe
    results_df <<- rbind(results_df, data.frame(Language = lang_df$lang[1],
                                               System = sys,
                                               Level = "Sentence",
                                               Cohen_d = cohens_d_sentence,
                                               stringsAsFactors = FALSE))
  }
}
}

# function to calculcate the Welch t-test (not assuming equal standard deviations)
calculate_t_test <- function(lang_df) {
  # Filter data for Paragraph and Sentence levels separately
  paragraph_data <- lang_df[lang_df$Level == "Paragraph", ]
  sentence_data <- lang_df[lang_df$Level == "Sentence", ]
  
  # Get the human mean and standard deviation at paragraph level
  human_mean_paragraph <- paragraph_data[paragraph_data$system == "human", ]$xwr_mean
  human_sd_paragraph <- paragraph_data[paragraph_data$system == "human", ]$xwr_std
  sample1_n <- paragraph_data[paragraph_data$system == "human", ]$xwr_observation
  
  # Loop through each system at both paragraph and sentence levels
  systems <- unique(c("gpt3", "gpt4", "llama2", "nmt"))
  for (sys in systems) {
    # Check if there is data available for the system at paragraph level
    if (any(paragraph_data$system == sys)) {
      # Get the mean and standard deviation for the system at paragraph level
      sys_mean_paragraph <- paragraph_data[paragraph_data$system == sys, ]$xwr_mean
      sys_sd_paragraph <- paragraph_data[paragraph_data$system == sys, ]$xwr_std
      sample2_n_para <- paragraph_data[paragraph_data$system == sys, ]$xwr_observation
      
      # Calculate Welch t-test at paragraph level
      # Calculate t-test at paragraph level
      se_diff_para <- sqrt((human_sd_paragraph^2 / sample1_n) + (sys_sd_paragraph^2 / sample2_n_para))
      t_statistic_para <- abs(human_mean_paragraph - sys_mean_paragraph) / se_diff_para

      # Get degrees of freedom using Welch's correction
      df_para <- (human_sd_paragraph^2 / sample1_n + sys_sd_paragraph^2 / sample2_n_para)^2 /
      (human_sd_paragraph^4 / (sample1_n^2 * (sample1_n - 1)) +
      sys_sd_paragraph^4 / (sample2_n_para^2 * (sample2_n_para - 1)))

      # Calculate p-value using t-distribution
      p_value_para <- 2 * pt(abs(t_statistic_para), df_para, lower.tail = FALSE)

      # Add the results to the dataframe
      t_test_results_df <<- rbind(t_test_results_df, data.frame(Language = lang_df$lang[1],
                                                 System = sys,
                                                 Level = "Paragraph",
                                                 t_statistic = t_statistic_para,
                                                 p_value = p_value_para,
                                                 stringsAsFactors = FALSE))

    }
      # Check if there is data available for the system at sentence level
    if (any(sentence_data$system == sys)) {
      # calculate the t-test at sentence level
      sys_mean_sentence <- sentence_data[sentence_data$system == sys, ]$xwr_mean
      sys_sd_sentence <- sentence_data[sentence_data$system == sys, ]$xwr_std
      sample2_n_sent <- sentence_data[sentence_data$system == sys, ]$xwr_observation

      # Calculate t-test at sentence level
      se_diff <- sqrt(((human_sd_paragraph^2)/ sample1_n) + ((sys_sd_sentence^2)/ sample2_n_sent))

      t_statistic_sent <- abs(human_mean_paragraph - sys_mean_sentence) / se_diff

      # get degrees of freedom using Welch's correction
      df_sent <- (human_sd_paragraph^2 / sample1_n + sys_sd_sentence^2 / sample2_n_sent)^2 /
      (human_sd_paragraph^4 / (sample1_n^2 * (sample1_n - 1)) +
      sys_sd_sentence^4 / (sample2_n_sent^2 * (sample2_n_sent - 1)))

      # calculate p-value
      p_value_sent <- 2 * pt(abs(t_statistic_sent), df_sent, lower.tail = FALSE)

      # Add the results to the dataframe
      t_test_results_df <<- rbind(t_test_results_df, data.frame(Language = lang_df$lang[1],
                                                 System = sys,
                                                 Level = "Sentence",
                                                 t_statistic = t_statistic_sent,
                                                 p_value = p_value_sent,
                                                 stringsAsFactors = FALSE))
}
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
  labs(title = "Cohen's d Effect Size with Hedge's g Correction for Systems' XWR as Compared to Human Values",
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
ggsave("../viz/cohen_d_effect_size.pdf", width = 12, height = 8, units = "in")

# Perform t-test for each language
for (lang_df in list_df) {
  calculate_t_test(lang_df)
}

# Print the combined results dataframe
print(t_test_results_df)

# Save the results dataframe to a CSV file
write.csv(t_test_results_df, file = "../results/t_test_results.csv", row.names = FALSE)

# Plot the t-test results
ggplot(t_test_results_df, aes(x = System, y = t_statistic, fill = Level)) +
  geom_bar(stat = "identity", position = "dodge") +
  facet_wrap(~Language, scales = "free") +
  theme_minimal() +
  theme(axis.text.x = element_text(hjust = 0.5)) +
  labs(title = "Welch t-test Results for Systems' XWR as Compared to Human XWR",
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
ggsave("../viz/t_test_results.pdf", width = 12, height = 8, units = "in")

# Plot the p-values
ggplot(t_test_results_df, aes(x = System, y = p_value, fill = Level)) +
  geom_bar(stat = "identity", position = "dodge") +
  facet_wrap(~Language, scales = "free") +
  geom_hline(yintercept = 0.05, linetype = "dashed", color = "red") +  # Add threshold line
  theme_minimal() +
  theme(axis.text.x = element_text(hjust = 0.5)) +
  labs(title = "Welch t-test p-values for systems' XWR as Compared to Human XWR",
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
ggsave("../viz/p_value_results.pdf", width = 12, height = 8, units = "in")

# close device
dev.off()


# End of script





