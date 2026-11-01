# Coursework portfolio sample: household expenditure and podcast listening
# Team assessment. See ../README.md for contribution and AI-assistance notes.
# Input datasets are intentionally not included; see data/README.md.

Sys.setlocale("LC_ALL", "English")
library(tidyverse)
library(ggplot2)
library(emmeans)
library(knitr)
library(patchwork)
library(Hmisc)
library(car)
library(gridExtra)

# Read the data
household <- read_csv("data/household_expenditure.csv")

# Check the data structure and variable types, ranges, and summary statistics
structure(household)
summary(household)


# Convert categorical variables to factors
# Set the order of income categroy to Low、Medium、High

household <- household %>% mutate(Sex = factor(Sex),income_category = factor(income_category, levels = c("Low", "Medium", "High")))

structure(household)
summary(household)


# Check the number of missing values for each variable.
# Decide the missing vaule need to drop or use other handling methods.

household %>% summarise(across(everything(), ~ sum(is.na(.))))


# Use histogram to check the distribution of the dataset
# And check is there any outlier or unreasonable numeric number before regression model

household_long <- household %>%
  select(Food, Alcohol, Debt, Housing, HouseholdSize, Vehicles) %>%
  pivot_longer(cols = everything(), names_to = "Variable", values_to = "Value")

ggplot(household_long, aes(x = Value)) +
  geom_histogram(bins = 30, fill = "grey70", colour = "black") +
  facet_wrap(~Variable, scales = "free", ncol = 3) + 
  labs(title = "Univariate Distributions of Continuous Variables",
       x = "Value", y = "Frequency") + theme_minimal()

# Create a cleaned dataset containing only complete observations
# Acoording to the graph above there is no any outlier in this dataset
# There is only a small amount of missing data, so using dropping method is a suitable method

household <- household %>%
  drop_na(Food, Alcohol, Debt, Housing, HouseholdSize, Sex, Vehicles, income_category, Kids)

#Check the correlation between variables

cor_results <- rcorr(as.matrix(select_if(household, is.numeric)))

print(cor_results)

m.food <- lm(Food ~ Kids + Alcohol + Debt + Housing + HouseholdSize + Vehicles + Sex + income_category, data = household)

# NHST approach
summary(m.food)

# Report coefficient estimates with 95% confidence intervals
cbind(coef(m.food), confint(m.food))

# Examine variance inflation factors to assess multicollinearity
vif(m.food)

# Using a multiple regression model including an interaction between alcohol and debt expenditure
m.food.interaction <- lm(Food ~ Alcohol * Debt + Kids + Housing + HouseholdSize + Vehicles + Sex + income_category,data = household)

# NHST approach
summary(m.food.interaction)

# Report coefficient estimates with 95% confidence intervals
cbind(coef(m.food.interaction), confint(m.food.interaction))

# Create a prediction plot to visualise the Alochol x Debt interaction
# Holding all other variables at their mean or reference values

debt_levels <- c(25, 50, 75, 100)

my_prediction_grid <- expand.grid(
  Alcohol = seq(min(household$Alcohol), max(household$Alcohol), length.out = 100),
  Debt = debt_levels,
  Housing = mean(household$Housing),
  Kids = mean(household$Kids),
  HouseholdSize = mean(household$HouseholdSize),
  Vehicles = mean(household$Vehicles),
  Sex = "female",
  income_category = "Medium")

# Generate predicted food expenditure with 95% confidence intervals
predictions <- predict(
  m.food.interaction,
  newdata = my_prediction_grid,
  interval = "confidence")

my_prediction_grid <- cbind(my_prediction_grid, predictions)

# Plot predicted food expenditure across alcohol spending at different debt levels
ggplot(my_prediction_grid, aes(x = Alcohol, y = fit, color = as.factor(Debt))) +
  geom_line(size = 1) +
  labs(title = "Figure 1:Predicted Food Expenditure by Alcohol Spending",
    subtitle = "Predictions shown at fixed household debt levels (£25, £50, £75, £100)",
    x = "Weekly Alcohol Spending (£)",
    y = "Predicted Weekly Food Expenditure (£)",
    color = "Debt (£)") + theme_minimal()


# read the data 
pod <- read_csv("data/podcast_listens.csv")

# Check the data structure and variable types, ranges, and summary statistics
structure(pod)
summary(pod)


# Change Platform and genre from categorical variables to factor
pod <- pod %>% 
        mutate(Platform = factor(Platform),genre = factor(genre))


# Check the number of missing values for each variable
pod %>% summarise(across(everything(), ~ sum(is.na(.))))


# Use histogram to check the distribution of the dataset
# And check is there any outlier or unreasonable numeric number before regression model

pod_long <- pod %>%
  select(daily.listens, subscribers, total.reviews, avg.review) %>%
  pivot_longer(cols = everything(), names_to = "variable", values_to = "value")

ggplot(pod_long, aes(x = value)) +
  geom_histogram(bins = 30, fill = "grey70", colour = "black") +
  facet_wrap(~variable, scales = "free", ncol = 2) +
  labs(title = "Univariate Distributions of Continuous Podcast Variables (Original Data)",
       subtitle = "Used to identify potential outliers and skewness",
       x = "Value", y = "Frequency") +
  theme_minimal()


ggplot(pod, aes(x = Platform)) +
  geom_bar(fill = "grey70", colour = "black") +
  labs(title = "Distribution of Platforms", x = "Platform", y = "Count") +
  theme_minimal()

# Filter out the average review rating out of 5
# Filter out negative subscriber counts
pod_clean <- pod %>%
  filter(avg.review <= 5) %>%    
  filter(subscribers >= 0)       

pod_clean <- pod_clean %>%
  mutate(genre = factor(genre),
         Platform = factor(Platform))

#Check the correlation between variables

pod_numeric <- pod_clean %>% 
  select(daily.listens, avg.review, total.reviews, subscribers)

pod_cor_results <- rcorr(as.matrix(pod_numeric))

print(pod_cor_results)

# Using a multiple regression model to check the relationship between variables

m.listen <- lm(daily.listens ~ avg.review + total.reviews + subscribers + genre, data = pod_clean)

# NHST approach
summary(m.listen)
# Report coefficient estimates with 95% confidence intervals
cbind(coef(m.listen), confint(m.listen))

vif(m.listen)


# Conduct an analysis of variance (ANOVA) on the regression model to assess the overall contribution of each predictor to daily listens

anova(m.listen)


# Compute estimated marginal means (EMMs) for genre from the regression model

emm.genre.base <- emmeans(m.listen, ~ genre)
emm.base.df <- as.data.frame(summary(emm.genre.base))

# Visualise genre differences using model-based EMMs with 95% confidence intervals

ggplot(emm.base.df, aes(x = genre, y = emmean, ymin = lower.CL, ymax = upper.CL)) +
  geom_point(colour = "magenta", size = 3) +
  geom_linerange(colour = "magenta", linewidth = 1) +
  geom_violin(data = pod_clean,
    mapping = aes(x = genre, y = daily.listens),
    alpha = 0.2,
    inherit.aes = FALSE) +
  labs(x = "Genre", y = "Daily listens",
    subtitle = "Figure 2: Raw distributions with model-adjusted means (95% CIs)") +
  theme_minimal()


# Use a multiple regression model including an interaction between subscriber count and podcast genre to check the relationship between subscribers and daily listens differs across genres

m.listen.interaction <- lm(daily.listens ~ avg.review + total.reviews + subscribers * genre, data = pod_clean)

# NHST approach 
summary(m.listen.interaction)

# Report coefficient estimates with 95% confidence intervals
cbind(coef(m.listen.interaction), confint(m.listen.interaction))


# Compare the baseline model and the interaction model using ANOVA

anova(m.listen, m.listen.interaction)


# Visualise the interaction between subscriber count and podcast genre

ggplot(pod_clean, aes(x = subscribers, y = daily.listens, col = genre)) + 
    geom_point(alpha = 0.2) + 
    geom_smooth(method = lm) +                                            
    labs(x = "Number of Subscribers", y = "Daily Listens", col = "Podcast Genre",
         title = "Figure 3: Effect of Subscribers by Genre")
  
