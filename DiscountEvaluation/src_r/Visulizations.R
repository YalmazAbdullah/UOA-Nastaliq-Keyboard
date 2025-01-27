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


# Read Pairwise Results for Press
dist_A <- read_csv("../output/dist_A.csv")
#########################################################
# Long form Press data
data <- log_data[, c(1, 3:10, 2)]
data_long <- melt(data, id.vars = c("ID", "Keyboard"), variable.name = "Finger", 
                  value.name = "Press")
data_long$Keyboard<-as.factor(data_long$Keyboard)
data_long <- data_long %>%
  mutate(Finger = recode(Finger,
                         Press_L_Little = "Left Little",
                         Press_L_Ring = "Left Ring",
                         Press_L_Middle = "Left Middle",
                         Press_L_Index = "Left Index",
                         Press_R_Little = "Right Little",
                         Press_R_Ring = "Right Ring",
                         Press_R_Middle = "Right Middle",
                         Press_R_Index = "Right Index"))

p <- ggplot(data_long, aes(x = Keyboard, y=Press, fill=Keyboard))+ geom_violin(trim = FALSE) +
  geom_boxplot(width = 0.2) +
  scale_fill_brewer()+
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank())+ scale_fill_brewer(palette="Set3")+
  ylab("Log of Number of Key Press")+ theme(legend.position = "bottom") +stat_summary(fun = "mean",
                                                                                      geom = "point",
                                                                                      color = "red")

p+facet_wrap(.~Finger,  ncol=4, nrow=2, scales = "free_x")
#########################################################
# Long form Dist data
data <- log_data[, c(1, 11:18, 2)]
data_long <- melt(data, id.vars = c("ID", "Keyboard"), variable.name = "Finger", 
                  value.name = "Dist")
data_long$Keyboard<-as.factor(data_long$Keyboard)
data_long <- data_long %>%
  mutate(Finger = recode(Finger,
                         Press_L_Little = "Left Little",
                         Press_L_Ring = "Left Ring",
                         Press_L_Middle = "Left Middle",
                         Press_L_Index = "Left Index",
                         Press_R_Little = "Right Little",
                         Press_R_Ring = "Right Ring",
                         Press_R_Middle = "Right Middle",
                         Press_R_Index = "Right Index"))

p <- ggplot(data_long, aes(x = Keyboard, y=Dist, fill=Keyboard))+ geom_violin(trim = FALSE) +
  geom_boxplot(width = 0.2) +
  scale_fill_brewer()+
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank())+ scale_fill_brewer(palette="Set3")+
  ylab("Log Keyying Distance")+ theme(legend.position = "bottom") +stat_summary(fun = "mean",
                                                                                      geom = "point",
                                                                                      color = "red")

p+facet_wrap(.~Finger,  ncol=4, nrow=2)
