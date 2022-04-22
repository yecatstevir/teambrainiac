# University of Michigan Master of Applied Data Science Capstone Team Brainiac

Authors:

- Stacey Beck 
- Benjamin Merrill
- Mary Soules

## Repository Organization
    ├── Dockerfile                                   <- Details to build and run docker
    ├── requirements.txt                             <- Details of installed dependencies
    ├── README.md                                    <- This README file
    ├── .gitignore                                   <- Specifies files ignored by git
    |
    └── source/
    |    ├── streamlit/
    |    |    └──                                    <- Contains landing_page.py app
    |    ├── helper/
    |    |    └──                                    <- Contains modules and Jupyter Notebooks from early project exploration
    |    |__ SingleSubjectSVM_Norm_CV.ipynb           <-Contains modules to test normalization strategies (no normalization, percent signal change,z-normalization) and to run a cv search on best strategy once chosen.
    |    |__ BuildSingleSubjectSVM_Models.ipynb      <- Contains modules to run single subject SVM model. Output can be used inline or saved for future use.
    |    |__ DataExplorationNotebook_SingleSubjectSVM.ipynb  <- Contains modules to explore normalization strategies we employed and to look at cross validation results. This notebook pulls in previously stored data after running the XXXX
    |    |__ VisualizationPlayground.ipynb           <-
    |    |__ single_subject.py                       <- Contains functions to access data, mask data, normalize data, run single subject model. The model will run on more than one turn for training, if desired. At this point testing is done on single runs only. This also contains functions for getting predictions to be stored for later use, accuracy scores for data exploration.
    |    |__ brain_viz_single_subj.py                <- Contains functions to create bmaps for brain visualizations, functions for brain images, interactive brain images, and functions to display decision functions scores across the time-series
    |    ├── group_svm/                              <- Also includes notebooks to demonstrate directory modules
    |    |__  |__ data/                              <-
    |    |__  |__ images/                            <-
    |    |__  |__ Adolescent_Group_SVM.ipynb         <-
    |    |__  |__ Explore_data.ipynb                 <-
    |    |__  |__ Young_Adult_Group_SVM.ipynb        <-
    |    |__  |__ Timeseries_Cross_Validation.ipynb  <-
    |    |__  |__ Group_charts.ipynb                 <-
    |    |__  |__ Group_All_MASK_SVM.ipynb           <-
    |    |    └── access_data.py                     <- Connect to AWS, uploads and downloads data
    |    |    └── analysis.py                        <- Collects metrics from models and saves data, uploading to AWS
    |    |    └── cross_validation.py                <- Partitions data using TimeSeries package from Sklearn for cross validation and gridsearch
    |    |    └── dataframes.py                      <- May want to rid of this file
    |    |    └── process.py                         <- Processes the data from MATLAB further, organizes data for model training
    |    |    └── train.py                           <- Training file for SVM using Train, Validation, Test or Train and Test sets
    |    |    └── visualize.py                       <- Code to visualize certain plots using Nilearn as well as normalization exploration
    |    └── data   
    |    |    └──                                    <- Contains data needed to be accessed within /source. Data dictionary, and T1 images for visualization 
    |    ├── DL/
    |    |    └──                                    <- Deep Learning folder containing modules and notebook to run 3D-CNN from AWS to analysis
 
## Environment Set-up

- requires path_config.py to access data from cloud storage
- store path_config.py in ./source

### Connect to Dockerfile 
#### build 
    docker build -t test_container .

#### run
    docker run -p 80:80 -v ~/path/teambrainiac:/source test_container

* specify your path where 'path'

### Install packages locally

#### run:
    !pip install boto3 nibabel nilearn
    
### For Streamlit app
    Streamlit's prerequisites:
        - IDE or text editor
        - Python 3.7 - Python 3.9
        - PIP
        
#### macOS/Linux:
        sudo easy_install pip
        
        pip3 install pipenv
        
        pipenv shell
        
        pipenv install streamlit
        
#### Run app in repo:
        pipenv shell
        
        streamlit run landing_page.py
        
#### To generally view the app in browser:
        https://share.streamlit.io/yecatstevir/teambrainiac/main/source/streamlit/landing_page.py
        

### Data in AWS:
- all_data_dictionary.pkl         : whole brain masked, rt_label filtered, UNNORMALIZED 2d numpy data for all subjects
- whole_brain_all_norm_2d.pkl     : whole brain masked, rt_label filtered, NORMALIZED 2d numpy data for all subjects
- all_data_masksubACC_norm_2d.pkl : subACC masked, rt_label filtered, NORMALIZED 2d numpy data for all subjects
- all_data_masksubAI_norm_2d.pkl  : subAI masked, rt_label filtered, NORMALIZED 2d numpy data for all subjects
- all_data_masksubNAcc_norm_2d.pkl: N.Accumbens masked, rt_label filtered, NORMALIZED 2d numpy data for all subjects
- all_data_masksubmPFC_norm_2d.pkl: Prefrontal Cortex masked, rt_label filtered, NORMALIZED 2d numpy data for all subjects
- single_subj_T1_resampled.nii    : NIFTI T1 Brain Image file of a single subject for Visualizations
- w3rtprun_01.nii                 : Data Affine for maping voxel coordinates to Real World Coordinates for Visualizations

### All_subject_masked_labeled.ipynb

- This is the pre-processing notebook
- This notebook will perform masking and normalization as well as filtering by label for all matlab data with running one cell. 
- Once the data is returned as masked, filtered and then normalized, check the shape/dims
- Saves the data locally as pickle file

### Access_Load_Data.ipynb

- This is a demo notebook for how the function access_load_data() works in utils.py
- Saves dictionary pickle file of data paths for subject .mat data, subject IDs, mask .mat data, and labels in ./source/data directory

### Mat_to_Numpy.ipynb

- This is a demonstration for how we can access our data from AWS using our data path dictionary pickle file and convert the .mat data to numpy arrays
- Once we access the .mat data in AWS, it downloads locally to .source/data so we can access it and convert to numpy
- Image data is 2d, but we are able to convert to 4d as long as we know the x, y, z components of the image before it was compressed.
- Option to save the 2d, 4d, and label numpy array data in ./source/data directory

### Visualize_Data.ipynb

- Currently unable to run without 4d image data - awaiting original image shape information before this notebook is able to be executed without errors. 



