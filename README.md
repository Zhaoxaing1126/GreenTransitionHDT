# GreenTransitionHDT
GreenTransitionHDT is a comprehensive policy evaluation model for the green freight transition for heavy-duty trucks(HDTs). This repository includes the emission estimation model for CO~2~ and air pollutant emissions and the ARIMA statistical prediction model. For more details, see the article "An Integrated Pathway Towards Timely Green Transition of Heavy-duty Trucks in China".

## *Note: 
This source is not a Python package. Users should run the code in a Python environment. In addition, several Python packages are required as shown in **System Requirements***.

## Authors
Pengjun Zhao*, Zhaoxiang Li, .

## License
This repository is licensed under the Apache License 2.0, see the LICENSE file for details.

## File descriptions
1. Individual_HDT_extraction.py: codes for individual HDT data extraction based on vehicle license plate ID. Lines 2-9 are the import of the dependent python libraries. Lines 12-19 are the creation of read/write paths and reading of base data. Lines 22-27 are the extraction of individual HDT data for each day.
2. EmissionEstimation.py: codes for trajectory-level emission estimation in the TrackATruck model. Lines 1-13 of the code run the import of the dependent python libraries. Lines 15-24 run the process of importing the underlying data involving the basic parameters of the model. Lines 26-158 are the main program that contains the processing of the GPS trajectory data and the emission estimation process.
3. Prediction_HDTPopulation.py: codes for HDT population prediction in the ARIMA model. Lines 2-8 are the import of python dependency libraries. Lines 11-27 are base parameter settings and data loading. Lines 30-85 are ARIMA model construction with output of predicted data for HDT population included.
4. GPS_Data.zip: the test data, including GPS trajectory data from three heavy-duty trucks(HDTs) over a three-day period (July 11 to July 13, 2016).The license plate information of the HDTs has been encrypted due to the data privacy information involved.
5. Emissionrate.csv: emission factors of CO~2~ and air pollutants under National IV standard.Emission factors for each category of emissions are provided in the form of 23 Opmode intervals.
6. Binfrequency.csv: test HDT trajectories with real Opmodes distribution. It is used to calculate the simulated Opmodes distribution for the test GPS trajectory data(GPS_Data.rar).

# Running the demo
We recommend that the user's device meets the following system requirements. Users can follow the steps below to run the code based on the test data provided.

## System requirements
1. Operating system: Windows 11/Linux.
2. Python version: 3.9.12 or higher.
3. Python libraries versions: pandas(>=1.4.2), numpy(>=1.25.1), matplotlib(>=3.5.1), tqdm(>=4.64.0), statsmodels(>=0.13.2).

## Preparing the files and setting operations
1. Download all the files provided in the repository  within your workspace.
2. Decompress GPS_data.zip. The data consists of GPS trajectory for three consecutive days (July 11 to 13, 2016) for 3 HDTs.
3. Check if the Python libraries versions in your work environment matches the version required by the codes. It is recommended to check the installed python libraries and their versions by using the "pip list" command.

## Running the emission estiamtion model codes
1. Run codes in Individual_HDT_extraction.py. Lines 12 and 13 are the input folder for the test data and the output folder for the result data. the model output from files in GPS_Data.zip will save in the folder created in line 13. The output of the codes will create separate folders for each day's GPS data where the GPS trajectory for each HDT is a csv file.
2. Run codes in EmissionEstimation.py. Lines 27-34 are the input for the test data and the output folder for the result data. The input data is sourced with the output of Individual_HDT_extraction.py. The model output will save in the folder created in lines 30-34. The output data will add new columns containing CO~2~ and air pollutant emissions (in unit g) for the daily GPS data for each HDT.

## Running the HDT population prediction model codes
Run codes in Prediction_HDTPopulation.py. The code provides an implementation of a year-based time series prediction model. Line 19 is the loading of historical data. The time series data to be predicted can be changed according to the user's needs. Lines 31-36 are the plotting of autocorrelation function (ACF) and partial autocorrelation function (PACF) for time series data. Lines 55-78 are the measurements of the evaluation metrics for different combinations of parameters in the ARIMA model. The user need consider ACF, PACF and evaluation metrics to determine the optimal parameters of the model for practical applications.
