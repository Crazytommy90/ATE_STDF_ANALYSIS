/****************************************************************************

Copyright (c) 2018, Xi Wang & Jinan Bayes Information Technology Co., Ltd.
All rights reserved.

License: BSD 3-Clause
Created: June 15, 2018
Author:  Xi Wang - powerddt@163.com

****************************************************************************/

#include <hdf5.h>

#ifdef __cplusplus
extern "C" {
#endif


typedef struct dataframe{
	const void *column;
	const void *index;
	const void *data;
} DATAFRAME;


/*-------------------------------------------------------------------------
*
* Set attribute functions
*
*-------------------------------------------------------------------------
*/
herr_t Bayes_H5Aset_attribute_string(hid_t data_obj, const char *attr_name, const char *attr_data);
herr_t Bayes_H5Aset_attribute_llong(hid_t data_obj, const char *attr_name, unsigned long long attr_data);
herr_t Bayes_H5Aset_attribute_bitfield(hid_t data_obj, const char *attr_name, char attr_data);
herr_t Bayes_H5Aset_group_global_attributes(hid_t data_obj);
herr_t Bayes_H5Aset_dataset_global_attributes(hid_t data_obj);

herr_t Bayes_H5Gset_create_dataframe_group(hid_t root_id, const char *group_name, int col, int row, int col_str_len_max, const void *column, const void *index, const void *data);
herr_t Bayes_H5Gset_create_dataframe_group2(hid_t root_id, const char *group_name, int col, int row, int col_str_len_max, DATAFRAME df);

#ifdef __cplusplus
}
#endif
