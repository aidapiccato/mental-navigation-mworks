import pickle
import numpy as np
from itertools import permutations
import os

MAX_NUM_STIMS = 6
MIN_NUM_STIMS = 2
N_SEQ_LEN_REPEATS = 2
IMAGE_PATH = '/images/objects1'
USERNAME = 'aidapiccato'
#USERNAME = 'apiccato'
dir_path = "/Users/%s/PycharmProjects/mental-navigation-mworks/pickle_meta" % USERNAME

def length_to_ids(l, n):
    '''
    Returns list of n seq_ids, each corr. to sequences of length l
    :param l: Length of desired seqs
    :param n: Number of seqs of length l
    :return:
    '''
    if (l == 2):
        start_id = 0
    else:
        start_id = np.math.factorial(l - 1)
    n_distinct = np.math.factorial(l)
    ids = np.random.choice(np.arange(n_distinct), n, replace=False)
    ids += start_id
    return ids


def generate_sess_meta(subject_id, meta_fn_tag):
    ''''

    '''
    subject = {}
    subject['seq_index'] = 0
    # generate set of 10 sequences, two for each length
    seqs = []
    for l in np.arange(MIN_NUM_STIMS, MAX_NUM_STIMS + 1):
        seqs.append(length_to_ids(l, n=N_SEQ_LEN_REPEATS))

    seqs = np.asarray(seqs).reshape((N_SEQ_LEN_REPEATS * (MAX_NUM_STIMS - MIN_NUM_STIMS + 1), ))
    np.random.shuffle(seqs)
    subject['seqs'] = seqs
    fn = "%s/sess_%s.pkl" % (dir_path, meta_fn_tag)
    d = {}
    if not os.path.isfile(fn):
        with open(fn, 'wb') as f:
            pickle.dump(d, f)
    with open(fn, 'rb') as f:
        try:
            d = pickle.load(f)
        except (EOFError) as e:
            d = {}

    d[subject_id] = subject

    with open(fn, 'wb') as f:
        pickle.dump(d, f)



def generate_meta(
        meta_fn_tag,

        # experiment-level parameters
        min_num_stims=MIN_NUM_STIMS,
        max_num_stims=MAX_NUM_STIMS,
        image_folder_path=IMAGE_PATH,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              # trial-level parameters
        prob=0.7,
        max_dist=None,
        fixed_dist=1,
        num_options=2
        ):

    '''
    Generates meta file with sequences, num_images_repeats of each length in the range (min_num_images). Each
    :param min_num_stims:
    :param max_num_stims:
    :param image_folder_path:
    :return:
    '''

    seq_meta = {
        'n_stims': [],
        'stim_paths': [],
        'seq_id': []
    }

    seq_id = 0

    seq_trial_meta = []

    for num_stims_idx, n_stims in enumerate(range(min_num_stims, max_num_stims + 1)):
        seq_perms = np.asarray(list(permutations(np.arange(n_stims))))
        for seq in seq_perms:
            seq_meta['seq_id'].append(seq_id)
            seq_meta['n_stims'].append(n_stims)
            stim_paths = np.asarray(['%s/%s.jpg' % (image_folder_path, stim_ix) for stim_ix in seq], dtype=str)
            seq_meta['stim_paths'].append(stim_paths)
            trial_meta = generate_trial_meta(n_stims, max_dist, prob, num_options, fixed_dist)
            seq_trial_meta.append(trial_meta)
            seq_id += 1
    trial_meta_fn = "%s/trial_%s.pkl" % (dir_path, meta_fn_tag)
    with open(trial_meta_fn, 'wb') as f:
        pickle.dump(seq_trial_meta, f)
    seq_meta_fn = "%s/seq_%s.pkl" % (dir_path, meta_fn_tag)
    with open(seq_meta_fn, 'wb') as f:
        pickle.dump(seq_meta, f)

    return seq_meta

def generate_trial_meta(num_stims, max_dist, prob, num_options, fixed_dist):
    '''
    :param n_condition_repeats: Number of times a pair is repeated (each time with different inter image dist)
    :param n_stims: Number of distinct stimuli
    :param max_dist: Maximum distance in units of padding between stimuli
    :param prob: Probability for geometric distribution
    :return: Nothing.
    '''
    trial_meta = {
        'stim_drift_direction': [],
        'stim_dist_cum': [],
        'trial_meta_index': [],
        'start_stim_index': [],
        'end_stim_index': [],
        'options_bin': [],
        'options_pos': [],
        'num_options': []
    }
    start_idx = np.repeat(np.linspace(0, num_stims - 1, num=num_stims), num_stims*2)
    end_idx = np.tile(np.linspace(0, num_stims - 1, num=num_stims), num_stims*2)
    num_pairs = num_stims**2 * 2
    for pair_index in range(num_pairs):
        stim_drift_direction = 1 if pair_index < (num_pairs / 2) else -1
        trial_meta['start_stim_index'].append(start_idx[pair_index])
        trial_meta['end_stim_index'].append(end_idx[pair_index])
        trial_meta['trial_meta_index'].append(pair_index)
        trial_meta['stim_drift_direction'].append(stim_drift_direction)
        end_stim_index = end_idx[pair_index]
        other = np.arange(num_stims)
        other = other[np.where(other != end_stim_index)]
        num_options = np.random.choice([2, 4, num_stims]) if num_options is None else num_options
        options_ixs = np.asarray(np.concatenate(([end_stim_index],
                                                 np.random.choice(other, num_options - 1, replace=False))), dtype=int)
        options_pos, options_bin = np.zeros(num_stims), np.zeros(num_stims)
        options_bin[options_ixs] = 1
        options_pos[options_ixs] = np.random.permutation(np.arange(num_options))
        trial_meta['num_options'].append(num_options)
        options_pos = np.concatenate((options_pos, np.zeros(MAX_NUM_STIMS - num_stims)))
        options_bin = np.concatenate((options_bin, np.zeros(MAX_NUM_STIMS - num_stims)))
        trial_meta['options_pos'].append(options_pos)
        trial_meta['options_bin'].append(options_bin)
        if fixed_dist is None:
            stim_dist = np.random.geometric(prob, size=num_stims)
            stim_dist = np.clip(stim_dist, 1, max_dist)
            stim_dist_cum = np.cumsum(stim_dist)
            stim_dist_cum = np.concatenate((stim_dist_cum, np.zeros(MAX_NUM_STIMS - num_stims)))
            trial_meta['stim_dist_cum'].append(stim_dist_cum)
        else:
            stim_dist = np.repeat([fixed_dist], num_stims)
            stim_dist_cum = np.cumsum(stim_dist)
            stim_dist_cum = np.concatenate((stim_dist_cum, np.zeros(MAX_NUM_STIMS - num_stims)))
            trial_meta['stim_dist_cum'].append(stim_dist_cum)
    return trial_meta