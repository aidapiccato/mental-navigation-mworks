import pickle as pk
import numpy as np
N_DISTINCT_STIMS = 8
N_OPTIONS = 2
username = 'apiccato'
# username = 'aidapiccato'
dir_path = "/Users/%s/PycharmProjects/mental-navigation-mworks/pickle_meta" % username

meta_fn_tag = getvar('subject_id')

def hash(index, n_stims, block_index, seq_id, subject_id):
	''''
	Hash trial index to randomized version. Seed is meta tag and should be unique for each subject
	'''
	shuff = np.random.RandomState(seed=int(str(block_index) + str(seq_id) + str(subject_id))).permutation(np.arange(n_stims * n_stims * 2))
	return shuff[index]

seq_fn = "%s/seq_%s.pkl" % (dir_path, meta_fn_tag)
trial_fn = '%s/trials.pkl' % (dir_path)
subject_fn = '%s/subject_%s.pkl' % (dir_path, meta_fn_tag)

trial_meta = pk.load(open(trial_fn, 'rb'))
seq_meta = pk.load(open(seq_fn, 'rb'))
subject_meta = pk.load(open(subject_fn, 'rb'))

def get_trial_metaparameters():
	trial_idx = getvar('trial_index')
	subject_id = getvar('subject_id')
	block_idx = getvar('block_index')
	n_stims = getvar('n_stims')
	seq_id = getvar('seq_id')
	stim_pos = getvar('stim_pos')
	stim_bin = getvar('stim_bin')
	option_stims = np.random.choice(np.where(stim_bin)[0], N_OPTIONS)
	option_pos = np.repeat([-1], N_DISTINCT_STIMS)
	option_bin = np.zeros((N_DISTINCT_STIMS))
	option_bin[option_stims] = 1
	option_pos[option_stims] = np.random.permutation((np.arange(N_OPTIONS)))
	meta = trial_meta[n_stims]
	trial_id = hash(trial_idx, n_stims, block_idx, seq_id, subject_id)
	# randomly choose two of present stim from which to select
	setvar('py_trial_meta_id', int(meta['trial_meta_id'][trial_id]))
	setvar('py_trial_id', trial_id)
	setvar('py_start_stim_index', int(meta['start_stim_index'][trial_id]))
	setvar('py_end_stim_index', int(meta['end_stim_index'][trial_id]))
	setvar('py_stim_drift_direction', meta['stim_drift_direction'][trial_id])
	setvar('py_options_pos', option_pos)
	setvar('py_options_bin', option_bin)
	return


def get_seq_metaparameters():
	idx = int(getvar('seq_index'))
	meta = subject_meta
	setvar('py_n_stims', int(meta['n_stims'][idx]))
	setvar('py_stim_pos', meta['stim_pos'][idx])
	setvar('py_stim_bin', meta['stim_bin'][idx])
	setvar('py_stim_dist_cum', meta['stim_dist_cum'][idx])
	return

def get_seq_index():
	meta = subject_meta
	setvar('py_seq_index', int(meta['seq_index']))
	return
