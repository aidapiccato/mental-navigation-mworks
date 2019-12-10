import pickle as pk
import numpy as np

# username = 'apiccato'
username = 'aidapiccato'
dir_path = "/Users/%s/PycharmProjects/mental-navigation-mworks/pickle_meta" % username

meta_fn_tag = getvar('meta_index')

def hash(index, n_stims, block_index, seq_id, subject_id):
	''''
	Hash trial index to randomized version. Seed is meta tag and should be unique for each subject
	'''
	shuff = np.random.RandomState(seed=int(str(block_index) + str(seq_id) + str(subject_id))).permutation(np.arange(n_stims * n_stims * 2))
	return shuff[index]

seq_fn = "%s/seq_%s.pkl" % (dir_path, meta_fn_tag)
trial_fn = '%s/trial_%s.pkl' % (dir_path, meta_fn_tag)
session_fn = '%s/sess_%s.pkl' % (dir_path, meta_fn_tag)

trial_meta = pk.load(open(trial_fn, 'rb'))
seq_meta = pk.load(open(seq_fn, 'rb'))
sess_meta = pk.load(open(session_fn, 'rb'))

def get_trial_metaparameters():
	trial_idx = getvar('trial_index')
	subject_id = getvar('subject_id')
	block_idx = getvar('block_index')
	n_stims = getvar('n_stims')
	seq_id = getvar('seq_id')
	meta = trial_meta[seq_id]
	trial_id = hash(trial_idx, n_stims, block_idx, seq_id, subject_id)
	setvar('py_trial_id', trial_id)
	setvar('py_start_stim_index', int(meta['start_stim_index'][trial_id]))
	setvar('py_end_stim_index', int(meta['end_stim_index'][trial_id]))
	setvar('py_options_pos', meta['options_pos'][trial_id])
	setvar('py_options_bin', meta['options_bin'][trial_id])
	setvar('py_num_options', meta['num_options'][trial_id])
	setvar('py_stim_drift_direction', meta['stim_drift_direction'][trial_id])
	setvar('py_stim_dist_cum', meta['stim_dist_cum'][trial_id])
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

