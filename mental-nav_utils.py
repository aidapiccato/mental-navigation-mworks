import pickle as pk

username = 'apiccato'
# username = 'aidapiccato'
dir_path = "/Users/%s/PycharmProjects/mental-navigation-mworks/pickle_meta" % username
meta_fn_tag = getvar('meta_index')

seq_fn = "%s/seq_%s.pkl" % (dir_path, meta_fn_tag)
trial_fn = '%s/trial_%s.pkl' % (dir_path, meta_fn_tag)
session_fn = '%s/sess_%s.pkl' % (dir_path, meta_fn_tag)

trial_meta = pk.load(open(trial_fn, 'rb'))
seq_meta = pk.load(open(seq_fn, 'rb'))
sess_meta = pk.load(open(session_fn, 'rb'))

def get_trial_metaparameters():
	trial_idx = getvar('selection_trial_index')
	seq_idx = getvar('selection_seq_index')
	meta = trial_meta[seq_idx]

	setvar('py_start_stim_index', int(meta['start_stim_index'][trial_idx]))
	setvar('py_end_stim_index', int(meta['end_stim_index'][trial_idx]))
	setvar('py_pair_index', int(meta['pair_index'][trial_idx]))
	setvar('py_meta_trial_index', meta['meta_trial_index'][trial_idx])
	setvar('py_options_pos', meta['options_pos'][trial_idx])
	setvar('py_options_bin', meta['options_bin'][trial_idx])
	setvar('py_num_options', meta['num_options'][trial_idx])
	setvar('py_stim_drift_direction', meta['stim_drift_direction'][trial_idx])
	setvar('py_stim_dist_cum', meta['stim_dist_cum'][trial_idx])
	return


def get_seq_metaparameters():
	id = int(getvar('seq_id'))
	meta = seq_meta
	setvar('py_n_stims', int(meta['n_stims'][id]))
	setvar('py_stim_paths', meta['stim_paths'][id])
	return

def get_subject_metaparameters():
	subject_id = getvar('subject_id')

	meta = sess_meta[subject_id]
	setvar('py_seq_index', int(meta['seq_index']))
	setvar('py_seqs', meta['seqs'])



