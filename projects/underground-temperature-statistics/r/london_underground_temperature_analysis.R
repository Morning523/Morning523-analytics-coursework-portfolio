# London Underground temperature analysis
# Coursework code adapted for a public portfolio.
# The original dataset and rendered assessment report are not included.
# See ../../../data/README.md for expected inputs and data notes.

# Section 1

library(tidyverse)
library(ggplot2)
library(knitr)
library(kableExtra)

# Read data 

temp <- read_csv("data/london_underground_temperature.csv")
spec(temp)
glimpse(temp)
summary(temp)

# Data Dictionary

# Data quality checks

ggplot(temp, aes(x = Temp, y = Line)) +
  geom_boxplot(outlier.colour = "red", width = 0.6) +
  labs(title = "Temperature by Underground Line", x = "Temperature (°C)", y = "Underground Line")

# Data Cleaning

 
temp_filter <- filter(temp, Temp>=10, Temp<=40)

# Summary Table

temp_line_sum <- temp_filter %>% 
  group_by(Line) %>%
  summarise(mean_temp = mean(Temp, na.rm=TRUE), 
                   sd_temp = sd(Temp, na.rm=TRUE),
                   lowest_temp = min(Temp, na.rm=TRUE),
                   highest_temp = max(Temp, na.rm=TRUE))

print(temp_line_sum)
                

# Exclude Sub-Surface Lines

temp.line_filter <- filter(temp_filter, Line !="Sub-surface_lines" )

# Plot the distribution of temperature across all years in the data set

temp_stat <-  temp.line_filter %>%
  group_by(Line) %>%
  summarise(mean_temp = mean(Temp, na.rm=TRUE), 
            sd_temp = sd(Temp, na.rm=TRUE))

 ggplot(temp.line_filter, aes(x = Temp)) + geom_density(alpha = 0.2, fill="cyan", colour = "black") + 
  geom_vline(data = temp_stat, aes(xintercept = mean_temp),linetype = "dashed") +
  geom_vline(data = temp_stat, aes(xintercept = mean_temp - sd_temp),colour = "blue", linetype = "dotted", linewidth = 1) +
  geom_vline(data = temp_stat, aes(xintercept = mean_temp + sd_temp),colour = "blue", linetype = "dotted", linewidth = 1)+
  facet_wrap(~ Line) +labs( title = "Temperature Distribution by Underground Line (All Years)", x = "Temperature (°C)", y = "Density")

# Perform a t-test to compare the temperature on the Bakerloo Line to the Central Line

two_lines <- temp.line_filter %>%
  filter(Line %in% c("Bakerloo", "Central"))

t.test(Temp ~ Line, data = two_lines)

# Temperature Comparison: Bakerloo vs Central

yearly_means <- two_lines %>%
  group_by(Year, Line) %>%
  summarise(mean_temp = mean(Temp, na.rm = TRUE), .groups = "drop")

p1 <- ggplot(yearly_means, aes(x = factor(Year), y = mean_temp, color = Line, group = Line)) +
  geom_line(linewidth = 1) + geom_point(size = 2) +labs(title = "Bakerloo vs Central Lines(All Month)",x = "Year", y = "Temperature (°C)")

p1

# Perform a t-test to compare the summer temperature on the Bakerloo Line to the Central Line

summer.months <- c("May", "June", "July", "August")

two_summer <- temp.line_filter %>%
  filter(Line %in% c("Bakerloo", "Central"),
         Month %in% summer.months)

 
t.test(Temp~Line, data = two_summer)

# Temperature Comparison in Summer Months: Bakerloo vs Central

summer_yearly <- two_summer %>%
  group_by(Year, Line) %>%
  summarise(summer_mean = mean(Temp, na.rm = TRUE), .groups = "drop")

p2 <- ggplot(summer_yearly, aes(x= factor(Year), summer_mean, color = Line, group = Line)) + 
  geom_line(linewidth = 1) + geom_point(size = 2) + labs(title = "Bakerloo vs Central Lines (May–Aug)",
       x = "Year", y = "Temperature (°C)")

p2

# Section 2

temp_line_sum %>%
  select(Line, mean_temp, lowest_temp, highest_temp) %>%
  kbl(caption = "Summary statistics of temperature by Underground line") %>%
  kable_styling()

library(patchwork)
p1 + p2 + plot_layout(ncol = 2)

