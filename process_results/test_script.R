# empty environment
rm(list=ls())

# Load the necessary library
# install.packages("data.table")
# install.packages("ggplot2")
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



# ############################################################
# # Plot the mean XWR scores by system for each language
# for paragraphs and sentences
# ############################################################

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

# Calculate the number of pages needed to fit all the plots
num_plots <- length(list_df)

# Open a PDF device to save the plots
pdf("plots.pdf")

count <- length(
                Filter(
                       Negate(is.null),
                       lapply(list_df,
                         function(df) {
                           if (nrow(df) >= 8) {
                             TRUE
                           } else {
                             NULL
                          }
                         }
                       )))
num_pages <- ceiling(count / 10)

# Iterate over each page
for (page in 1:num_pages){
  start_plot <- (page -1)*10 +1
  end_plot <- min(start_plot + 9, num_plots)

  # Check if there are enough plots remaining to fill a complete page
  if (start_plot <= num_plots) {
    # Create a new page
    if (page > 2) {
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

# ############################################################
# # Plot the mean XWR scores by system for paragraphs and sentences
# Exclude the outlier langs 'de-ja' & 'fr-pl'
# ############################################################

# Exclude langs 'de-ja' & 'fr-pl'
paras_table <- paras_table[!(lang == "de-ja" | lang == "fr-pl"),]
sents_table <- sents_table[!(lang == "de-ja" | lang == "fr-pl"),]

# Calculate mean xwr for paragraphs
paras_means <- paras_table[, .(MeanXWR = mean(xwr_mean)), by = system]

# Calculate mean xwr_mean for sentences
sents_means <- sents_table[, .(MeanXWR = mean(xwr_mean)), by = system]

# Add a column to each data frame to indicate the level
paras_means$Level <- "Paragraph"
sents_means$Level <- "Sentence"

combined_means <- rbind(paras_means, sents_means)

combined_means <- combined_means[!(system == "human" & Level == "Sentence")]

# rename the "llama" column with "llama2"
combined_means[combined_means$system == "llama", "system"] <- "llama2"

# Convert 'system' and 'Level' to factor for better plotting control
combined_means$system <- factor(combined_means$system, levels = unique(combined_means$system))
combined_means$Level <- factor(combined_means$Level, levels = c('Paragraph', 'Sentence'))

# Now plot the combined table
ggplot(combined_means, aes(x = system, y = MeanXWR, fill = Level)) +
  geom_bar(stat = "identity", position = position_dodge(), width = 0.7) +
  scale_fill_manual(values = c("Paragraph"="#333333", "Sentence"="#999999")) +
  theme_minimal() +
  theme(axis.text.x=element_text(hjust=0.5,size=25),
        axis.text.y=element_text(size=20),   # Larger y-axis labels
        legend.position="top",               # Move legend to top
        legend.box="horizontal",             # Horizontal Legend
        legend.title=element_text(size=20),  # Larger Legend Title
        legend.text=element_text(size=20))+
  # Larger Legend Text                               # Limit Y Axis
 labs(title="mean XWR without de-ja & fr-pl",
       x=NULL,
       y=NULL,
       fill=NULL) + guides(fill = guide_legend(title.position="top",
                                               title.vjust=.5))

# ############################################################
# # Plot the mean XWR scores by system for paragraphs and sentences
# Include only WMT data
# ############################################################

# Include langs 'en-de_news' & 'de_en_news'
paras_table <- paras_table[(lang == "en-de_news" | lang == "de_en_news"),]
sents_table <- sents_table[(lang == "en-de_news" | lang == "de_en_news"),]

# Calculate mean xwr_mean for paragraphs
paras_means <- paras_table[, .(MeanXWR = mean(xwr_mean)), by = system]

# Calculate mean xwr for sentences
sents_means <- sents_table[, .(MeanXWR = mean(xwr_mean)), by = system]

# Add a column to each data frame to indicate the level
paras_means$Level <- "Paragraph"
sents_means$Level <- "Sentence"

combined_means <- rbind(paras_means, sents_means)

combined_means <- combined_means[!(system == "human" & Level == "Sentence")]

# rename the "llama" column with "llama2"
combined_means[combined_means$system == "llama", "system"] <- "llama2"

# Convert 'system' and 'Level' to factor for better plotting control
combined_means$system <- factor(combined_means$system, levels = unique(combined_means$system))
combined_means$Level <- factor(combined_means$Level, levels = c('Paragraph', 'Sentence'))

# Now plot the combined table
ggplot(combined_means, aes(x = system, y = MeanXWR, fill = Level)) +
  geom_bar(stat = "identity", position = position_dodge(), width = 0.7) +
  scale_fill_manual(values = c("Paragraph"="#333333", "Sentence"="#999999")) +
  theme_minimal() +
  theme(axis.text.x=element_text(hjust=0.5,size=25),
        axis.text.y=element_text(size=20),   # Larger y-axis labels
        legend.position="top",               # Move legend to top
        legend.box="horizontal",             # Horizontal Legend
        legend.title=element_text(size=20),  # Larger Legend Title
        legend.text=element_text(size=20))+
  # Larger Legend Text                               # Limit Y Axis
  labs(title="mean XWR with only WMT data",
       x=NULL,
       y=NULL,
       fill=NULL) + guides(fill = guide_legend(title.position="top",
                                               title.vjust=.5))

# ############################################################
# # Plot the mean XWR scores by system for paragraphs and sentences
# Exclude only WMT data
# ############################################################

# Read the first CSV file into a data frame
paras_table <- fread("para_syntax_scores.csv")

# Read the second CSV file into a data frame
sents_table <- fread("sent_syntax_scores.csv")

# Exclude langs 'en-de_news' & 'de_en_news'
paras_table <- paras_table[!(lang == "en-de_news" | lang == "de_en_news"),]
sents_table <- sents_table[!(lang == "en-de_news" | lang == "de_en_news"),]

# Calculate mean xwr for paragraphs
paras_means <- paras_table[, .(MeanXWR = mean(xwr_mean)), by = system]

# Calculate mean xwr for sentences
sents_means <- sents_table[, .(MeanXWR = mean(xwr_mean)), by = system]

# Add a column to each data frame to indicate the level
paras_means$Level <- "Paragraph"
sents_means$Level <- "Sentence"

combined_means <- rbind(paras_means, sents_means)

combined_means <- combined_means[!(system == "human" & Level == "Sentence")]

# rename the "llama" column with "llama2"
combined_means[combined_means$system == "llama", "system"] <- "llama2"

# Convert 'system' and 'Level' to factor for better plotting control
combined_means$system <- factor(combined_means$system, levels = unique(combined_means$system))
combined_means$Level <- factor(combined_means$Level, levels = c('Paragraph', 'Sentence'))

# Now plot the combined table
ggplot(combined_means, aes(x = system, y = MeanXWR, fill = Level)) +
  geom_bar(stat = "identity", position = position_dodge(), width = 0.7) +
  scale_fill_manual(values = c("Paragraph"="#333333", "Sentence"="#999999")) +
  theme_minimal() +
  theme(axis.text.x=element_text(hjust=0.5,size=25),
        axis.text.y=element_text(size=20),   # Larger y-axis labels
        legend.position="top",               # Move legend to top
        legend.box="horizontal",             # Horizontal Legend
        legend.title=element_text(size=20),  # Larger Legend Title
        legend.text=element_text(size=20))+
  # Larger Legend Text                               # Limit Y Axis
  labs(title="mean XWR without WMT data",
       x=NULL,
       y=NULL,
       fill=NULL) + guides(fill = guide_legend(title.position="top",
                                               title.vjust=.5))                                               



# ############################################################
# # Group by lang and compare human and LLMs XWR scores for para level
# ############################################################

# install.packages("RColorBrewer")  
library(data.table)
library(RColorBrewer)
library(dplyr)
library(ggplot2)

# Load the data
paras_table <- fread("para_syntax_scores.csv")

# Define your custom colors
colors <- setNames(c("#56B4E9", "#666666", "#999999", "#333333"), c("human", "gpt3", "gpt4", "llama"))

# Ensure the 'system' column is a factor with levels in the correct order
paras_table$system <- factor(paras_table$system, levels = names(colors))

# Prepare the difference calculation and update 'lang' factor levels
difference_table <- paras_table %>%
  filter(system %in% c("human", "gpt3", "gpt4", "llama")) %>%
  group_by(lang) %>%
  summarize(
    HumanXWR = xwr_mean[system == "human"][1], # Assuring exactly one human score is used
    MaxLLMXWR = max(xwr_mean[system %in% c("gpt3", "gpt4", "llama")]), # Find max xwr among LLMs
    Difference = HumanXWR - MaxLLMXWR,
    .groups = 'drop' # Drop the grouping
  ) %>%
  arrange(desc(Difference))

# Extract the ordered languages for reordering the original table
ordered_langs <- difference_table$lang

# Update 'lang' factor levels in paras_table based on the new order
paras_table$lang <- factor(paras_table$lang, levels = ordered_langs)

# Sort the data frame by lang, and within each lang, by the system
paras_table <- paras_table[order(lang, -as.numeric(system))]

# Stacked plot twith horizontal bars and values inside the bars
ggplot(paras_table, aes(x = xwr_mean, y = lang, fill = system)) +
  geom_bar(stat = "identity", position = "stack") +
  scale_fill_manual(values = colors) +
  
  # Add text labels inside the bars
  geom_text(aes(label = round(xwr_mean, 2), fill = system, color = system),  # Set label, fill, and color aesthetic
            position = position_stack(vjust = 0.5), size = 3, show.legend = FALSE) +  # Adjust position and size
  # Set color to white for llama and gpt3
  scale_color_manual(values = c("gpt3" = "white", "llama" = "white", "gpt4" = "black", "human" = "black")) +
  
  # Adjust the theme
  theme_minimal() +
  theme(
    axis.text.x = element_text(hjust = 1, size = 15),
    axis.text.y = element_text(size = 15),
    plot.title = element_text(face = "bold")
  ) +
  
  # Customize the legend
  guides(
    fill = guide_legend(title.position = "top", title.vjust = 0.6),
    override.aes = list(x = 7.5)
  ) +
  
  # Remove x and y-axis titles and "0.0" from the x-axis
  labs(x = NULL, y = NULL, title = NULL)

# # #stacked plot with horizontal bars
# ggplot(paras_table, aes(x = xwr_mean, y = lang, fill = system)) +
#   geom_bar(stat = "identity", position = "stack") +  
#   scale_fill_manual(values = colors) +
#   theme_minimal() +
#   theme(axis.text.x = element_text(hjust = 1, size = 15,),
#         axis.text.y = element_text(size = 15),
#         plot.title = element_text(face = "bold")) +
#   labs(title = NULL,
#        x = NULL,
#        y = NULL,
#        fill = NULL) +
#   guides(fill = guide_legend(title.position = "top",    # Position the legend title to the top
#                              title.vjust = 0.5),       # Adjust vertical justification of the title
#          override.aes = list(x = 7.5))                 # Adjust the position of the legend on the x-axis


# # #small, with vertical bars
# ggplot(paras_table, aes(x = lang, y = xwr_mean, fill = system)) +
#   geom_bar(stat = "identity", position = "dodge") +
#   scale_fill_manual(values = colors) +
#   theme_minimal() +
#   theme(axis.text.x = element_text(angle = 45, hjust = 1),
#         plot.title = element_text(face = "bold")) +
#   labs(title = "XWR Scores in Paragraph-level Translations by Language and System",
#        x = "Translations",
#        y = "XWR Score",
#        fill = "System")

# # #small, with horizontal bars
# ggplot(paras_table, aes(x = xwr_mean, y = lang, fill = system, label = round(xwr_mean, 2))) +
#   geom_bar(stat = "identity", position = "dodge") +
#   scale_fill_manual(values = colors) +
#   theme_minimal() +
#   theme(axis.text.x = element_text(hjust = 1, size = 15),
#         axis.text.y = element_text(size = 15),
#         plot.title = element_text(face = "bold")) +
#   labs(title = "XWR Scores in Paragraph-level Translations by Language and System",
#        x = "XWR Score",
#        y = NULL,
#        fill = "System")


# ############################################################
# # Plot the mean Length Variation scores by system for paragraphs and sentences
# ############################################################

# Calculate mean length_var for paragraphs
paras_means_LV <- paras_table[, .(MeanLV = mean(length_var)), by = system]

# Calculate mean length_var for sentences
sents_means_LV <- sents_table[, .(MeanLV = mean(length_var)), by = system]

# Add a column to each data frame to indicate the level
paras_means_LV$Level <- "Paragraph"
sents_means_LV$Level <- "Sentence"

# Combine the two tables
combined_means_LV <- rbind(paras_means_LV, sents_means_LV)

combined_means_LV <- combined_means_LV[!(system == "human" & Level == "Sentence")]

# rename the "llama" column with "llama2"
combined_means_LV[combined_means_LV$system == "llama", "system"] <- "llama2"

combined_means_LV

# Convert 'system' and 'Level' to factor for better plotting control
combined_means_LV$system <- factor(combined_means_LV$system, levels = unique(combined_means_LV$system))
combined_means_LV$Level <- factor(combined_means_LV$Level, levels = c('Paragraph', 'Sentence'))

# Reorder the levels of 'system'
combined_means_LV$system <- factor(combined_means_LV$system, levels = c("human", "gpt3", "gpt4", "llama2", "nmt"))

# Plot the combined table
ggplot(combined_means_LV, aes(x = system, y = MeanLV, fill = Level)) +
  geom_bar(stat = "identity", position = position_dodge(), width = 0.7) +
  scale_fill_manual(values = c("Paragraph" = "#333333", "Sentence" = "#999999")) +
  theme_minimal() +
  theme(axis.text.x = element_text(hjust = 0.5, size = 25),
        axis.text.y = element_text(size = 20),      # Larger y-axis labels
        legend.position = "top",                    # Move legend to the top
        legend.box = "horizontal",                  # Horizontal legend
        legend.title = element_text(size = 20),     # Larger legend title
        legend.text = element_text(size = 20)) +    # Larger legend text
  labs(title = "Length Variation across langs and methods",
       x = NULL,
       y = NULL,
       fill = NULL) +
  guides(fill = guide_legend(title.position = "top",  # Position the legend title at the top
                             title.vjust = 0.5))

# ############################################################
# # Plot the mean Length Variation scores by system for paragraphs only
# ############################################################

# Calculate mean length_var for paragraphs grouped by system and lang
paras_means_LV_lang <- paras_table[, .(MeanLV = mean(length_var)), by = .(system, lang)]

# Add a column to the data frame to indicate the level
paras_means_LV_lang$Level <- "Paragraph"

# Rename the "llama" column with "llama2"
paras_means_LV_lang$system[paras_means_LV_lang$system == "llama"] <- "llama2"

# Define your custom colors
colors <- c("human" = "#56B4E9", "gpt3" = "#666666", "gpt4" = "#999999", "llama2" = "#333333")

# Convert 'system' and 'Level' to factor for better plotting control
paras_means_LV_lang$system <- factor(paras_means_LV_lang$system, levels = c("human", "gpt3", "gpt4", "llama2"))
paras_means_LV_lang$Level <- factor(paras_means_LV_lang$Level)

ggplot(paras_means_LV_lang, aes(x=system, y=MeanLV, fill= system)) +
  geom_bar(stat="identity", position=position_dodge(), width=.7) +
  scale_fill_manual(values= colors) +  # Here is where you set color for Paragraphs
  theme_minimal() +
  theme(axis.text.x = element_text(hjust=0.5,size=25),
        axis.text.y = element_text(size=20),      # Larger y-axis labels
        legend.position="top",                     # Move legend to top
        legend.box="horizontal",                   # Horizontal legend
        legend.title=element_text(size=20),         # Larger Legend title
        legend.text=element_text(size=20))   +      # Larger Legend text
  labs(title="Length Variation for Para",
  x = NULL,
  y = NULL,
  fill=NULL) +
  guides(fill=guide_legend(nrow = 1, byrow = TRUE))

# ############################################################
# ############################################################
# ############################################################
# ############################################################

# ############################################################
# # Plot the mean n2m Ratio by system for paragraphs and sentences
# # Remove all n2mR from sentences table that indicate a merge 
# ############################################################

library(data.table)

# Read the second CSV file into a data frame
sents_table <- fread("sent_syntax_scores.csv")

# Recalculate n2mR
sents_table[, adjusted_n2mR := (n2m - merges) / total_src_sents]
# Calculate mean adjusted_n2mR for each system
mean_adjusted_n2mR_per_system <- sents_table[, .(Mean_n2mR = mean(adjusted_n2mR, na.rm = TRUE)), by = system]
# # Calculate overall mean adjusted_n2mR
# overall_mean_adjusted_n2mR <- mean(sents_table$adjusted_n2mR, na.rm = TRUE)

# Calculate mean n2mR for paragraphs
paras_means <- paras_table[, .(Mean_n2mR = mean(n2mR)), by = system]

# Add a column to each data frame to indicate the level
paras_means$Level <- 'Paragraph'
mean_adjusted_n2mR_per_system$Level <- 'Sentence'

# Combine the two tables
combined_means <- rbind(paras_means, mean_adjusted_n2mR_per_system)
# rename the "llama" column with "llama2"
combined_means[combined_means$system == "llama", "system"] <- "llama2"

# Convert 'system' and 'Level' to factor for better plotting control
combined_means$system <- factor(combined_means$system, levels = unique(combined_means$system))
combined_means$Level <- factor(combined_means$Level, levels = c('Paragraph', 'Sentence'))

# Now plot the combined table
ggplot(combined_means, aes(x = system, y = Mean_n2mR, fill = Level)) +
  geom_bar(stat = "identity", position = position_dodge(), width = 0.7) +
  scale_fill_manual(values = c("Paragraph" = "#333333", "Sentence" = "#999999")) +
  theme_minimal() +
  theme(axis.text.x = element_text(hjust = 1, size = 15,)) +
  labs(title = "Mean n2m Alignment Ratio by System and Level",
       x = NULL,
       y = "Mean n2m Ratio",
       fill = "Level")

# ############################################################
# # Group by lang and compare human and LLMs stacked mergesRatio and splitsRatio
# ############################################################

library(tidyr)
library(dplyr)
library(ggplot2)

# Assuming paras_table is your dataset
# Transform the data to long format
long_data <- paras_table %>%
  gather(key = "RatioType", value = "Value", mergesRatio, splitsRatio)

# Ensure the 'system' column is a factor with the correct order
long_data$system <- factor(long_data$system, levels = names(colors))

# Plotting
ggplot(long_data, aes(x = lang, y = Value, fill = RatioType)) +
  geom_bar(stat = "identity", position = "stack") +
  scale_fill_manual(values = c("mergesRatio" = "#56B4E9", "splitsRatio" = "#999999")) +
  facet_wrap(~system) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        plot.title = element_text(face = "bold")) +
  labs(title = "Ratio of Merged and Split Sentences to Number of Source Sentences in Paragraph-level Translations",
       x = "Translations",
       y = "Ratio",
       fill = "Ratio Type")

# ############################################################
# # Group by lang and compare human and LLMs n2mRatio scores
# ############################################################

# Define your custom colors
colors <- setNames(c("#56B4E9", "#666666", "#999999", "#333333"), c("human", "gpt3", "gpt4", "llama"))

# Ensure the 'system' column is a factor with levels in the correct order
paras_table$system <- factor(paras_table$system, levels = names(colors))

# Prepare the difference calculation and update 'lang' factor levels
difference_table <- paras_table %>%
  filter(system %in% c("human", "gpt3", "gpt4", "llama")) %>%
  group_by(lang) %>%
  summarize(
    Human_n2mR = n2mR[system == "human"][1], # Assuring exactly one human score is used
    MaxLLM_n2mR = max(n2mR[system %in% c("gpt3", "gpt4", "llama")]), # Find max xwr_mean among LLMs
    Difference = Human_n2mR - MaxLLM_n2mR,
    .groups = 'drop' # Drop the grouping
  ) %>%
  arrange(desc(Difference))

# Extract the ordered languages for reordering the original table
ordered_langs <- difference_table$lang

# Update 'lang' factor levels in paras_table based on the new order
paras_table$lang <- factor(paras_table$lang, levels = ordered_langs)

# Plot with your custom colors and updated data
ggplot(paras_table, aes(x = lang, y = n2mR, fill = system)) +
  geom_bar(stat = "identity", position = "dodge") +
  scale_fill_manual(values = colors) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        plot.title = element_text(face = "bold")) +
  labs(title = "n2m Alignment Ratio by Language and System",
       x = "Translations",
       y = "n2mRatio",
       fill = "System")

# ############################################################
# # Group by lang and compare human and LLMs merges ratio 
# ############################################################

# Define your custom colors
colors <- setNames(c("#56B4E9", "#666666", "#999999", "#333333"), c("human", "gpt3", "gpt4", "llama"))

# Ensure the 'system' column is a factor with levels in the correct order
paras_table$system <- factor(paras_table$system, levels = names(colors))

# Prepare the difference calculation and update 'lang' factor levels
difference_table <- paras_table %>%
  filter(system %in% c("human", "gpt3", "gpt4", "llama")) %>%
  group_by(lang) %>%
  summarize(
    Human_mergesRatio = mergesRatio[system == "human"][1], # Assuring exactly one human score is used
    MaxLLM_mergesRatio = max(mergesRatio[system %in% c("gpt3", "gpt4", "llama")]), # Find max xwr_mean among LLMs
    Difference = Human_mergesRatio - MaxLLM_mergesRatio,
    .groups = 'drop' # Drop the grouping
  ) %>%
  arrange(desc(Difference))

# Extract the ordered languages for reordering the original table
ordered_langs <- difference_table$lang

# Update 'lang' factor levels in paras_table based on the new order
paras_table$lang <- factor(paras_table$lang, levels = ordered_langs)

# Plot with your custom colors and updated data
ggplot(paras_table, aes(x = lang, y = mergesRatio, fill = system)) +
  geom_bar(stat = "identity", position = "dodge") +
  scale_fill_manual(values = colors) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        plot.title = element_text(face = "bold")) +
  labs(title = "The Ratio of Merged Sentences by Language and System",
       x = "Translations",
       y = "mergesRatio",
       fill = "System")


# ############################################################
# # Group by lang and compare human and LLMs splits ratio 
# ############################################################

# Define your custom colors
colors <- setNames(c("#56B4E9", "#666666", "#999999", "#333333"), c("human", "gpt3", "gpt4", "llama"))

# Ensure the 'system' column is a factor with levels in the correct order
paras_table$system <- factor(paras_table$system, levels = names(colors))

# Prepare the difference calculation and update 'lang' factor levels
difference_table <- paras_table %>%
  filter(system %in% c("human", "gpt3", "gpt4", "llama")) %>%
  group_by(lang) %>%
  summarize(
    Human_splitsRatio = splitsRatio[system == "human"][1], # Assuring exactly one human score is used
    MaxLLM_splitsRatio = max(splitsRatio[system %in% c("gpt3", "gpt4", "llama")]), # Find max splitsRatio among LLMs
    Difference = Human_splitsRatio - MaxLLM_splitsRatio,
    .groups = 'drop' # Drop the grouping
  ) %>%
  arrange(desc(Difference))

# Extract the ordered languages for reordering the original table
ordered_langs <- difference_table$lang

# Update 'lang' factor levels in paras_table based on the new order
paras_table$lang <- factor(paras_table$lang, levels = ordered_langs)

# Plot with your custom colors and updated data
ggplot(paras_table, aes(x = lang, y = splitsRatio, fill = system)) +
  geom_bar(stat = "identity", position = "dodge") +
  scale_fill_manual(values = colors) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        plot.title = element_text(face = "bold")) +
  labs(title = "The Ratio of Split Sentences by Language and System",
       x = "Translations",
       y = "splitsRatio",
       fill = "System")

# ############################################################
# # Plot the mean n2m Ratio by system for paragraphs and sentences (with merges in sent)
# ############################################################

# Calculate mean n2mR for paragraphs
paras_means <- paras_table[, .(Mean_n2mR = mean(n2mR)), by = system]

# Calculate mean n2mR for sentences
sents_means <- sents_table[, .(Mean_n2mR = mean(n2mR)), by = system]

# Add a column to each data frame to indicate the level
paras_means$Level <- 'Paragraph'
sents_means$Level <- 'Sentence'

# Combine the two tables
combined_means <- rbind(paras_means, sents_means)

# Convert 'system' and 'Level' to factor for better plotting control
combined_means$system <- factor(combined_means$system, levels = unique(combined_means$system))
combined_means$Level <- factor(combined_means$Level, levels = c('Paragraph', 'Sentence'))

# Now plot the combined table
ggplot(combined_means, aes(x = system, y = Mean_n2mR, fill = Level)) +
  geom_bar(stat = "identity", position = position_dodge(), width = 0.7) +
  scale_fill_manual(values = c("Paragraph" = "#333333", "Sentence" = "#999999")) +
  theme_minimal() +
  theme(axis.text.x = element_text(hjust = 1, size = 15,)) +
  labs(title = "Mean n2m Alignment Ratio by System and Level",
       x = NULL,
       y = "Mean n2m Ratio",
       fill = "Level")


# ############################################################
# # Visualize the comet scores for each system
# ############################################################

library(data.table)

# Read the comet scores into a data frame
comet_scores <- fread("comet_scores_para.csv")

# The columns are lang,system,score. We want to plot the score for each system by lang with custom colors

# Define your custom colors
colors <- setNames(c("#56B4E9", "#666666", "#999999", "#333333"), c("human", "gpt3", "gpt4", "llama"))

# Ensure the 'system' column is a factor with levels in the correct order
comet_scores$system <- factor(comet_scores$system, levels = names(colors))

# Plot with your custom colors and updated data
ggplot(comet_scores, aes(x = lang, y = score, fill = system)) +
  geom_bar(stat = "identity", position = "dodge") +
  scale_fill_manual(values = colors) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        plot.title = element_text(face = "bold")) +
  labs(title = "COMET Scores for Paragraph-level Translations, one2one Alignment",
       x = "Translations",
       y = "COMET Score",
       fill = "System")


# ############################################################
# # Visualize the comet scores for sent level
# ############################################################
library(data.table)

# Read the comet scores into a data frame
comet_scores <- fread("comet_scores_sent.csv")

# The columns are lang,system,score. We want to plot the score for each system by lang with custom colors

# Define your custom colors
colors <- setNames(c("#56B4E9", "#666666", "#999999", "#333333"), c("human", "gpt3", "gpt4", "llama"))

# Ensure the 'system' column is a factor with levels in the correct order
comet_scores$system <- factor(comet_scores$system, levels = names(colors))

# Plot with your custom colors and updated data
ggplot(comet_scores, aes(x = lang, y = score, fill = system)) +
  geom_bar(stat = "identity", position = "dodge") +
  scale_fill_manual(values = colors) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        plot.title = element_text(face = "bold")) +
  labs(title = "COMET Scores for Sentence-level Translations, one2one Alignment",
       x = "Translations",
       y = "COMET Score",
       fill = "System")
