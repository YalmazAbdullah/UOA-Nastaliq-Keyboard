library(ggpubr)
library(dplyr)
library(readr)

# read data
setwd("~/UOA-Nastaliq-Keyboard/DiscountEvaluation/src_r/")
data_sentence <- read.csv("../data/sentence/score/combined_dataset.csv")

# log transform
log_data <- data.frame(
  ID = data_sentence$ID,
  Keyboard = data_sentence$Keyboard,
  Press_L_Little = log(data_sentence$Press_L_Little+1),
  Press_L_Ring = log(data_sentence$Press_L_Ring+1),
  Press_L_Middle = log(data_sentence$Press_L_Middle+1),
  Press_L_Index = log(data_sentence$Press_L_Index+1),
  
  Press_R_Little = log(data_sentence$Press_R_Little+1),
  Press_R_Ring = log(data_sentence$Press_R_Ring+1),
  Press_R_Middle = log(data_sentence$Press_R_Middle+1),
  Press_R_Index = log(data_sentence$Press_R_Index+1),
  
  Dist_L_Little = log(data_sentence$Dist_L_Little+1),
  Dist_L_Ring = log(data_sentence$Dist_L_Ring+1),
  Dist_L_Middle = log(data_sentence$Dist_L_Middle+1),
  Dist_L_Index = log(data_sentence$Dist_L_Index+1),
  
  Dist_R_Little = log(data_sentence$Dist_R_Little+1),
  Dist_R_Ring = log(data_sentence$Dist_R_Ring+1),
  Dist_R_Middle = log(data_sentence$Dist_R_Middle+1),
  Dist_R_Index = log(data_sentence$Dist_R_Index+1)
)

# Read Pairwise Results for Press
press_A <- read_csv("../output/press_A.csv")
View(press_A)


# Read Pairwise Results for Press
dist_A <- read_csv("../output/dist_A.csv")
View(dist_A)
#########################################################
# Long form Press data
data <- log_data[, c(1, 3:10, 2)]
data_long <- melt(data, id.vars = c("ID", "Keyboard"), variable.name = "Finger", 
                  value.name = "Press")
data_long$Keyboard<-as.factor(data_long$Keyboard)

# Plot Press data
plot<-ggviolin(
  data_long, x = "Finger", y = "Press", fill = "Keyboard", position = position_dodge(1)) +
  geom_boxplot(aes(x = Finger, y = Press, group = interaction(Keyboard, Finger)),
               fill = "white", width = 0.1, position = position_dodge(1)) +
  scale_fill_brewer(palette = "Set2") +
  labs(x = "Finger", y = "Log(Scaled Key Press Count+1)")

print(plot)
#########################################################
# Long form Dist data
data <- log_data[, c(1, 11:18, 2)]
data_long <- melt(data, id.vars = c("ID", "Keyboard"), variable.name = "Finger", 
                  value.name = "Dist")
data_long$Keyboard<-as.factor(data_long$Keyboard)

# Plot Dist data
ggviolin(
  data_long, x = "Keyboard", y = "Dist", fill = "Finger", position = position_dodge(1)) +
  geom_boxplot(aes(x = Keyboard, y = Dist, group = interaction(Keyboard, Finger)),fill = "white", width = 0.1, position = position_dodge(1)) +
  scale_fill_brewer(palette = "Set2") +
  labs(x = "Keyboard", y = "Log(Key Dist Count+1)")

print(plot)
