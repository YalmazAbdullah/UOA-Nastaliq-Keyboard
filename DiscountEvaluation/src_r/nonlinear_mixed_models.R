library(tidyverse)
library(rstatix)
library(nlme)

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

# Total distance calculation and log transformation
data$Base <- data$Distance*data$Prob_Add1
#sqrt transformation seems to work better 
data$Transformed_Base <- sqrt(data$Base)
view(data)

print(sum(data$Frequency))

#################
# Winsorization #
#################
#let's use 10% of our data to winsorize, we have N = 207 and 10% = 20.7 ~ 21
#I also tried 15% but I think 10% works better. You can try other alternatives
percent = 21
wins <- function(x, n=percent) { 
  xx <- sort(unique(x)) 
  x[x<=xx[n]] <- xx[n+percent]
  x[x>=xx[length(xx)-n]] <- xx[length(xx)-n]
  x 
}

data$Transformed_Base <- wins(data$Base,percent)

view(data)
ggplot(data=data, mapping=aes(x=Keyboard, y=Base))+geom_boxplot()
ggplot(data, aes(Base, fill = Keyboard))+geom_histogram()

ggplot(data=data, mapping=aes(x=Keyboard, y=Transformed_Base))+geom_boxplot()
ggplot(data, aes(Transformed_Base, fill = Keyboard))+geom_histogram()

##################################
# linear mixed effects Model #
##################################
mod <- lme(Transformed_Base ~  Keyboard *Hand_Finger , random = ~ Keyboard | Key, data =data)
mod

#get list of residuals 
res <- resid(mod)
plot(fitted(mod), res)
#add a horizontal line at 0 
abline(0,0)
qqnorm(res)
#add a straight diagonal line to the plot
qqline(res) 
plot(density(res))

summary <- summary(mod)
table = as.data.frame(summary$tTable)
table 
significant <- subset(table, `p-value`< .05)
knitr::kable(significant, format = "markdown")

knitr::kable(anova(mod), format = "markdown")

