import math
import pickle as pk

dir_path = "/Users/apiccato/PycharmProjects/mental-navigation-mworks/pickle_meta"
meta_fn_tag = getvar('trials_from_meta')

fn = '%s/meta_ones.pkl' % dir_path
meta = pk.load(open(fn, 'rb'))

def get_metaparameters():
	idx = getvar('selection_index')
	setvar('py_start_stim_index', int(meta['start_stim_index'][idx]))
	setvar('py_end_stim_index', int(meta['end_stim_index'][idx]))
	setvar('py_pair_index', int(meta['pair_index'][idx]))
	setvar('py_meta_index', meta['meta_index'][idx])
	setvar('py_stim_dist_cum', meta['stim_dist_cum'][idx])
	setvar('py_options_list', meta['options_list'][idx])
	setvar('py_stim_drift_direction', meta['stim_drift_direction'][idx])
	return


