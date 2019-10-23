import pickle
import numpy as np

def generate_meta(n_condition_repeats, num_stims, max_dist, prob, filename):
    '''
    :param n_condition_repeats: Number of times a pair is repeated (each time with different inter image dist)
    :param n_stims: Number of distinct stimuli
    :param max_dist: Maximum distance in units of padding between stimuli
    :param prob: Probability for geometric distribution
    :return: Nothing. Save s
    '''
    meta = {
        'stim_drift_direction': [],
        'stim_dist_cum': [],
        'meta_index': [],
        'start_stim_index': [],
        'end_stim_index': [],
        'pair_index': [],
        'options_list': [],
        'num_options': []
    }
    start_idx = np.repeat(np.linspace(0, num_stims - 1, num=num_stims), num_stims-1)
    # end_idx = np.tile(np.linspace(0, num_stims - 1, num=num_stims), num_stims-1)
    end_idx = np.repeat(np.linspace(0, num_stims - 1, num=num_stims), num_stims-1)
    # end_idx = np.concatenate([np.asarray(np.delete(np.arange(num_stims), i)) for i in range(num_stims)])
    print(end_idx)
    num_pairs = num_stims * (num_stims - 1)
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
            right = [] if end_stim_index == num_stims - 1 else np.arange(end_stim_index + 1, num_stims)
            # right = np.arange(end_stim_index + 1, np.amin((num_stims - 1, end_stim_index + 1)))
            num_options = np.random.randint(2, num_stims)
            meta['num_options'].append(num_options)
            # options_list = np.random.choice(np.concatenate((np.arange(0, end_stim_index), np.arange(end_stim_index+1, num_stims))), num_)
            options_list = np.random.permutation(np.concatenate(([end_stim_index],
                                                                        np.arange(0, end_stim_index),
                                                                        right)))
            meta['options_list'].append(options_list)
            stim_dist = np.random.geometric(prob, size=num_stims)
            stim_dist = np.clip(stim_dist, 1, max_dist)
            stim_dist_cum = np.cumsum(stim_dist)
            meta['stim_dist_cum'].append(stim_dist_cum)

    with open(filename, 'wb') as f:
        pickle.dump(meta, f)