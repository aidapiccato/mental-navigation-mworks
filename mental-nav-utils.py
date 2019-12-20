import pickle as pk
import numpy as np
N_DISTINCT_STIMS = 8
MAX_NUM_STIMS = 6
MIN_NUM_STIMS = 2
N_OPTIONS = 2

# REPLACE WITH CORRECT PATH TO pickle_meta/ DIRECTORY
dir_path = "/Users/aidapiccato/PycharmProjects/mental-navigation-mworks/pickle_meta"

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
    meta = trial_meta[n_stims - MIN_NUM_STIMS]
    trial_id = hash(trial_idx, n_stims, block_idx, seq_id, subject_id)
    end_stim_index_image = np.where(np.asarray(stim_pos) == int(meta['end_stim_index'][trial_id]))[0]
    temp = np.where(np.asarray(stim_bin) == 1)[0]
    temp = temp[temp != end_stim_index_image]
    option_stims = np.random.choice(temp, N_OPTIONS - 1)
    option_stims = np.append(option_stims, end_stim_index_image)
    option_pos = np.repeat([-1], N_DISTINCT_STIMS)
    option_bin = np.zeros((N_DISTINCT_STIMS))
    option_bin[option_stims] = 1
    option_pos[option_stims] = np.random.permutation((np.arange(N_OPTIONS)))
    setvar('py_trial_meta_id', int(meta['trial_meta_id'][trial_id]))
    setvar('py_trial_id', trial_id)
    setvar('py_start_stim_index', int(meta['start_stim_index'][trial_id]))
    setvar('py_end_stim_index', int(meta['end_stim_index'][trial_id]))
    setvar('py_stim_drift_direction', meta['stim_drift_direction'][trial_id])
    setvar('py_options_pos', option_pos)
    setvar('py_options_bin', option_bin)
    setvar('py_option_0', np.where(option_pos == 0)[0][0])
    setvar('py_option_1', np.where(option_pos == 1)[0][0])
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

def set_seq_index():
    idx = int(getvar('seq_index'))
    subject_id = int(getvar('subject_id'))
    meta = subject_meta
    meta['seq_index'] = idx
    with open('%s/subject_%s.pkl' % (dir_path, subject_id), 'wb') as f:
        pk.dump(meta, f)
