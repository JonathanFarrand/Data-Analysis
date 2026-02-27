library(arrow)

# Read the feather file
path <- "data/setup/created/ball_by_ball2.feather"
ball_data <- read_feather(path)

# View it
head(df2)
