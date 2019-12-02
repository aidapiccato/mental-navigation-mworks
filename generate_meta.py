import pickle
import numpy as np

def generate_meta(n_condition_repeats, num_stims, max_dist, prob, filename, num_options_p=None):
    '''
    :param n_condition_repeats: Number of times a pair is repeated (each time with different inter image dist)
    :param n_stims: Number of distinct stimuli
    :param max_dist: Maximum distance in units of padding between stimuli
    :param prob: Probability for geometric distribution
    :return: Nothing.
    '''
    meta = {
        'stim_drift_direction': [],
        'stim_dist_cum': [],
        'meta_index': [],
        'start_stim_index': [],
        'end_stim_index': [],
        'pair_index': [],
        'options_bin': [],
        'options_pos': [],
        'num_options': []
    }
    start_idx = np.repeat(np.linspace(0, num_stims - 1, num=num_stims), num_stims)
    end_idx = np.tile(np.linspace(0, num_stims - 1, num=num_stims), num_stims)
    num_pairs = num_stims**2
    for t in range(n_condition_repeats):
        for pair_index in range(num_pairs):
            meta_index = t * num_pairs + pair_index
            stim_drift_direction = 1 if np.random.rand() > 0.5 else -1
            meta['start_stim_index'].append(start_idx[pair_index])
            meta['end_stim_index'].append(end_idx[pair_index])
            meta['pair_index'].append(pair_index)
            meta['meta_index'].append(meta_index)
            meta['stim_drift_direction'].append(stim_drift_direction)
            end_stim_index = end_idx[pair_index]
            other = np.arange(num_stims)
            other = other[np.where(other != end_stim_index)]
            if num_options_p is None:
                num_options = np.random.choice([2, 4, num_stims])
            else:
                num_options = num_options_p
            options_ixs = np.asarray(np.concatenate(([end_stim_index],
                np.random.choice(other, num_options - 1, replace=False))), dtype=int)
            options_pos, options_bin = np.zeros(num_stims), np.zeros(num_stims)
            options_bin[options_ixs] = 1
            options_pos[options_ixs] = np.random.permutation(np.arange(num_options))
            meta['num_options'].append(num_options)
            meta['options_pos'].append(options_pos)
            meta['options_bin'].append(options_bin)
            # stim_dist = np.random.geometric(prob, size=num_stims)
            # stim_dist = np.clip(stim_dist, 1, max_dist)
            # stim_dist_cum = np.cumsum(stim_dist)
            # meta['stim_dist_cum'].append(stim_dist_cum)

    with open(filename, 'wb') as f:
        pickle.dump(meta, f)