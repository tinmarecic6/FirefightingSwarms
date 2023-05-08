import pandas as pd

def get_mean(data,algorithm):
	data_mean = data.groupby(by="formation").mean()
	data_mean.insert(0,"algorithm",algorithm)
	return data_mean

data = pd.read_csv("AllRunResults_bckp.csv")
light_gen_chance = "light_generation_chance"

simpleAlg = "SimpleAlgorithm"
simpleAlgWithAvoid = "SimpleAlgorithmWihAvoidance"
piAlgorithm = "PIAlgorithm"
piAlgorithmWithAvoidance = "PIAlgorithmWithAvoidance"
simple_alg_data_0_001 = data[(data[light_gen_chance]==0.001) & (data["algorithm"]==simpleAlg)]
simple_alg_data_0_005 = data[(data[light_gen_chance]==0.005) & (data["algorithm"]==simpleAlg)]
simple_alg_data_0_01 = data[(data[light_gen_chance]==0.01) & (data["algorithm"]==simpleAlg)]

improved_simple_alg_data_0_001 = data[(data[light_gen_chance]==0.001)&(data["algorithm"]==simpleAlgWithAvoid)]
improved_simple_alg_data_0_005 = data[(data[light_gen_chance]==0.005)&(data["algorithm"]==simpleAlgWithAvoid)]
improved_simple_alg_data_0_01 = data[(data[light_gen_chance]==0.01)&(data["algorithm"]==simpleAlgWithAvoid)]

pi_data_0_001 = data[(data[light_gen_chance]==0.001) & (data["algorithm"]==piAlgorithm)]
pi_data_0_005 = data[(data[light_gen_chance]==0.005) & (data["algorithm"]==piAlgorithm)]
pi_data_0_01 = data[(data[light_gen_chance]==0.01) & (data["algorithm"]==piAlgorithm)]

pi_improved_data_0_001 = data[(data[light_gen_chance]==0.001)&(data["algorithm"]==piAlgorithmWithAvoidance)]
pi_improved_data_0_005 = data[(data[light_gen_chance]==0.005)&(data["algorithm"]==piAlgorithmWithAvoidance)]
pi_improved_data_0_01 = data[(data[light_gen_chance]==0.01)&(data["algorithm"]==piAlgorithmWithAvoidance)]



mean_simple_000_1 = get_mean(simple_alg_data_0_001,simpleAlg)
mean_simple_000_5 = get_mean(simple_alg_data_0_005,simpleAlg)
mean_simple_00_1 = get_mean(simple_alg_data_0_01,simpleAlg)

mean_improved_simple_000_1 = get_mean(improved_simple_alg_data_0_001,simpleAlgWithAvoid)
mean_improved_simple_000_5 = get_mean(improved_simple_alg_data_0_005,simpleAlgWithAvoid)
mean_improved_simple_00_1 = get_mean(improved_simple_alg_data_0_01,simpleAlgWithAvoid)

mean_pi_000_1 = get_mean(pi_data_0_001,piAlgorithm)
mean_pi_000_5 = get_mean(pi_data_0_005,piAlgorithm)
mean_pi_00_1 = get_mean(pi_data_0_01,piAlgorithm)

mean_improved_pi_000_1 = get_mean(pi_improved_data_0_001,piAlgorithmWithAvoidance)
mean_improved_pi_000_5 = get_mean(pi_improved_data_0_005,piAlgorithmWithAvoidance)
mean_improved_pi_00_1 = get_mean(pi_improved_data_0_01,piAlgorithmWithAvoidance)
