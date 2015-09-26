newdata <- cbind(data['review_count'],data['stars'],city_matrix[,1],city_matrix[,2],category_matrix[,1],category_matrix[,4])
colnames(newdata)[3]<-'las vegas'
colnames(newdata)[4]<-'phoenix'
colnames(newdata)[5]<-'Indian'
colnames(newdata)[6]<-'Chinese'

las_score <- c()
phoenix_score <- c()

indian_score <-c()
chinese_score <- c()
for(i in 1:length(newdata[,1])){
  row=newdata[i,]
  if (row[3] == 1){
    
    las_score <- c(las_score,row[2])
  }
  if(row[4] == 1){
    phoenix_score <- c(phoenix_score,row[2])
  }  
}

mean_las = mean(unlist(las_score))
mean_phoenix = mean(unlist(phoenix_score))

barplot(c(mean_las,mean_phoenix),names.arg=c("Las Vegas","Phoenix"),ylim=c(0,5),ylab = "score",main="Average restaurant score in Las Vegas and Phoenix")

indian_score <-c()
chinese_score <- c()
for(i in 1:length(newdata[,1])){
  row=newdata[i,]
  if (row[5] == 1){
    
    indian_score <- c(indian_score,row[1])
  }
  if(row[6] == 1){
    chinese_score <- c(chinese_score,row[1])
  }  
}

mean_indian = mean(unlist(indian_score))
mean_chinese = mean(unlist(chinese_score))

barplot(c(mean_indian,mean_chinese),names.arg=c("Indian","chinese"),ylim = c(0,50),ylab = "review count",main="Average review count between indain and chinese food")
