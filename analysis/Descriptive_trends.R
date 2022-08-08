### INFO
# project: Project #28: Androgen deprivation therapy (ADT) for prostate cancer and COVID-19
# author: Agz Leman
# 4th May 2022
# Plots monthly rates 
###

## library
library(tidyverse)
library(here)
library(MASS)

start <- "2020-03-01"

ADTinj_Rates <- read_csv(here::here("output", "measures", "measure_ADT_inj_rate.csv"))
###
# count ADT injectables 
###
p <- ggplot(data = ADTinj_Rates,
                    aes(date, ADTinj)) +
  geom_line()+
  geom_point()+
  scale_x_date(date_breaks = "2 month",
               date_labels = "%Y-%m")+
  labs(title = "ADT injectable medications", 
       x = "", y = "Number of prescriptions")+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

p <- p + geom_vline(xintercept=as.Date(start, format="%Y-%m-%d"), size=0.3, colour="red")
p <- p +  geom_text(aes(x=as.Date(start, format="%Y-%m-%d")+5, y=min(ADTinj_Rates$ADTinj)), 
                    color = "red",label="Start of\nrestrictions", angle = 90, size = 3)
p <- p + labs(caption="OpenSafely-TPP Aug 2022")
p <- p + theme(plot.caption = element_text(size=8))
p <- p + theme(plot.title = element_text(size = 10))

ggsave(
  plot= p, dpi=800,width = 20,height = 10, units = "cm",
  filename="ADTinj_count.png", path=here::here("output"),
)

###
# rates per 100,000
###
ADTinj_Rates$rate <- ADTinj_Rates$ADTinj / ADTinj_Rates$population * 100000
p <- ggplot(data = ADTinj_Rates,
                          aes(date, rate)) +
  geom_line()+
  geom_point()+
  scale_x_date(date_breaks = "2 month",
               date_labels = "%Y-%m")+
  labs(title = "ADT injectable medications", 
       x = "", y = "Rate per 100.000 \nadult male population")+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

p <- p + geom_vline(xintercept=as.Date(start, format="%Y-%m-%d"), size=0.3, colour="red")
p <- p +  geom_text(aes(x=as.Date(start, format="%Y-%m-%d")+5, y=min(ADTinj_Rates$rate)), 
                    color = "red",label="Start of\nrestrictions", angle = 90, size = 3)
p <- p + labs(caption="OpenSafely-TPP Aug 2022")
p <- p + theme(plot.caption = element_text(size=8))
p <- p + theme(plot.title = element_text(size = 10))

ggsave(
  plot= p, dpi=800,width = 20,height = 10, units = "cm",
  filename="ADTinj_rates.png", path=here::here("output"),
)

###
# rates per 100,000 ****by region***
###
Region <- read_csv(here::here("output", "measures", "measure_ADTinjbyRegion_rate.csv"))
Region$rate <- Region$ADTinj / Region$population * 100000

p <- ggplot(data = Region,
            aes(date, rate, color = region, lty = region)) +
  geom_line()+
  #geom_point(color = "region")+
  scale_x_date(date_breaks = "2 month",
               date_labels = "%Y-%m")+
  labs(title = "ADT injectable medications by Region", 
       x = "", y = "Rate per 100.000 \nadult male population")+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 45, hjust = 1), legend.position="bottom")
p <- p + labs(caption="OpenSafely-TPP Aug 2022")
p <- p + theme(plot.caption = element_text(size=8))
p <- p + theme(plot.title = element_text(size = 10))

p <- p + geom_vline(xintercept=as.Date(start, format="%Y-%m-%d"), size=0.3, colour="red")

ggsave(
  plot= p, dpi=800,width = 20,height = 10, units = "cm",
  filename="ADTinjbyRegion.png", path=here::here("output"),
)

####
# rates per 100,000 ****by IMD***
####
IMD <- read_csv(here::here("output", "measures", "measure_ADTinjbyIMD_rate.csv"))
IMD$rate <- IMD$ADTinj / IMD$population * 100000

p <- ggplot(data = IMD,
            aes(date, rate, color = imd_cat, lty = imd_cat)) +
  geom_line()+
  #geom_point(color = "imd_cat")+
  scale_x_date(date_breaks = "2 month",
               date_labels = "%Y-%m")+
  labs(title = "ADT injectable medications by IMD", 
       x = "", y = "Rate per 100.000 \nadult male population")+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 45, hjust = 1), legend.position="bottom")
p <- p + labs(caption="OpenSafely-TPP Aug 2022")
p <- p + theme(plot.caption = element_text(size=8))
p <- p + theme(plot.title = element_text(size = 10))
p <- p + geom_vline(xintercept=as.Date(start, format="%Y-%m-%d"), size=0.3, colour="red")

ggsave(
  plot= p, dpi=800,width = 20,height = 10, units = "cm",
  filename="ADTinjbyIMD.png", path=here::here("output"),
)

####
# rates per 100,000 ****by Ethnicity***
####
Ethn <- read_csv(here::here("output", "measures", "measure_ADTinjbyEthnicity_rate.csv"))
Ethn$rate <- Ethn$ADTinj / Ethn$population * 100000

p <- ggplot(data = Ethn,
            aes(date, rate, color = ethnicity, lty = ethnicity)) +
  geom_line()+
  scale_x_date(date_breaks = "2 month",
               date_labels = "%Y-%m")+
  labs(title = "ADT injectable medications by ethnicity", 
       x = "", y = "Rate per 100.000 \nadult male population")+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 45, hjust = 1), legend.position="bottom")
p <- p + labs(caption="OpenSafely-TPP Aug 2022")
p <- p + theme(plot.caption = element_text(size=8))
p <- p + theme(plot.title = element_text(size = 10))
p <- p + geom_vline(xintercept=as.Date(start, format="%Y-%m-%d"), size=0.3, colour="red")

ggsave(
  plot= p, dpi=800,width = 20,height = 10, units = "cm",
  filename="ADTinjbyEthnicity.png", path=here::here("output"),
)

#################################################
#######
# Oral medications 
#######
#################################################

ADToral_Rates <- read_csv(here::here("output", "measures", "measure_ADT_oral_rate.csv"))
###
# count ADT Oral medications  
###
p <- ggplot(data = ADToral_Rates,
                    aes(date, ADToral)) +
  geom_line()+
  geom_point()+
  scale_x_date(date_breaks = "2 month",
               date_labels = "%Y-%m")+
  labs(title = "ADT oral medications", 
       x = "", y = "Number of prescriptions")+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

p <- p + geom_vline(xintercept=as.Date(start, format="%Y-%m-%d"), size=0.3, colour="red")
p <- p +  geom_text(aes(x=as.Date(start, format="%Y-%m-%d")+5, y=min(ADToral_Rates$ADToral)), 
                    color = "red",label="Start of\nrestrictions", angle = 90, size = 3)
p <- p + labs(caption="OpenSafely-TPP Aug 2022")
p <- p + theme(plot.caption = element_text(size=8))
p <- p + theme(plot.title = element_text(size = 10))

ggsave(
  plot= p, dpi=800,width = 20,height = 10, units = "cm",
  filename="ADToral_count.png", path=here::here("output"),
)

###
# rates per 100,000
###
ADToral_Rates$rate <- ADToral_Rates$ADToral / ADToral_Rates$population * 100000
p <- ggplot(data = ADToral_Rates,
                          aes(date, rate)) +
  geom_line()+
  geom_point()+
  scale_x_date(date_breaks = "2 month",
               date_labels = "%Y-%m")+
  labs(title = "ADT oral medications", 
       x = "", y = "Rate per 100.000 \nadult male population")+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

p <- p + geom_vline(xintercept=as.Date(start, format="%Y-%m-%d"), size=0.3, colour="red")
p <- p +  geom_text(aes(x=as.Date(start, format="%Y-%m-%d")+5, y=min(ADToral_Rates$rate)), 
                    color = "red",label="Start of\nrestrictions", angle = 90, size = 3)
p <- p + labs(caption="OpenSafely-TPP Aug 2022")
p <- p + theme(plot.caption = element_text(size=8))
p <- p + theme(plot.title = element_text(size = 10))

ggsave(
  plot= p, dpi=800,width = 20,height = 10, units = "cm",
  filename="ADToral_rates.png", path=here::here("output"),
)

###
# rates per 100,000 ****by region***
###
Region <- read_csv(here::here("output", "measures", "measure_ADToralbyRegion_rate.csv"))
Region$rate <- Region$ADToral / Region$population * 100000

p <- ggplot(data = Region,
            aes(date, rate, color = region, lty = region)) +
  geom_line()+
  #geom_point(color = "region")+
  scale_x_date(date_breaks = "2 month",
               date_labels = "%Y-%m")+
  labs(title = "ADT oral medications by Region", 
       x = "", y = "Rate per 100.000 \nadult male population")+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 45, hjust = 1), legend.position="bottom")
p <- p + labs(caption="OpenSafely-TPP Aug 2022")
p <- p + theme(plot.caption = element_text(size=8))
p <- p + theme(plot.title = element_text(size = 10))

p <- p + geom_vline(xintercept=as.Date(start, format="%Y-%m-%d"), size=0.3, colour="red")

ggsave(
  plot= p, dpi=800,width = 20,height = 10, units = "cm",
  filename="ADToralbyRegion.png", path=here::here("output"),
)

####
# rates per 100,000 ****by IMD***
####
IMD <- read_csv(here::here("output", "measures", "measure_ADToralbyIMD_rate.csv"))
IMD$rate <- IMD$ADToral / IMD$population * 100000

p <- ggplot(data = IMD,
            aes(date, rate, color = imd_cat, lty = imd_cat)) +
  geom_line()+
  #geom_point(color = "imd_cat")+
  scale_x_date(date_breaks = "2 month",
               date_labels = "%Y-%m")+
  labs(title = "ADT oral medications by IMD", 
       x = "", y = "Rate per 100.000 \nadult male population")+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 45, hjust = 1), legend.position="bottom")
p <- p + labs(caption="OpenSafely-TPP Aug 2022")
p <- p + theme(plot.caption = element_text(size=8))
p <- p + theme(plot.title = element_text(size = 10))
p <- p + geom_vline(xintercept=as.Date(start, format="%Y-%m-%d"), size=0.3, colour="red")

ggsave(
  plot= p, dpi=800,width = 20,height = 10, units = "cm",
  filename="ADToralbyIMD.png", path=here::here("output"),
)

####
# rates per 100,000 ****by Ethnicity***
####
Ethn <- read_csv(here::here("output", "measures", "measure_ADToralbyEthnicity_rate.csv"))
Ethn$rate <- Ethn$ADToral / Ethn$population * 100000

p <- ggplot(data = Ethn,
            aes(date, rate, color = ethnicity, lty = ethnicity)) +
  geom_line()+
  scale_x_date(date_breaks = "2 month",
               date_labels = "%Y-%m")+
  labs(title = "ADT oral medications by ethnicity", 
       x = "", y = "Rate per 100.000 \nadult male population")+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 45, hjust = 1), legend.position="bottom")
p <- p + labs(caption="OpenSafely-TPP Aug 2022")
p <- p + theme(plot.caption = element_text(size=8))
p <- p + theme(plot.title = element_text(size = 10))
p <- p + geom_vline(xintercept=as.Date(start, format="%Y-%m-%d"), size=0.3, colour="red")

ggsave(
  plot= p, dpi=800,width = 20,height = 10, units = "cm",
  filename="ADToralbyEthnicity.png", path=here::here("output"),
)


