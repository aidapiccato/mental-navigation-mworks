import pickle as pk

dir_path = "/Users/aidapiccato/PycharmProjects/mental-navigation-mworks/pickle_meta"
meta_fn_tag = getvar('trials_from_meta')

fn = '%s/1.pkl' % dir_path
meta = pk.load(open(fn, 'rb'))

def get_metaparameters():
	idx = getvar('selection_index')
	setvar('py_start_stim_index', int(meta['start_stim_index'][idx]))
	setvar('py_end_stim_index', int(meta['end_stim_index'][idx]))
	setvar('py_pair_index', int(meta['pair_index'][idx]))
	setvar('py_meta_index', meta['meta_index'][idx])
	setvar('py_options_pos', meta['options_pos'][idx])
	setvar('py_options_bin', meta['options_bin'][idx])
	setvar('py_num_options', meta['num_options'][idx])
	setvar('py_stim_drift_direction', meta['stim_drift_direction'][idx])
	setvar('py_stim_dist_cum', meta['stim_dist_cum'][idx])
	return


