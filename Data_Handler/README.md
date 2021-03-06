## Data_Handler

### SQL folder
This folder contained all the SQL scripts needed for the project
1. `_AVE.sql` is used to create the Confusion Matrix and False Positive Rate.
2. `_conversion.sql` is used to create Conversion Rate, Rolling Conversion Rate and Delta.  
3. `_partner_ranking.sql` is used to create Quote Ranking Proportion.
4. `_percentageDiscount.sql` is used to create Percentage Discounted.
5. `_rankCompareMatrix.sql` is used to create Rank Comparison Matrix.
6. `_sales_volume.sql` is used to create Sales.
 
 
### 1.Import_Data
This module handles all importing functions from Bigquery.

**Note:** *Please change the credentials file to your
local directory.*
```
os.environ['GOOGLE_APPLICATION_CREDENTIALS'
                   ] = r'C\Users\%name%\AppData\Roaming\gcloud\application_default_credentials.json'
```
 
Give the SQL script path to initialise it. 
```
from Data_Handler.Import_Data import import_data
import_cls = import_data('2.Model_refit.sql')
```
1. `import_cls.df` to return the dataset.
2. `import_cls.df_info()` to print a log file to the `my_logs` directory.


### 2.MyPickle
This module allows you dump and load pickle object from the directory.
1. `load('\\path\file.pkl')`
2. `dump(object, '\\path\file.pkl')`


### 3.logging
Like the `MyPickle` above, this module allows you to log data to the local folder with more specifications such as timestamps and file format.

1. `save_fig(fig_id, *, tight_layout=True,fig_extension="png", resolution=300)` <br>
	Allows you to save `png` file image to `my_logs` directory.
	<br>
	<br>

2. `dump_mojo(model, *, production=False, timestamp=False)`<br>
	 Allows you to export the H2O mojo file to a production folder `scoring\MOHO_PROD` or a development folder `MOJO_DEV`. The export file can either have a timestamps or without.
	



### 4.GCP_StorageBucket
This module allows you to do the following:

| Description     				              | Syntax |
| ----------- 						          | ----------- |
|a. Create bucket in the google cloud storage | `create_bucket('bucket_name')`|
|b. Upload object to the bucket               | `upload_blob('bucket_name', r'/source/file/path/name.format', 'name.format')`|
|c. Download object from the bucket           | `download_blob('bucket_name', 'name.format', r'/destination/path/file/name.format')`        			|
|d. Delete object from the bucket             | `delete_blob('bucket_name', 'name.format')`       				|









