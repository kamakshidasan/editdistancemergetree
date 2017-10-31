# Does not work currently

library("TDA")

data <- read.csv(file="/home/nagarjun/Desktop/timedGaussian2/tv_1.csv", header=TRUE, sep=",")
Diag1 <- gridDiag(data[c('y','x')], FUNvalues = data['scalars'], sublevel = FALSE)

data <- read.csv(file="/home/nagarjun/Desktop/timedGaussian2/tv_199.csv", header=TRUE, sep=",")
Diag2 <- gridDiag(data[c('y','x')], FUNvalues = data['scalars'], sublevel = FALSE)

attach(mtcars)
par(mfrow=c(1,2))

plot(Diag1[["diagram"]])
plot(Diag2[["diagram"]])

print(bottleneck(Diag1 = Diag1[["diagram"]], Diag2 = Diag2[["diagram"]], dimension = 0))
#print(wasserstein(Diag1 = Diag1[["diagram"]], Diag2 = Diag2[["diagram"]], p = 2, dimension = 0))
