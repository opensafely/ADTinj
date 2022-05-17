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


###
#download and prep the data
###

ADT_Rates <- read_csv(here::here("output", "measures", "measure_ADT_rate.csv"))
####when using downloaded data 
#ADT_Rates <- read.csv("~/OpenSafely/ADT/Output release/measure_ADT_rate.csv")
#ADT_Rates$date <- as.Date(ADT_Rates$date, format = "%Y-%m-%d")
# calc rate per 100
ADT_Rates$rate <- ADT_Rates$ADT / ADT_Rates$population * 100000
###
# plot monthly number of Rxs
###
p <- ggplot(data = ADT_Rates,
                    aes(date, ADT)) +
  geom_line()+
  geom_point()+
  scale_x_date(date_breaks = "2 month",
               date_labels = "%Y-%m")+
  labs(title = "ADT injectable meducations", 
       x = "", y = "Number of prescriptions")+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
start <- "2020-03-01"
p <- p + geom_vline(xintercept=as.Date(start, format="%Y-%m-%d"), size=0.3, colour="red")
p <- p +  geom_text(aes(x=as.Date(start, format="%Y-%m-%d")+5, y=min(ADT_Rates$ADT)), 
                    color = "red",label="Start of\nrestrictions", angle = 90, size = 3)
# save
ggsave(
  plot= p, dpi=800,width = 20,height = 10, units = "cm",
  filename="ADT_count.png", path=here::here("output"),
)

###
# plot monthly rates per 100
###
p <- ggplot(data = ADT_Rates,
                          aes(date, rate)) +
  geom_line()+
  geom_point()+
  scale_x_date(date_breaks = "2 month",
               date_labels = "%Y-%m")+
  labs(title = "ADT injectable meducations", 
       x = "", y = "Rate per 100.000 \nadult male population")+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
start <- "2020-03-01"
p <- p + geom_vline(xintercept=as.Date(start, format="%Y-%m-%d"), size=0.3, colour="red")
p <- p +  geom_text(aes(x=as.Date(start, format="%Y-%m-%d")+5, y=min(ADT_Rates$rate)), 
                    color = "red",label="Start of\nrestrictions", angle = 90, size = 3)
# save
ggsave(
  plot= p, dpi=800,width = 20,height = 10, units = "cm",
  filename="ADT_rates.png", path=here::here("output"),
)

########## model the data 

model_data <- subset(ADT_Rates, select=c("rate","date"))
model_data$lockdown <- 0 

# periods
start <- "2020-03-01"

# censor the analysis - cut two months at the end 
#model_data <- model_data[6:dim(model_data)[1],]
model_data2 <- model_data[1:(dim(ADT_Rates)[1]-2),]
model_data2$time <- as.numeric(c(1:dim(model_data2)[1]))
model_data_no_covid <- model_data2
model_data2$lockdown[model_data2$date>start]<-1

model <- glm(rate ~ time 
                 + lockdown + lockdown*time
             , data=model_data2)

model_data2$predicted <- predict(model,type="response",model_data2)
model_data2$predicted_no_covid <- predict(model,type="response",model_data_no_covid)

ilink <- family(model)$linkinv
model_data2 <- bind_cols(model_data2, setNames(as_tibble(predict(model, model_data2, se.fit = TRUE)[1:2]),
                                             c('fit_link','se_link')))
model_data2 <- mutate(model_data2,
                     pred  = ilink(fit_link),
                     upr = ilink(fit_link + (2 * se_link)),
                     lwr = ilink(fit_link - (2 * se_link)))
model_data2 <- bind_cols(model_data2, setNames(as_tibble(predict(model, model_data_no_covid, se.fit = TRUE)[1:2]),
                                             c('fit_link_noCov','se_link_noCov')))


model_data2 <- mutate(model_data2,
                     pred_noCov  = ilink(fit_link_noCov),
                     upr_noCov = ilink(fit_link_noCov + (2 * se_link_noCov)),
                     lwr_noCov = ilink(fit_link_noCov - (2 * se_link_noCov)))


p <- ggplot(data = model_data,aes(date, rate, color = "Recorded data", lty="Recorded data")) +
  geom_line()+
  geom_point()+
  scale_x_date(date_breaks = "3 month",
               date_labels = "%Y-%m")+
  labs(title = "ADT injectable medications", 
       x = "", y = "Rate per 100.000 \nadult male population")+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 45, hjust = 1), legend.position="bottom")
start <- "2020-03-01"
p <- p + geom_vline(xintercept=as.Date(start, format="%Y-%m-%d"), size=0.3, colour="red")
p <- p +  geom_text(aes(x=as.Date(start, format="%Y-%m-%d")+5, y=min(ADT_Rates$rate)), 
                    color = "red",label="Start of\nrestrictions", angle = 90, size = 3)

p<-p+geom_line(data=model_data2, aes(y=predicted, color = "Model with COVID-19", lty="Model with COVID-19"), size=0.5)
#p<-p+geom_ribbon(data=model_data2, aes(ymin = lwr, ymax = upr), fill = "grey30", alpha = 0.1)
p<-p+geom_line(data=model_data2, aes(y=predicted_no_covid, color = "Model", lty="Model"), size=0.5)
p<-p+geom_ribbon(data=model_data2, aes(ymin = lwr_noCov, ymax = upr_noCov),color = "red",
                 lty=0, fill = "red", alpha = 0.1)
p <- p + labs(caption="OpenSafely-TPP May 2022")
p <- p + theme(plot.caption = element_text(size=8))
p <- p + theme(plot.title = element_text(size = 10))
p <- p + scale_color_manual(name = NULL, values = c("Model" = "red", "Recorded data" = "black", 
                                                 "Model with COVID-19" = "blue"),guide="none")
p <- p + scale_linetype_manual(name = NULL, values = c("Model" = "solid", "Recorded data" = "solid",
                                                   "Model with COVID-19" = "dashed"),guide="none")
p <- p + scale_fill_manual(name = NULL, values = c("Model" = "red", "Recorded data" = "white",
                                                    "Model with COVID-19" = "white"),guide="none")
p <- p + guides(colour = guide_legend(override.aes = list(linetype=c(1,2,1),fill=c("red",NA,NA), 
                                                          shape = c(NA, NA, 16))))

ggsave(
  plot= p, dpi=800,width = 20,height = 10, units = "cm",
  filename="ADTmodel_rates.png", path=here::here("output"),
)

####
# plot by region 
####


Region <- read_csv(here::here("output", "measures", "measure_ADTbyRegion_rate.csv"))
Region$rate <- Region$ADT / Region$population * 100000

p <- ggplot(data = Region,
            aes(date, rate, color = region, lty = region)) +
  geom_line()+
  #geom_point(color = "region")+
  scale_x_date(date_breaks = "3 month",
               date_labels = "%Y-%m")+
  labs(title = "ADT injectable medications", 
       x = "", y = "Rate per 100.000 \nadult male population")+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 45, hjust = 1), legend.position="bottom")
p <- p + labs(caption="OpenSafely-TPP May 2022")
p <- p + theme(plot.caption = element_text(size=8))
p <- p + theme(plot.title = element_text(size = 10))

start <- "2020-03-01"
p <- p + geom_vline(xintercept=as.Date(start, format="%Y-%m-%d"), size=0.3, colour="red")

# save
ggsave(
  plot= p, dpi=800,width = 20,height = 10, units = "cm",
  filename="ADTbyRegion.png", path=here::here("output"),
)


