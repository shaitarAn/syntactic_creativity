library(data.table)

# Load data
para_data <- fread("../few-shot/results/para_syntax_scores.csv")
sent_data <- fread("../few-shot/results/sent_syntax_scores.csv")

# Add 'Level' column to distinguish between paragraph and sentence data
para_data[, Level := "Paragraph"]
sent_data[, Level := "Sentence"]

# Combine both datasets
combined_data <- rbind(para_data, sent_data)

# Check system types and handle appropriately
combined_data[, system := as.character(system)]  # Ensuring 'system' is treated as a character vector

# Remove specific system if needed and rename systems
combined_data <- combined_data[system != "gpt4mch"]
combined_data[system == "gpt4hum", system := "gpt4"]

# Aggregate data to calculate mean values for each metric
agg_data <- combined_data[, .(xwr_mean = mean(xwr_mean, na.rm = TRUE),
                              n2mR = mean(n2mR, na.rm = TRUE),
                              length_var = mean(length_var, na.rm = TRUE)),
                          by = .(lang, system, Level)]

# Melt the aggregated data to long format for easier analysis
melted_data <- melt(agg_data, id.vars = c("lang", "system", "Level"), variable.name = "Metric", value.name = "Score")

# Function to perform t-tests comparing human scores to each MT system per metric, language, and level
perform_t_tests <- function(sub_data) {
  human_data <- sub_data[sub_data$system == "human", .(Score)]
  mt_data <- sub_data[sub_data$system != "human", .(Score)]
  if (nrow(human_data) > 0 && nrow(mt_data) > 0) {
    test_result <- t.test(mt_data$Score, human_data$Score)
    return(test_result$p.value)
  } else {
    return(NA_real_)
  }
}

# Apply the t-tests and assign p-values
melted_data[, p_value := perform_t_tests(.SD), by = .(lang, system, Level, Metric)]

library(ggplot2)
# Plot the results
ggplot(melted_data, aes(x = system, y = Score, fill = system)) +
  geom_bar(stat = "identity", position = position_dodge()) +
  geom_text(aes(label = ifelse(p_value < 0.05, "*", "")), vjust = -0.5, color = "red") +
  facet_wrap(~lang + Metric + Level, scales = "free_x") +
  labs(title = "Comparison of Metrics Across Systems", x = "System", y = "Metric Score") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
