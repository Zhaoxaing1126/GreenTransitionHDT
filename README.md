# GreenTransitionHDT
GreenTransitionHDT is a comprehensive policy evaluation model for the green freight transition for heavy-duty trucks(HDTs). This repository includes the emission estimation model for CO~2~ and air pollutant emissions and the ARIMA statistical projection model. For more details, see the article "An Integrated Pathway Towards Timely Green Transition of Heavy-duty Trucks in China". Supporting data for this article is also included in this repository.

# *Note: 
This source is not a Python package. Users should run the code in a Python environment. In addition, several Python packages are required as shown in **System Requirements***.

## Authors
Pengjun Zhao*, Zhaoxiang Li, .
## License
This repository is licensed under the Apache License 2.0, see the LICENSE file for details.
## File descriptions
1. Individual_HDT_extraction.py: Codes for individual HDT data extraction based on vehicle license plate ID. Lines 2-9 are the import of the dependent python libraries. Lines 12-19 are the creation of read/write paths and reading of base data. Lines 22-27 are the extraction of individual HDT data for each day.
2. EmissionEstimation_Trajectorylevel.py: codes for trajectory-level emission estimation in the TrackATruck model. Lines 1-13 of the code run the import of the dependent python libraries. Lines 15-24 run the process of importing the underlying data involving the basic parameters of the model. Lines 26-158 are the main program that contains the processing of the GPS trajectory data and the emission estimation process.
3. GPS_Data.rar: the test data, including GPS trajectory data from three heavy-duty trucks(HDTs) over a three-day period (July 11 to July 13, 2016).The license plate information of the HDTs has been encrypted due to the data privacy information involved.
4. emissionrate.csv: emission factors of CO~2~ and air pollutants under National IV standard.Emission factors for each category of emissions are provided in the form of 23 Opmode intervals.
5. Binfrequency.csv: test HDT trajectories with real Opmodes distribution. It is used to calculate the simulated Opmodes distribution for the test GPS trajectory data(GPS_Data.rar).
6. 

# Running the demo
We recommend that the user's device meets the following system requirements. Users can follow the steps below to run the code based on the test data provided.

## System requirements
1. Operating system: Windows 10/Linux.
2. Python version: 3.9.12 or higher.
3. Python libraries versions: pandas(>=0.5.1), numpy(>=1.11.8), os(>=3.1.1), matplotlib(>=1.5), time(>=0.8.2), tqdm(>=3.5.1), math(>=1.4.4), itertools(>=1.0.14), statsmodels(>=0.8.3).

## Step 1: preparing the files and setting operations

## Step 2: running the codes
