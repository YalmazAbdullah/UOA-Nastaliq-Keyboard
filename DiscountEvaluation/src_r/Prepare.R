library(tidyverse)
library(rstatix)

data_unigram <- read.csv("./output/monad/dakshina_dataset.csv")
data_bigram <- read.csv("./output/dyad/dakshina_dataset.csv")
data_sentence <- read.csv("./output/semtemce/dakshina_dataset.csv")

data_unigram$Score <- data_unigram$KeyyingDistance * data_unigram$Frequency

set.seed(123)
Participant <- rep(1:10, each = 3) # 10 participants, 3 conditions each
Condition <- rep(c("A", "B", "C"), times = 10)
Frequency <- sample(1:10, 30, replace = TRUE) # Random button press frequencies
Preference <- rbinom(30, size = 1, prob = 0.5) # Random binomial responses

dataset <- data.frame(Participant, Condition, Frequency, Preference)
print(dataset)

data_bigram$Reach <- ifelse(data_bigram$Reach == "True", 1, 0)

crulp <- subset(data_bigram, Keyboard == "CRULP")
windows <- subset(data_bigram, Keyboard == "WINDOWS")
ime <- subset(data_bigram, Keyboard == "IME")

crulp$Probability <- (crulp$Frequency+1)/(sum(crulp$Frequency)+9024)
ime$Probability <- (ime$Frequency+1)/(sum(ime$Frequency)+9024)
windows$Probability <- (windows$Frequency+1)/(sum(windows$Frequency)+9024)
data_bigram <- rbind(crulp, windows, ime)

data_bigram$Frequency<-log(data_bigram$Frequency)

data_bigram$HandScore = data_bigram$Probability * data_bigram$SameHand


ggplot(data_bigram, aes(x = HandScore, fill=Keyboard)) + 
  geom_histogram(position="identity", colour="grey40") +scale_y_log10()+
  facet_grid(Keyboard ~ .)

library(ggplot2)
ggplot(data_bigram, aes(x = Keyboard, y = HandScore, group = Keyboard)) +
  geom_boxplot() +
  stat_summary(fun = mean, geom = "point", color = "red", size = 3) + scale_y_log10()+
  theme_minimal()