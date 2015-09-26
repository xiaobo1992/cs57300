data<- read.table("yelp.dat",header=TRUE,sep=";",comment.char="",quote='"')
trim <- function (x) gsub("^\\s+|\\s+$", "", x)

#find first 30 category
category <-c()
for(item in unlist(data['categories'])){
  temp <- unlist(strsplit(item,",",fixed=T))
  for(i in temp){
    if(!is.element(i,category)){
      category <- c(category,i)
    }
  }
}
category <- category[1:30]
category <- trim(category)

#find top 30 city
city<-data['city']
city<-table(city)
city<-sort(city,decreasing = TRUE)
city<-city[1:30]
city<-names(city)
city<-trim(city)

#create binary matrix for city
city_matrix <- matrix(nrow = length(data[,1]),ncol = length(city),dimnames = list(c(),city))
for (i in 1: length(city)){
  for (j in 1:length(data[,1])){
    if (city[i] == trim(as.character(unlist(data[j,]['city'])))){
      city_matrix[j,i]=1
    }else{
      city_matrix[j,i]=0      
    }
  }
}

#create binary matrix for category
category_matrix<- matrix(nrow = length(data[,1]),ncol = length(category),dimnames = list(c(),category))
for (i in 1: length(category)){
  for (j in 1:length(data[,1])){
    if (regexpr(category[i],trim(as.character(unlist(data[j,]['categories'])))) > 0){
      category_matrix[j,i]=1
    }else{
      category_matrix[j,i]=0      
    }
  }
}


#get chi_square result for 30*30 pais
chi_matrix = matrix(nrow =30,ncol = 30,dimnames  = list(city,category))
p_matrix = matrix(nrow =30,ncol = 30,dimnames  = list(city,category))
for (i in 1 :length(city)){
  for(j in 1 : length(category)){
    
    b_matrix = matrix(c(0,0,0,0),nrow =2)    
    for (k in 1:length(data[,1])){
      if (city_matrix[k,i] == 0 & category_matrix[k,j] == 0){
        b_matrix[1] = b_matrix[1] + 1
      }
      if(city_matrix[k,i] == 0 & category_matrix[k,j] == 1){
        b_matrix[2] = b_matrix[2] + 1
      }
      
      if(city_matrix[k,i] == 1 & category_matrix[k,j] == 0){
        b_matrix[3] = b_matrix[3] + 1
      } 
      if (city_matrix[k,i] == 1 & category_matrix[k,j] == 1){
        b_matrix[4] = b_matrix[4] + 1
      }     
    }
    
    result = chisq.test(b_matrix)$statistic
    p = chisq.test(b_matrix)$p.value
    if(is.nan(result)){
      chi_matrix[i,j] =0
      p_matrix[i,j] = 0
    }else{
      chi_matrix[i,j] = result 
      p_matrix[i,j] = p
    }
    
  }  
}

#get top5 attribute pair
top5 <- order(chi_matrix,decreasing=T)[1:5]

for (i in top5){
  t = which(chi_matrix==chi_matrix[i],arr.ind=T)
  x = t[1]
  y = t[2]
  
  cat("city: ",city[x],"\n")
  cat("category: ",category[y],"\n")
  cat("chi_square: ",chi_matrix[i],'\n')
  cat("p: ",p_matrix[i],'\n')
}

#part d
agood <- cbind(city_matrix[,3],category_matrix[,7])
amax <- cbind(city_matrix[,3],category_matrix[,1])

amax_score <- c()
agood_score <- c()

sequence <- c(16,32,64,128,256,1024,2048,4096,8192)

for (n in sequence){
  testsample <- sample(1:length(data[,1]),n)
  
  b_matrix = matrix(c(0,0,0,0),nrow =2)
  for (k in testsample){
    if (amax[k,1] == 0 & amax[k,2] == 0){
      b_matrix[1] = b_matrix[1] + 1
    }
    if(amax[k,1] == 0 & amax[k,2] == 1){
      b_matrix[2] = b_matrix[2] + 1
    }
    
    if(amax[k,1] == 1 & amax[k,2] == 0){
      b_matrix[3] = b_matrix[3] + 1
    } 
    if (amax[k,1] == 1 & amax[k,2] == 1){
      b_matrix[4] = b_matrix[4] + 1
    } 
  }
  result = chisq.test(b_matrix)$statistic
  if(is.nan(result)){
    amax_score <- c(amax_score,0)
  }else{
    amax_score <- c(amax_score,result)
  }
  
}


for (n in sequence){
  testsample <- sample(1:length(data[,1]),n)
  
  b_matrix = matrix(c(0,0,0,0),nrow =2)
  for (k in testsample){
    if (agood[k,1] == 0 & agood[k,2] == 0){
      b_matrix[1] = b_matrix[1] + 1
    }
    if(agood[k,1] == 0 & agood[k,2] == 1){
      b_matrix[2] = b_matrix[2] + 1
    }
    
    if(agood[k,1] == 1 & agood[k,2] == 0){
      b_matrix[3] = b_matrix[3] + 1
    } 
    if (agood[k,1] == 1 & agood[k,2] == 1){
      b_matrix[4] = b_matrix[4] + 1
    } 
  }
  result = chisq.test(b_matrix)$statistic
  if(is.nan(result)){
    agood_score <- c(agood_score,0)
  }else{
    agood_score <- c(agood_score,result)
  }
  
}

plot(sequence,amax_score,col='red',type='l',ylab = "chi square score",main='size vs chi_square score')
lines(sequence,agood_score,col='green',type='l')
legend("topleft", legend = c("good attribute",'best attribute'), col=c('red','green'), lty=c(1,1))











