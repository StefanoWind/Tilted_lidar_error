# Tilted_lidar_error
This repository is an implementation of the semi-empirical error model proposed by Letizia et al. 2024.

Cross-contamination_bias.py calculates the bias due to cross-contamination for an arbitrary profiling scan that applies eddy-covariance method to the "instantaneous" velocity components to estimate the Reynolds stresses. The function requires as inputs azimuths, elevations, and true Reynolds stress tensors.

Error_stdev_geometry.py calculates the geometrical amplification factor of the error standard deviation for either DBS or six-beam scans (tilted or regular). These factors determine how sampling error is amplified on the individual Reynolds stresses estimates for different scans. The function requires as inputs azimuths, elevations.
