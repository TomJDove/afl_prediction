
# Use the FitzRoy package to get AFL data from afltables.com

library(fitzRoy)

results <- fetch_results(season = 2000:2022, source = "afltables")
write.csv(results, file = "afl_matches.csv", row.names = FALSE)

# Get 2023 data

results2023 <- fetch_results(season = 2023, source = "afltables")
results2023
