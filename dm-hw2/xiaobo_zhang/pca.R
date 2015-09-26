data<- read.table("yelp.dat",header=TRUE,sep=";",comment.char="",quote='"')
#part1
x<-data[c(3:4,8:9,14:44)]
logx<-x;
logx['review_count'] <- log(logx['review_count'])

pca_old<-princomp(x)
screeplot(pca_old,type='line')
pca_old$loadings[,1]
summary(pca_old)


pca_new<-princomp(logx)
screeplot(pca_new,type='line')
pca_new$loadings[,1]
summary(pca_new)

sample_data<- x[sample(1:nrow(x),100,replace=FALSE),]
pca_sample_old<-princomp(sample_data)
screeplot(pca_sample_old,type='line')
pca_sample_old$loadings[,1]
summary(pca_sample_old)

sample_data_log<-logx[sample(1:nrow(logx),100,replace=FALSE),]
pca_sample_new<-princomp(sample_data_log)
screeplot(pca_sample_new,type='line')
pca_sample_new$loadings[,1]
summary(pca_sample_new)

