library('TDA')

# Simple Test to check if bottleneck works [Why doesn't have R have multiline comments?!]

#diagram1 <-as.matrix(read.csv(file="/home/nagarjun/Desktop/bitbucket/editdistancemergetree/persistence/input/tv_1-persistent-pairs.csv", header=TRUE, sep=","))
#diagram2 <-as.matrix(read.csv(file="/home/nagarjun/Desktop/bitbucket/editdistancemergetree/persistence/input/tv_2-persistent-pairs.csv", header=TRUE, sep=","))
# print(bottleneck(Diag1 = diagram1, Diag2 = diagram2, dimension = 0))

diagrams = list()

files_number <- 199

for (i in 1:files_number){
	parent_path <- "/home/nagarjun/Desktop/bitbucket/editdistancemergetree/other-distances/input/"
	file_number <- paste("split-pairs-tv_", i, sep="")
	file_name <- paste(file_number, ".csv", sep="")
	file_path <- paste(parent_path, file_name, sep="")
	diagram_csv <- read.csv(file=file_path, header=TRUE, sep=",")
	diagram <-as.matrix(diagram_csv)
	diagrams[[i]] <- diagram
}

for (i in 2:files_number){
	#Compare consecutively
	file_names <- paste(i-1, i, sep=",")
	bottleneck_distance <- bottleneck(Diag1 = diagrams[[i-1]], Diag2 = diagrams[[i]], dimension = 0)
	wasserstein_distance <- wasserstein(Diag1 = diagrams[[i-1]], Diag2 = diagrams[[i]], p = 2, dimension = 0)

	# Compare with the first one
	#file_names <- paste(1, i, sep=",")
	#bottleneck_distance <- bottleneck(Diag1 = diagrams[[1]], Diag2 = diagrams[[i]], dimension = 0)
	#wasserstein_distance <- wasserstein(Diag1 = diagrams[[1]], Diag2 = diagrams[[i]], p = 2, dimension = 0)

	distances <- paste(bottleneck_distance, wasserstein_distance, sep=",")
	output_line <- paste(file_names, distances, sep=",")
	print(output_line)
}
