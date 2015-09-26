#plot funny
y=c(0.3749,0.3565,0.3484)
ystd = c(0.001,0.01,0.0125)
b=c(0.4031,0.4966,0.5618)
x=c(10,50,90)
plot(x,y,ylim=c(0.2,0.8),type='b',xlab="% of trainning data",ylab="zero-one-loss",main="Funny data: zero-one-loss VS taining data size"
     ,col='red')
lines(x,b,ylim=c(0.2,0.8),type='b',col='green')
legend("topright", cex = 0.75,legend = c("NBC",'Baseline'), col=c('red','green'), lty=c(1,1))


#plot star
y=c(0.2500,0.2100,0.2136)
ystd = c(0.001,0.01,0.0125)
b=c(0.5593,0.4837,0.5038)
x=c(10,50,90)
plot(x,y,ylim=c(0.1,0.8),type='b',xlab="% of trainning data",ylab="zero-one-loss",main="Stars data: zero-one-loss VS taining data size"
     ,col='red')
lines(x,b,ylim=c(0.1,0.8),type='b',col='green')
legend("topright",cex = 0.75,legend = c("NBC",'Baseline'), col=c('red','green'), lty=c(1,1))