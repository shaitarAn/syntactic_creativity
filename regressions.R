# install.packages("data.table")
# install.packages("ggplot2")

library(data.table)
library(ggplot2)

# empty environment
rm(list=ls())

# Read the first CSV file into a data frame
paras_table <- fread("para_syntax_scores.csv")

# Read the second CSV file into a data frame
sents_table <- fread("sent_syntax_scores.csv")

# Add a column to each data frame to indicate the level
paras_table$Level <- "Paragraph"
sents_table$Level <- "Sentence"

combined_table <- rbind(paras_table, sents_table)

library(lme4)
library(lmerTest)

# boxplot(xwr_mean ~ system, combined_table)
# boxplot(xwr_mean ~ Level, combined_table)
boxplot(xwr_mean ~ lang + system, combined_table)
boxplot(xwr_mean ~ Level + system, combined_table)
boxplot(xwr_mean ~ Level + lang, combined_table)

library(ggplot2)

# Create the boxplot using ggplot2
ggplot(combined_table, aes(x = lang, y = xwr_mean, fill = Level)) +
  geom_boxplot() +
  scale_fill_manual(values = c("#56B4E9", "#666666")) +  # Define colors for levels
  labs(x = NULL, y = NULL) +                             # Remove axis labels
  theme(axis.text.x = element_text(angle = 45, hjust = 1))  # Rotate x-axis labels


# Create the boxplot using ggplot2
ggplot(combined_table, aes(x = lang, y = xwr_mean, fill = system)) +
  geom_boxplot() +
  scale_fill_manual(values = c("#56B4E9", "#666666", "#999999", "#333333", "white")) +  # Define colors for levels
  labs(x = NULL, y = NULL) +                             # Remove axis labels
  theme(axis.text.x = element_text(angle = 45, hjust = 1))  # Rotate x-axis labels

########################
# Model
########################

# Predictor = language
model1 = lmer(xwr_mean ~ system + (1|Level), data=combined_table)
summary(model1)

plot(model1)

# run a logistic regression model multinomial
# Convert xwr_mean to a binary outcome variable
combined_table$binary_xwr <- ifelse(combined_table$xwr_mean > mean(combined_table$xwr_mean), 1, 0)

# Run logistic regression
model_logistic <- glm(binary_xwr ~ system, data = combined_table, family = "binomial")

# View summary of the logistic regression model
summary(model_logistic)
plot(model_logistic)