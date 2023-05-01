import pandas as pd

data = pd.read_csv("AllRunResults_bckp.csv")
simple_alg_data_0_001 = data[(data["light_generation_chance"]==0.001) & (data["algorithm"]=="SimpleAlgorithm")]
simple_alg_data_0_005 = data[(data["light_generation_chance"]==0.005) & (data["algorithm"]=="SimpleAlgorithm")]
simple_alg_data_0_01 = data[(data["light_generation_chance"]==0.01) & (data["algorithm"]=="SimpleAlgorithm")]
improved_simple_alg_data_0_001 = data[(data["light_generation_chance"]==0.001)&(data["algorithm"]=="SimpleAlgorithmWihAvoidance")]
improved_simple_alg_data_0_005 = data[(data["light_generation_chance"]==0.005)&(data["algorithm"]=="SimpleAlgorithmWihAvoidance")]
improved_simple_alg_data_0_01 = data[(data["light_generation_chance"]==0.01)&(data["algorithm"]=="SimpleAlgorithmWihAvoidance")]



mean_000_1 = simple_alg_data_0_001.groupby(by="formation").mean()
mean_000_5 = simple_alg_data_0_005.groupby(by="formation").mean()
mean_00_1 = simple_alg_data_0_001.groupby(by="formation").mean()


# print(simple_alg_data[["algorithm","formation","light_generation_chance","time_passed"]])


