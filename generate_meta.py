import pickle
import numpy as np
from itertools import permutations
import os

MAX_NUM_STIMS = 6
MIN_NUM_STIMS = 2
N_SEQ_LEN_REPEATS = 2
N_DISTINCT_STIMS = 8
IMAGE_PATH = '/images/objects1'
USERNAME = 'aidapiccato'
# USERNAME = 'apiccato'
dir_path = "/Users/%s/PycharmProjects/mental-navigation-mworks/pickle_meta" % USERNAME

meta_fn_tag = 1

def generate_trial_meta():
    a = []
    trial_meta_id = 0
    for n_stims in np.arange(MIN_NUM_STIMS, MAX_NUM_STIMS + 1):
        d = {
            'stim_drift_direction': [],
            'trial_meta_id': [],
            'start_stim_index': [],
            'end_stim_index': [],
        }
        start_idx = np.repeat(np.linspace(0, n_stims - 1, num=n_stims), n_stims * 2)
        end_idx = np.tile(np.linspace(0, n_stims - 1, num=n_stims), n_stims  * 2)
        n_conditions = n_stims**2 * 2
        for trial_id in np.arange(n_conditions):
            d['trial_meta_id'].append(trial_meta_id)
            d['stim_drift_direction'].append(1 if trial_id < (n_conditions / 2) else -1)
            d['start_stim_index'].append(start_idx[trial_id])
            d['end_stim_index'].append(end_idx[trial_id])
            trial_meta_id += 1
        a.append(d)
    fn = "%s/trials.pkl" % (dir_path)
    with open(fn, 'wb') as f:
        pickle.dump(a, f)


def generate_subject_meta(subject_id):
    subject = {
        'n_stims': [],
        'stim_bin': [],
        'stim_pos': [],
        'stim_dist_cum': [],
        'seq_index': 0
    }

    seq_lens = np.repeat(np.arange(MIN_NUM_STIMS, MAX_NUM_STIMS + 1), N_SEQ_LEN_REPEATS)

    np.random.shuffle(seq_lens)

    for seq_len in seq_lens:
        subject['n_stims'].append(seq_len)
        stims = np.random.choice(np.arange(N_DISTINCT_STIMS), seq_len, replace=False)
        stim_bin = np.zeros(N_DISTINCT_STIMS)
        stim_pos = np.repeat([-1], N_DISTINCT_STIMS)
        stim_bin[stims] = 1
        stim_pos[stims] = np.random.permutation(np.arange(seq_len))
        subject['stim_bin'].append(stim_bin)
        subject['stim_pos'].append(stim_pos)
        stim_dist_cum = stim_pos + 1
        subject['stim_dist_cum'].append(stim_dist_cum)

    fn = "%s/subject_%s.pkl" % (dir_path, subject_id)

    with open(fn, 'wb') as f:
        pickle.dump(subject, f)

