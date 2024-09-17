# empty environment
rm(list=ls())
# dev.off()

# Load the necessary library
# install.packages("data.table")
# install.packages("ggplot2")
library(data.table)
library(ggplot2)
# Install and load the effsize package
# install.packages("effsize")
library(effsize)


# Read the first CSV file into a data frame
paras_table <- fread("../few-shot/results/para_syntax_scores.csv")

# Read the second CSV file into a data frame
sents_table <- fread("../few-shot/results/sent_syntax_scores.csv")

# Add a column to each data frame to indicate the level
paras_table$Level <- "Paragraph"
sents_table$Level <- "Sentence"

combined_table <- rbind(paras_table, sents_table)

# exclude rows where lang in en-de_news or de-en_news
combined_table <- combined_table[lang != "en-de_news" & lang != "de-en_news"]
combined_table <- combined_table[system != "gpt4mch"]

# Convert 'system' and 'Level' to factor for better plotting control
combined_table$system <- factor(
  combined_table$system, levels = unique(combined_table$system)
)

# select only the necessary columns in the combined table
combined_table <- combined_table[, .(lang, system, xwr_mean, xwr_std, n2mR,length_var, Level)]

# Aggregate the data by language, system, and level to calculate the mean values
combined_table <- combined_table[, .(
  xwr_mean = mean(xwr_mean),
  xwr_std = mean(xwr_std),
  n2mR = mean(n2mR),
  length_var = mean(length_var)# Summing up the observations if necessary
), by = .(lang, system, Level)]

# Convert 'system' and 'Level' to factor for better plotting control
combined_table$system <- factor(
  combined_table$system, levels = c("human", "gpt3", "gpt4hum", "nmt")
)
combined_table$Level <- factor(
  combined_table$Level, levels = c('Paragraph', 'Sentence')
)

# Split data by language after preprocessing
list_df <- split(combined_table, combined_table$lang)

# Continue with the existing functions for analysis


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

calculate_cohens_d <- function(lang_df) {
  paragraph_data <- lang_df[lang_df$Level == "Paragraph", ]
  sentence_data <- lang_df[lang_df$Level == "Sentence", ]
  
  if (nrow(paragraph_data) == 0) {
    print(paste("No paragraph data for language:", lang_df$lang[1]))
    return()
  }
  
  if (!any(paragraph_data$system == "human")) {
    print(paste("No human data for paragraph level in language:", lang_df$lang[1]))
    return()
  }
  
  # Get human mean and standard deviation at paragraph level
  human_data <- paragraph_data[paragraph_data$system == "human", ]
  human_mean <- mean(human_data$xwr_mean)  # ensure aggregation if not already done
  human_sd <- mean(human_data$xwr_std)  # standard deviation can be aggregated similarly if appropriate
  human_observation <- sum(human_data$xwr_observations)  # summing up if multiple entries
  
  systems <- setdiff(unique(paragraph_data$system), "human")
  
  for (sys in systems) {
    sys_data <- paragraph_data[paragraph_data$system == sys, ]
    if (nrow(sys_data) > 0) {
      sys_mean <- mean(sys_data$xwr_mean)
      sys_sd <- mean(sys_data$xwr_std)
      sys_observation <- sum(sys_data$xwr_observations)
      
      pooled_sd <- sqrt(((human_observation - 1) * human_sd^2 + (sys_observation - 1) * sys_sd^2) / (human_observation + sys_observation - 2))
      cohens_d <- (sys_mean - human_mean) / pooled_sd
      
      results_df <<- rbind(results_df, data.frame(Language = lang_df$lang[1], System = sys, Level = "Paragraph", Cohen_d = cohens_d, stringsAsFactors = FALSE))
    } else {
      print(paste("No data for system", sys, "in language", lang_df$lang[1], "at Paragraph level."))
    }
  }
}

# Execute function and debug
for (lang_df in list_df) {
  print(paste("Processing language:", lang_df$lang[1]))
  calculate_cohens_d(lang_df)
}

print(results_df)

calculate_t_test <- function(lang_df) {
  # Filter data for Paragraph and Sentence levels separately
  paragraph_data <- lang_df[lang_df$Level == "Paragraph", ]
  sentence_data <- lang_df[lang_df$Level == "Sentence", ]
  
  # Ensure human data exists at paragraph level
  if (nrow(paragraph_data[paragraph_data$system == "human", ]) == 0) {
    print(paste("No human data for", lang_df$lang[1], "at Paragraph level. Skipping..."))
    return()
  }
  
  human_mean_paragraph <- paragraph_data[paragraph_data$system == "human", ]$xwr_mean
  human_sd_paragraph <- paragraph_data[paragraph_data$system == "human", ]$xwr_std
  sample1_n <- paragraph_data[paragraph_data$system == "human", ]$xwr_observations
  
  systems <- unique(c("gpt3", "gpt4hum", "nmt"))
  for (sys in systems) {
    if (nrow(paragraph_data[paragraph_data$system == sys, ]) > 0) {
      # Proceed with paragraph-level t-test calculations
      sys_mean_paragraph <- paragraph_data[paragraph_data$system == sys, ]$xwr_mean
      sys_sd_paragraph <- paragraph_data[paragraph_data$system == sys, ]$xwr_std
      sample2_n_para <- paragraph_data[paragraph_data$system == sys, ]$xwr_observations
      
      se_diff_para <- sqrt((human_sd_paragraph^2 / sample1_n) + (sys_sd_paragraph^2 / sample2_n_para))
      t_statistic_para <- abs(human_mean_paragraph - sys_mean_paragraph) / se_diff_para
      df_para <- (human_sd_paragraph^2 / sample1_n + sys_sd_paragraph^2 / sample2_n_para)^2 /
        (human_sd_paragraph^4 / (sample1_n^2 * (sample1_n - 1)) + sys_sd_paragraph^4 / (sample2_n_para^2 * (sample2_n_para - 1)))
      p_value_para <- 2 * pt(abs(t_statistic_para), df_para, lower.tail = FALSE)
      
      t_test_results_df <<- rbind(t_test_results_df, data.frame(Language = lang_df$lang[1], System = sys, Level = "Paragraph", t_statistic = t_statistic_para, p_value = p_value_para, stringsAsFactors = FALSE))
    }
    
    if (nrow(sentence_data[sentence_data$system == sys, ]) > 0) {
      # Proceed with sentence-level t-test calculations
      sys_mean_sentence <- sentence_data[sentence_data$system == sys, ]$xwr_mean
      sys_sd_sentence <- sentence_data[sentence_data$system == sys, ]$xwr_std
      sample2_n_sent <- sentence_data[sentence_data$system == sys, ]$xwr_observations
      
      se_diff_sent <- sqrt((human_sd_paragraph^2 / sample1_n) + (sys_sd_sentence^2 / sample2_n_sent))
      t_statistic_sent <- abs(human_mean_paragraph - sys_mean_sentence) / se_diff_sent
      df_sent <- (human_sd_paragraph^2 / sample1_n + sys_sd_sentence^2 / sample2_n_sent)^2 /
        (human_sd_paragraph^4 / (sample1_n^2 * (sample1_n - 1)) + sys_sd_sentence^4 / (sample2_n_sent^2 * (sample2_n_sent - 1)))
      p_value_sent <- 2 * pt(abs(t_statistic_sent), df_sent, lower.tail = FALSE)
      
      t_test_results_df <<- rbind(t_test_results_df, data.frame(Language = lang_df$lang[1], System = sys, Level = "Sentence", t_statistic = t_statistic_sent, p_value = p_value_sent, stringsAsFactors = FALSE))
    }
  }
}


# close device
dev.off()


# End of script





