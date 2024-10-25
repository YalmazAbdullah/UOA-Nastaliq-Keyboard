library(FSA)
library(tidyverse)
library(ggpubr)
library(rstatix)
library(lme4)
library(robustlmm)
library(ggplot2)
library(emmeans)
library(nlme)
library(lmerTest)
library(parameters)

################
# Prepare Data #
################
# Read Data
data <- read.csv("./output/data/dakshina.csv")
data <- read.csv("./output/data/roUrParl.csv")
view(data)

# Add Hand-Finger combined column
# Each key uses only one Hand-Finger combination
data$Hand_Finger <- paste(data$Hand, data$Finger)
view(data)

# Add 1 smoothing
crulp <- subset(data, Keyboard == "CRULP")
roman <- subset(data, Keyboard == "Roman")
windows <- subset(data, Keyboard == "Windows")

crulp$Prob_Add1 <- (crulp$Frequency+1)/(sum(crulp$Frequency)+length(crulp$Frequency))
roman$Prob_Add1 <- (roman$Frequency+1)/(sum(roman$Frequency)+length(roman$Frequency))
windows$Prob_Add1 <- (windows$Frequency+1)/(sum(windows$Frequency)+length(windows$Frequency))

data <- rbind(crulp, roman, windows)
view(data)

# Total distance calculation
data$Base <- data$Distance*data$Prob_Add1
view(data)

# Summary stats
data %>%
  group_by(Keyboard) %>%
  get_summary_stats(Base, type = "common") 


#################
# Friedman test #
#################
res.fried <- data %>% friedman_test(Base ~ Keyboard | Key)
res.fried

# Effect size
data %>% friedman_effsize(Base ~ Keyboard |Key) 

# Post-hoc
pwc <- data %>%
  wilcox_test(Base ~ Keyboard, paired = TRUE, p.adjust.method = "hommel")
pwc 

ggboxplot(data, x = "Keyboard", y = "Base", add = "jitter")


##################################
# Non linear mixed effects Model #
##################################
# build model
mod <- lme(Base ~  Keyboard *Hand_Finger , random = ~ Keyboard | Key, data =data)
mod

# format output
tut <- summary(mod)
tabl = tut$tTable 
tabl 

# comparison
anova(mod)

# robust model
model_robust <- lmer(Base ~ Hand_Finger * Keyboard + (1 | Key), data = data)
summary(model_robust)
car::Anova(model_robust)

summary(model_robust)
parameters::p_value(model_robust)$p<.05

emmeans_model <- emmeans(model_robust, pairwise ~ Hand_Finger )
summary(emmeans_model) # here we have pairwise comparisons 
contrasts <- as.data.frame(emmeans_model$contrasts)
sign_effects <- subset(contrasts, p.value <.05)
sign_effects
