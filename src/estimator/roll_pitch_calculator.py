import argparse
import numpy as np

from estimator.data import trajectoryplanner, utilities
from estimator.data.datamaker import DataMaker
from estimator.data.datastore import DataStore
from estimator.state_estimator import StateEstimator


class RollPitchCalculator(StateEstimator):

    N_DIM = 6

    def estimate_state(self):

        roll, pitch = utilities.accs_to_roll_pitch(self.acc_data)
        yaw = np.zeros(roll.shape[0])
        self.rots = utilities.angles_to_rots_zyx(roll, pitch, yaw)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-D", "--datanum", required=False, help="Number of data file (1 to 3 inclusive)")

    args = vars(parser.parse_args())

    num = args["datanum"]
    if not num:
        planner = trajectoryplanner.round_trip_easy
        source = DataMaker(planner)
        m = np.ones(RollPitchCalculator.N_DIM)
        b = np.zeros(RollPitchCalculator.N_DIM)
    else:
        source = DataStore(dataset_number=num, path_to_data="data")

    f = RollPitchCalculator(source)
    f.estimate_state()

    if not num:
        utilities.plot_rowwise_data(["z-axis"], ["x", "y", "z"], [source.ts, source.ts], source.angles, f.angles)
    else:
        f.plot_comparison(f.rots, f.ts_imu, source.rots_vicon, source.ts_vicon)