# RF_Measurement

# RF Analysis Docker Container Usage Instructions

This document provides step-by-step instructions for using the RF Analysis Docker container to process S-parameter data and generate analysis plots.

## Prerequisites

- Docker installed on your system
- S-parameter (S2P) files for analysis

## Building the Docker Image

1. Clone the repository or download the source code containing the Dockerfile and Python scripts.
2. Open a terminal/command prompt and navigate to the directory containing the Dockerfile.
3. Build the Docker image using the following command:

   ```
   docker build -t rf_analysis .
   ```

   This command builds a Docker image and tags it as 'rf_analysis'.

## Preparing Your Data

1. Create a directory on your local machine to store your input S2P files.
2. Place all your S2P files in this directory.
3. Create an empty directory on your local machine for the output files.

## Running the Analysis

1. Open a terminal/command prompt, not Powershell if Windows system.
2. Navigate to the directory containing your input S2P files.
3. Run the Docker container using the following command if you are in the base directory of this repo:

   ```
   docker run -v /path/to/input:/data/input -v /path/to/output:/data/output yourusername/rf_measurement:latest --input_folder /data/input --output_folder /data/output
   ```

   This command does the following:
   - Mounts your current directory as the input directory in the container
   - Mounts a subdirectory named 'output' as the output directory in the container
   - Runs the rf_analysis container

4. The analysis will run, and the results will be saved in the 'output' directory.

## Output

After running the container, you should find the following in your 'output' directory:

- PNG files of various plots (e.g., Qfactor.png, Capacitance_conductance.png, Tunability.png)
- An HDF5 file (results.h5) containing the detailed analysis results

## Troubleshooting

If you encounter any issues:

1. Ensure your input directory contains valid S2P files.
2. Check that you have write permissions for the output directory.
3. If you get a "file not found" error, make sure you're in the correct directory when running the Docker command.
4. For permission issues, you may need to run Docker with elevated privileges or adjust the file permissions in the Dockerfile.

## Additional Notes

- The analysis parameters are currently set within the script. To change these, you'll need to modify the Python script and rebuild the Docker image.
- For large datasets, the analysis may take some time to complete. Be patient and allow the process to finish.

For any further questions or issues, please contact the maintainer of this Docker container.

## Prune unused/dangling image

   ```
   docker image prune
   ```


## Using the Docker Image from DockerHub

You can pull the latest version of the image from Docker Hub:

```
docker pull yourusername/rf_measurement:latest
```

To run the container:

```
docker run -v /path/to/input:/data/input -v /path/to/output:/data/output yourusername/rf_measurement:latest --input_folder /data/input --output_folder /data/output
```

Replace `/path/to/input` and `/path/to/output` with your actual input and output directory paths.