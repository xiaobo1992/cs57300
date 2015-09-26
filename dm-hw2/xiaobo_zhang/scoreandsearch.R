#part2
data<- read.table("yelp.dat",header=TRUE,sep=";",comment.char="",quote='"')
newdata = data[c(4,42)]
pca = princomp(newdata)
mean_data = scale(newdata,center=T,scale=F)

seq1 = seq(-0.95,0.95,by = 0.05)
variance = c()

for (v1 in seq1){
  v2 = sqrt(1-v1^2)
  b1 = c(v1,v2)
  transformdata = as.matrix(mean_data) %*% as.matrix(b1)
  diff = max(transformdata)- min(transformdata)
  variance = c(variance,diff)  
}

plot(seq1, variance)