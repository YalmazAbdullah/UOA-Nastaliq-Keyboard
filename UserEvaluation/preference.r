library(readr)
library(tidyverse)
library(ggpubr)
library(rstatix)

df <- read_csv("Data_User/preference_rankings.csv")

# Reshape into long format
long_df <- df %>%
  pivot_longer(
    cols = c("1", "2", "3"),   # use actual column names from your CSV
    names_to = "rank",
    values_to = "condition"
  ) %>%
  mutate(rank = as.integer(gsub("X", "", rank)))

desc <- long_df %>%
  group_by(condition, rank) %>%
  summarise(count = n(), .groups = "drop") %>%
  group_by(condition) %>%
  mutate(percent = round(100 * count / sum(count), 1))
print(desc)

# Summary stats
long_df %>%
  group_by(condition) %>%
  get_summary_stats(rank, type = "common")

# Omnibus Friedman test (requires user column!)
long_df %>%
  friedman_test(rank ~ condition | user)

# Effect size
long_df %>%
  friedman_effsize(rank ~ condition | user)

# Posthoc Wilcoxon test
pwc <- long_df %>%
  wilcox_test(rank ~ condition, paired = TRUE, p.adjust.method = "holm")

# Effect sizes
eff <- long_df %>%
  wilcox_effsize(rank ~ condition, paired = TRUE)

print(pwc)
print(eff)