/****************************************************************************

Copyright (c) 2018, Xi Wang & Jinan Bayes Information Technology Co., Ltd.
All rights reserved.

License: BSD 3-Clause
Created: June 15, 2018
Author:  Xi Wang - powerddt@163.com

****************************************************************************/

#include "stdafx.h"

#include "HDF5PandasDataframe.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "H5ATTR.h"

/*-------------------------------------------------------------------------
*
* Set attribute functions
*
*-------------------------------------------------------------------------
*/

/*-------------------------------------------------------------------------
* Function: Bayes_H5Aset_attribute_strin
* Purpose: Write a stirng to an attribute of a data object
* Return: Success: 0, Failure: -1
* Author: Xi Wang (powerddt@163.com)
* Date: June 13, 2018
* Comments:
* Modifications:
*-------------------------------------------------------------------------
*/

herr_t Bayes_H5Aset_attribute_string(hid_t data_obj, const char *attr_name, const char *attr_data)
{
	herr_t status = H5ATTRset_attribute_string(data_obj, attr_name, attr_data, strlen(attr_data), H5T_CSET_UTF8);
	return status;
}

/*-------------------------------------------------------------------------
* Function: Bayes_H5Aset_attribute_llong
* Purpose: Write a 64-bit integer data to an attribute of a data object
* Return: Success: 0, Failure: -1
* Author: Xi Wang (powerddt@163.com)
* Date: June 13, 2018
* Comments:
* Modifications:
*-------------------------------------------------------------------------
*/

herr_t Bayes_H5Aset_attribute_llong(hid_t data_obj, const char *attr_name, unsigned long long attr_data)
{
	hsize_t dims[1] = {1}; // dimentison
	herr_t status = H5ATTRset_attribute(data_obj, attr_name, H5T_NATIVE_LLONG, 0, dims, (char*)&attr_data);
	return status;
}

/*-------------------------------------------------------------------------
* Function: Bayes_H5Aset_attribute_bitfield
* Purpose: Write a bitfield data (0 or 1) to an attribute of a data object
* Return: Success: 0, Failure: -1
* Author: Xi Wang (powerddt@163.com)
* Date: June 13, 2018
* Comments:
* Modifications:
*-------------------------------------------------------------------------
*/

herr_t Bayes_H5Aset_attribute_bitfield(hid_t data_obj, const char *attr_name, char attr_data)
{
	hsize_t dims[1] = { 1 }; // dimentison
	herr_t status = H5ATTRset_attribute(data_obj, attr_name, H5T_NATIVE_B8, 0, dims, &attr_data);
	return status;
}

/*-------------------------------------------------------------------------
* Function: Bayes_H5Aset_group_global_attribute
* Purpose: Write the global attributes to the data object
* Return: Success: 0, Failure: -1
* Author: Xi Wang (powerddt@163.com)
* Date: June 13, 2018
* Comments:
* Modifications:
*-------------------------------------------------------------------------
*/

herr_t Bayes_H5Aset_group_global_attributes(hid_t data_obj)
{
	herr_t status;
	status = Bayes_H5Aset_attribute_string(data_obj, "CLASS", "GROUP");
	status = Bayes_H5Aset_attribute_string(data_obj, "TITLE", "");
	status = Bayes_H5Aset_attribute_string(data_obj, "VERSION", "1.0");
	return status;
}

/*-------------------------------------------------------------------------
* Function: Bayes_H5Aset_dataset_global_attribute
* Purpose:  Write the global attributes to the data object
* Return: Success: 0, Failure: -1
* Author: Xi Wang (powerddt@163.com)
* Date: June 13, 2018
* Comments:
* Modifications:
*-------------------------------------------------------------------------
*/

herr_t Bayes_H5Aset_dataset_global_attributes(hid_t data_obj)
{
	herr_t status;
	status = Bayes_H5Aset_attribute_string(data_obj, "CLASS", "ARRAY");
	status = Bayes_H5Aset_attribute_string(data_obj, "FLAVOR", "numpy");
	status = Bayes_H5Aset_attribute_string(data_obj, "TITLE", "");
	status = Bayes_H5Aset_attribute_string(data_obj, "VERSION", "2.4");
	return status;
}

/*-------------------------------------------------------------------------
*
* Dataframe functions
*
*-------------------------------------------------------------------------
*/


/*-------------------------------------------------------------------------
* Function: Bayes_H5Gset_create_dataframe_group
* Purpose:  Create a group which stores a dataframe from arrays. Each dataframe contains four datasets.
* Return: Success: 0, Failure: -1
* Author: Xi Wang (powerddt@163.com)
* Date: June 13, 2018
* Comments:
* Modifications:
*-------------------------------------------------------------------------
*/

herr_t Bayes_H5Gset_create_dataframe_group(hid_t root_id, const char *group_name, int col, int row, int col_str_len_max, const void *column, const void *index, const void *data)
{
	herr_t status;

	//dataframe group: the group contains four dataset for each dataframe
	hid_t group_id = H5Gcreate(root_id, group_name, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
	Bayes_H5Aset_group_global_attributes(group_id);
	Bayes_H5Aset_attribute_string(group_id, "axis0_variety", "regular");
	Bayes_H5Aset_attribute_string(group_id, "axis1_variety", "regular");
	Bayes_H5Aset_attribute_string(group_id, "block0_items_variety", "regular");
	Bayes_H5Aset_attribute_string(group_id, "encoding", "UTF-8");
	Bayes_H5Aset_attribute_string(group_id, "pandas_type", "frame");
	Bayes_H5Aset_attribute_string(group_id, "pandas_version", "0.15.2");
	Bayes_H5Aset_attribute_llong(group_id, "nblocks", 1);
	Bayes_H5Aset_attribute_llong(group_id, "ndim", 2);

	hsize_t col_dim = col;
	hid_t col_space = H5Screate_simple(1, &col_dim, NULL);
	hid_t holding_tid = H5Tcreate(H5T_STRING, col_str_len_max); // the max length of each column name string (ignoring  '\0')

	// dataset axis0: column names (header of the dataframe), the same as block0_items
	hid_t axis0 = H5Dcreate(group_id, "axis0", holding_tid, col_space, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
	Bayes_H5Aset_dataset_global_attributes(axis0);
	Bayes_H5Aset_attribute_string(axis0, "kind", "string");
	// Bayes_H5Aset_attribute_string(axis0, "name", "N.");
	Bayes_H5Aset_attribute_bitfield(axis0, "transposed", 1);
	status = H5Dwrite(axis0, holding_tid, H5S_ALL, H5S_ALL, H5P_DEFAULT, column);

	// dataset block0_items: column names (header of the dataframe), the same as axis0
	hid_t block0_items = H5Dcreate(group_id, "block0_items", holding_tid, col_space, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
	Bayes_H5Aset_dataset_global_attributes(block0_items);
	Bayes_H5Aset_attribute_string(block0_items, "kind", "string");
	Bayes_H5Aset_attribute_string(block0_items, "name", "N.");
	Bayes_H5Aset_attribute_bitfield(block0_items, "transposed", 1);
	status = H5Dwrite(block0_items, holding_tid, H5S_ALL, H5S_ALL, H5P_DEFAULT, column);

	// dataset axis1: indexes of the dataframe (a time series)
	hsize_t row_dim = row;
	hid_t row_space = H5Screate_simple(1, &row_dim, NULL);
	hid_t axis1 = H5Dcreate(group_id, "axis1", H5T_NATIVE_LONG, row_space, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
	Bayes_H5Aset_dataset_global_attributes(axis1);
	Bayes_H5Aset_attribute_string(axis1, "kind", "integer");
	// Bayes_H5Aset_attribute_string(axis1, "name", "N.");
	Bayes_H5Aset_attribute_string(axis1, "index_class", "integer");
	Bayes_H5Aset_attribute_bitfield(axis1, "transposed", 1);
	status = H5Dwrite(axis1, H5T_NATIVE_LONG, H5S_ALL, H5S_ALL, H5P_DEFAULT, index);

	//dataset block0_values: values of dataframe
	hsize_t dims[2];
	dims[0] = row_dim;
	dims[1] = col_dim;
	hid_t col_row_space = H5Screate_simple(2, dims, NULL);
	hid_t block0_values = H5Dcreate(group_id, "block0_values", H5T_NATIVE_DOUBLE, col_row_space, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
	Bayes_H5Aset_dataset_global_attributes(axis1);
	Bayes_H5Aset_attribute_bitfield(block0_values, "transposed", 1);
	status = H5Dwrite(block0_values, H5T_NATIVE_DOUBLE, H5S_ALL, H5S_ALL, H5P_DEFAULT, data);

	// Close and release resources.
	status = H5Gclose(group_id);

	status = H5Dclose(axis0);
	status = H5Dclose(axis1);
	status = H5Dclose(block0_items);
	status = H5Dclose(block0_values);
	
	status = H5Sclose(col_space);
	status = H5Sclose(row_space);
	status = H5Sclose(col_row_space);

	return status;
}

/*-------------------------------------------------------------------------
* Function: Bayes_H5Gset_create_dataframe_group2
* Purpose:  Create a group which stores a dataframe from a DATAFRAME. Each dataframe contains four datasets.
* Return: Success: 0, Failure: -1
* Author: Xi Wang (powerddt@163.com)
* Date: June 13, 2018
* Comments:
* Modifications:
*-------------------------------------------------------------------------
*/

herr_t Bayes_H5Gset_create_dataframe_group2(hid_t root_id, const char *group_name, int col, int row, int col_str_len_max, DATAFRAME df)
{
	herr_t status;
	status = Bayes_H5Gset_create_dataframe_group(root_id, group_name, col, row, col_str_len_max, df.column, df.index, df.data);
	return status;
}